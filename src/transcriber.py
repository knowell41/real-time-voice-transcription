from logging import Logger
import pyaudio
import threading
import queue
import wave
import time
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf
import sounddevice as sd
import numpy as np
from datetime import datetime
import uuid
import os
import traceback


class Transcriber:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 4092
    RECORD_SECONDS = 2

    def __init__(self, logger: Logger, output_dir=None):
        self.logger = logger
        self.device = pyaudio.PyAudio()
        self.is_streaming = False
        self.frames = []
        self.output_dir = output_dir
        self.stream_thread = None
        self.audio_queue = queue.Queue()
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
        self.model = WhisperForConditionalGeneration.from_pretrained(
            "openai/whisper-base.en"
        )
        self.transcribed_text = ""
        self.prediction_thread = threading.Thread(
            target=self.process_predictions, daemon=True
        )
        self.prediction_thread.start()
        self.is_prediction_running = True

    def predict(self, speech_array: list, sampling_rate: int):
        try:
            # self.logger.debug(speech_array)
            input_features = self.processor(
                speech_array, sampling_rate=sampling_rate, return_tensors="pt"
            ).input_features
            predicted_ids = self.model.generate(input_features)
            return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[
                0
            ]
        except Exception as e:
            # If prediction encounters any error, just return an empty string.
            self.logger.error(traceback.print_exc())
            return ""

    def destroy_device(self):
        """Release PortAudio system resources"""
        self.logger.debug("Terminating Audio device...")
        self.device.terminate()
        self.logger.debug("Audio device terminated.")

    def start_listening(self):
        """Start streaming audio from the device"""
        if not self.is_streaming:
            self.is_streaming = True
            self.logger.debug("Starting audio stream...")
            self.stream_thread = threading.Thread(
                target=self._stream_audio, daemon=True
            )
            self.stream_thread.start()

    def _stream_audio(self):
        stream = self.device.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self._callback,
        )
        stream.start_stream()
        while self.is_streaming:
            time.sleep(1)

        self.stop_listening(stream)

    def stop_listening(self, stream=None):
        """Stop streaming audio from the device"""
        if self.is_streaming:
            self.is_streaming = False
            self.stream_thread.join()

            if stream is not None:
                stream.stop_stream()
                stream.close()

            self.logger.debug("Audio stream stopped.")

        self.destroy_device()

    def _callback(self, input_data, frame_count, time_info, flags):
        """Callback function to handle audio data during streaming."""
        self.frames.append(input_data)
        if len(self.frames) > 10:
            self.audio_queue.put((b"".join(self.frames), self.RATE))
            self.frames = []
        return (input_data, pyaudio.paContinue)

    def process_predictions(self):
        """Process audio data from the queue and generate transcriptions."""
        self.logger.debug("Prediction processing thread started.")
        while True:
            if not self.audio_queue.empty():
                speech_data, rate = self.audio_queue.get()

                # save chunk to wav
                # filename = self.to_wav(speech_data, rate)

                # get speech_array from chunk wav file
                # speech_array, sampling_rate = sf.read(filename)

                # get speech_array from raw stream data
                speech_array = np.frombuffer(speech_data, dtype=np.int16)
                text = self.predict(speech_array, self.RATE)
                print(text)
                self.transcribed_text += f"{text} "
            time.sleep(0.1)  # to avoid tight loop

    def to_wav(self, speech_data, rate):
        now = datetime.now()

        if not self.output_dir:
            self.output_dir = f"output/{uuid.uuid4().hex}"

        os.makedirs(self.output_dir, exist_ok=True)

        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/audio_chunk_{timestamp_str}.wav"
        sample_width = self.device.get_sample_size(self.FORMAT)
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(speech_data)

        return filename

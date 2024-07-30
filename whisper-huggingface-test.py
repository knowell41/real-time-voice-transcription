from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf

# Load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small.en")

# Load audio file (replace 'path/to/audio.wav' with your file path)
audio_path = "src/output.wav"
speech_array, sampling_rate = sf.read(audio_path)
print(speech_array)
# Preprocess the audio to the required format
input_features = processor(
    speech_array, sampling_rate=sampling_rate, return_tensors="pt"
).input_features

# # Generate token ids
predicted_ids = model.generate(input_features)

# # Decode the token ids to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription[0])

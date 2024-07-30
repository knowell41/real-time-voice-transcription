# Real Time Voice Transcription

The goal of this repo is to create a `python console` application that transcribe the speech in `real-time` using 2 major components;
- Audio stream
- Speech to text


## Audio stream

This component is responsible for accessing microphone of the device using `pyaudio` python module.

## Speech to text

This component is responsible for processing the Audio stream and convert it to `text` using `huggingface` model `https://huggingface.co/openai/whisper-base.en`.


# Environment Setup
1. clone this repo

```
> git clone https://github.com/knowell41/real-time-voice-transcription.git
> cd real-time-voice-transcription
```
2. Create virtual environment and install dependencies
```
> python3 -m venv  <your-env-name>
> source <your-env-name>/bin/activate
> pip install -r requirements.txt
```

# Run
```
> cd src
> python main.py
2024-07-30 17:40:33,270 - 6403351f - DEBUG - Terminating transcriber process...
2024-07-30 17:40:33,346 - 6403351f - DEBUG - Terminating Audio device...
2024-07-30 17:40:33,367 - 6403351f - DEBUG - Audio device terminated.
2024-07-30 17:40:33,369 - 6403351f - DEBUG - Audio stream stopped.
2024-07-30 17:40:33,369 - 6403351f - DEBUG - Terminating Audio device...
2024-07-30 17:40:33,369 - 6403351f - DEBUG - Audio device terminated.
========Transcribed text in this session=========
 You  >>  (static)  (mufflers speaking off microphone softly on mic )  [ Silence ]  - (indiscity chatter drown  It's a  (static buzzing loudly off microphone softly on radio)  [static noises]  (clippers buzzing loudly on TV)  [Music fades]  I  *Music fades*  (mumbling off microphone.)  (laugh's speech)  Okay.  *silicon*  [Music fades.]
=================================================
2024-07-30 17:40:33,369 - 6403351f - DEBUG - DONE

```


# ToDo
This script is not yet working as intended. There are few issues
- Not running in `real-time`
- Not transcribing the speech correctly.


## Similar Project
Exisisting javascript project of the same purpose which works very well.

[Web Speech API](https://www.google.com/intl/en/chrome/demos/speech.html) 

[Web Speech API Demo](https://www.google.com/intl/en/chrome/demos/speech.html)
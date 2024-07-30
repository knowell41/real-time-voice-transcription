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
```

# ToDo
This script is not yet working as intended. There are few issues
- Not running in `real-time`
- Not transcribing the speech correctly.


## Similar Project
Exisisting javascript project of the same purpose which works very well.

[Web Speech API](https://www.google.com/intl/en/chrome/demos/speech.html) 

[Web Speech API Demo](https://www.google.com/intl/en/chrome/demos/speech.html)
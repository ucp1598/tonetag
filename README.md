# ToneTag

**Does an AI respond better when it knows *how* you said something, not just *what* you said?**

ToneTag is a small personal project that explores this question. The goal: you speak into a
microphone, and the app produces a transcript plus short "tone tags" describing how it
sounded, for example:

    [hesitant, quiet, slow] I don't know... I guess I'm okay.

The plan is to ask an AI assistant to reply twice, once to the plain transcript and once to the
tone-tagged version, and show the two replies side by side so the difference is easy to judge.

> ToneTag describes the *apparent* tone of a recording using simple, readable rules and
> pretrained models. It does not know what anyone truly feels, and it is not a mental-health
> or diagnostic tool.

## Status: early work in progress

| Piece | State |
|---|---|
| Speech-to-text with word timestamps | Working |
| Project setup, tests | Working |
| Prosody features (pitch, energy, pauses, speech rate) | Planned |
| Emotion model on the audio | Planned |
| Rule-based tone tags, each with the measurement that triggered it | Planned |
| Plain vs tone-tagged AI replies, side by side | Planned |
| Streamlit app with microphone input | Planned |
| Written comparison of the results | Planned |

## What works today

Give it a short English audio clip and it prints the transcript and the start and end time
of every word. Those timestamps are the foundation for later measuring pauses and speech rate.

## Tech stack (current)

- Python 3.11
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (`small` model, CPU, int8) for transcription
- pytest for tests

Planned: Streamlit, praat-parselmouth and librosa (prosody), Hugging Face `transformers`
(pretrained speech-emotion model). The current local processing stack is free and open source and runs on a normal laptop CPU. No model training is involved

## Install and run

Developed and tested on Windows with Python 3.11. Other platforms have not been tested.
Run these in PowerShell:

    py -3.11 -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

Transcribe the included demo clip:

    python -m tonetag.transcribe samples/hello.wav

Expected output is the transcript followed by a word-by-word list with start and end times.
The first run downloads the `small` Whisper model (about 460 MB), which is cached afterwards.
`samples/hello.wav` is a synthetic clip made with text-to-speech, not a real person's voice.

## Run the tests

    pytest

## Limitations

- English only.
- Record a clip, then analyze it. There is no real-time streaming.
- Transcription can make mistakes, especially with fast, quiet or noisy speech.
- Tone tags will be rough, rule-based guesses, not facts about a person.
- Only tested on Windows with Python 3.11.

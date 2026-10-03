"""Speech-to-text: audio file -> transcript + word timestamps (faster-whisper, CPU)."""
from dataclasses import dataclass

from faster_whisper import WhisperModel

# "small" is a good accuracy/speed balance on a laptop CPU. Use "base" if it is too slow.
MODEL_SIZE = "small"

_model = None  # loaded once, because loading takes a few seconds


@dataclass
class Word:
    text: str
    start: float  # seconds from start of clip
    end: float


@dataclass
class Transcript:
    text: str
    words: list
    duration: float  # total clip length in seconds
    language: str


def _get_model(model_size=MODEL_SIZE):
    global _model
    if _model is None:
        # int8 = compressed weights, much faster on CPU with little accuracy loss
        _model = WhisperModel(model_size, device="cpu", compute_type="int8")
    return _model


def transcribe(audio_path, model_size=MODEL_SIZE):
    """Transcribe an audio file (English). Returns a Transcript."""
    model = _get_model(model_size)
    # word_timestamps=True gives per-word start/end times (needed later for pauses and speech rate)
    segments, info = model.transcribe(
        str(audio_path), language="en", word_timestamps=True, vad_filter=True
    )
    words = []
    for seg in segments:  # segments is a generator: the work happens as we loop
        for w in seg.words or []:
            words.append(Word(text=w.word.strip(), start=w.start, end=w.end))
    text = " ".join(w.text for w in words)
    return Transcript(text=text, words=words, duration=info.duration, language=info.language)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit("Usage: python -m tonetag.transcribe path\\to\\clip.wav")
    t = transcribe(sys.argv[1])
    print(f"Transcript: {t.text}")
    print(f"Duration: {t.duration:.1f}s, words: {len(t.words)}")
    for w in t.words:
        print(f"  {w.start:6.2f} - {w.end:6.2f}  {w.text}")

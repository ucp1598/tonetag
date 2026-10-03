import wave
from pathlib import Path

import pytest

from tonetag.transcribe import Transcript, transcribe

SAMPLE = Path(__file__).parent.parent / "samples" / "hello.wav"


def test_silence_gives_empty_transcript(tmp_path):
    # 1 second of silence: should not crash and should return no words
    path = tmp_path / "silence.wav"
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(b"\x00\x00" * 16000)
    t = transcribe(path)
    assert isinstance(t, Transcript)
    assert t.words == []
    assert t.duration == pytest.approx(1.0, abs=0.1)


@pytest.mark.skipif(not SAMPLE.exists(), reason="samples/hello.wav not present")
def test_sample_speech_has_words_and_ordered_timestamps():
    t = transcribe(SAMPLE)
    assert len(t.words) > 0
    assert all(w.end >= w.start for w in t.words)
    assert [w.start for w in t.words] == sorted(w.start for w in t.words)

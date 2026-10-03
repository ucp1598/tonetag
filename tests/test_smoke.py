import importlib


def test_package_modules_import():
    for name in ("transcribe", "prosody", "emotion", "tagger", "llm"):
        importlib.import_module(f"tonetag.{name}")


def test_third_party_imports():
    for name in ("streamlit", "faster_whisper", "parselmouth", "librosa", "transformers", "torch"):
        importlib.import_module(name)

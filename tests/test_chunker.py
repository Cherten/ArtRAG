import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.chunker import chunk_text

def test_chunk_size():
    text = "word " * 600
    chunks = chunk_text(text, chunk_size=500)
    assert all(len(c) <= 550 for c in chunks)
    assert len(chunks) >= 5

def test_empty_text():
    assert chunk_text("") == []

def test_short_text():
    text = "Short text."
    chunks = chunk_text(text, chunk_size=500)
    assert len(chunks) == 1
    assert chunks[0] == text
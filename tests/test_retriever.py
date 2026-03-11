import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.retriever import Retriever

@pytest.fixture
def retriever():
    if not os.path.exists("data/index/art.index"):
        pytest.skip("Индекс не найден, пропускаем тест")
    return Retriever()

def test_retrieve_returns_list(retriever):
    results = retriever.retrieve("painting", k=3)
    assert isinstance(results, list)
    assert len(results) == 3
    for r in results:
        assert "chunk" in r
        assert "score" in r
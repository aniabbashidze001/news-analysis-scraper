"""
Unit tests for the article processing pipeline in processors.py.

Tests include:
- Processing of raw article files and deduplication
- Date normalization function for various formats
- Article validity checking based on required fields
All tests use temporary paths to avoid altering real data.
"""

import sys
import os
import json
import pytest
from src.data.processors import process_raw_articles, RAW_DIR, PROCESSED_PATH
from src.data.processors import normalize_date, is_valid_article

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

RAW_DIR = "data_output/raw"
PROCESSED_PATH = "data_output/processed/cleaned_articles.json"


@pytest.fixture
def setup_test_file(tmp_path, monkeypatch):
    """
        Fixture that sets up a temporary raw data file and patches processor paths.

        Creates a raw JSON file with two articles (one valid, one duplicate/invalid),
        and sets `RAW_DIR` and `PROCESSED_PATH` to use temporary paths for safe testing.

        Returns:
            Path to the expected cleaned articles output file.
    """
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    processed_path = tmp_path / "processed" / "cleaned_articles.json"
    processed_path.parent.mkdir()

    monkeypatch.setattr("src.data.processors.RAW_DIR", str(raw_dir))
    monkeypatch.setattr("src.data.processors.PROCESSED_PATH", str(processed_path))

    test_file = raw_dir / "aj.json"
    test_data = [
        {
            "title": "Test Article",
            "link": "http://test.com/article-1",
            "published": "2025-06-17",
            "category": "test",
        },
        {
            "title": "Duplicate Test Article",
            "link": "http://test.com/article-1",
            "published": "bad-date",
            "category": "test",
        },
    ]
    with test_file.open("w", encoding="utf-8") as f:
        json.dump(test_data, f)

    return processed_path


def test_process_raw_articles(setup_test_file):
    """
        Test that process_raw_articles filters out invalid/duplicate articles
        and writes a correctly cleaned JSON output.
    """
    processed_path = setup_test_file
    process_raw_articles()

    assert processed_path.exists()
    with open(processed_path, "r", encoding="utf-8") as f:
        result = json.load(f)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["title"] == "Test Article"


def test_normalize_date_valid_formats():
    """
        Test normalize_date with valid date formats and embedded date strings.
    """
    assert normalize_date("2025-06-22") == "2025-06-22"
    assert normalize_date("2025/06/22") == "2025-06-22"
    assert normalize_date("Date: 2025-06-22") == "2025-06-22"
    assert normalize_date("2025/06/22 extra text") == "2025-06-22"


def test_normalize_date_invalid():
    """
        Test normalize_date with invalid inputs, ensuring None is returned.
    """
    assert normalize_date(None) is None
    assert normalize_date("") is None
    assert normalize_date("invalid-date") is None
    assert normalize_date(12345) is None


def test_is_valid_article():
    """
        Test is_valid_article to confirm valid articles pass and invalid ones fail.
    """
    valid = {
        "title": "Example Article",
        "link": "https://example.com/news",
        "published": "2025-06-22",
    }
    invalids = [
        {},  # empty
        {"title": "", "link": "https://x.com", "published": "2025-06-22"},  # blank title
        {"title": "Title", "link": "badlink", "published": "2025-06-22"},  # invalid link
        {"title": "Title", "link": "http://valid.com", "published": "??"},  # invalid date
    ]

    assert is_valid_article(valid)
    for article in invalids:
        assert not is_valid_article(article)

"""
Integration test for CLI-based data processing in the News Aggregation System.

This test verifies the full processing pipeline triggered via the CLI:
- It mocks the raw input JSON files
- Executes the CLI with `--process`
- Asserts correct output, file creation, and data integrity

The test ensures that the CLI command performs deduplication, date normalization,
and filtering of invalid entries correctly, end-to-end.
"""

import os
import json
import subprocess
import pytest
import shutil

RAW_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../data_output/raw")
)
PROCESSED_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../data_output/processed/cleaned_articles.json"
    )
)


@pytest.fixture
def setup_raw_data():
    """
        Fixture to isolate the raw data environment for CLI processing tests.

        - Backs up existing raw article files.
        - Injects a temporary `aj.json` file containing test articles.
        - Cleans up test artifacts and restores original files after the test.
    """
    temp_backup = os.path.join(RAW_DIR, "tmp_backup")
    os.makedirs(temp_backup, exist_ok=True)

    for file in os.listdir(RAW_DIR):
        full_path = os.path.join(RAW_DIR, file)
        if file.endswith(".json"):
            shutil.move(full_path, os.path.join(temp_backup, file))

    os.makedirs(RAW_DIR, exist_ok=True)
    test_file = os.path.join(RAW_DIR, "aj.json")
    test_data = [
        {
            "title": "Integration Article",
            "link": "http://test.com/integration-1",
            "published": "2025-06-17",
            "category": "test",
        },
        {
            "title": "Duplicate Article",
            "link": "http://test.com/integration-1",
            "published": "invalid-date",
            "category": "test",
        },
    ]
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    yield

    # Clean up test file
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(PROCESSED_PATH):
        os.remove(PROCESSED_PATH)

    # Restore backup
    for file in os.listdir(temp_backup):
        shutil.move(os.path.join(temp_backup, file), os.path.join(RAW_DIR, file))
    os.rmdir(temp_backup)


def test_cli_process_command(setup_raw_data):
    """
        Integration test for CLI data processing command.

        - Invokes `main.py --process` via subprocess.
        - Asserts successful execution (exit code 0).
        - Checks for correct terminal output (includes '✅ Processed').
        - Verifies only valid, deduplicated article is written to processed JSON.
    """
    result = subprocess.run(
        ["python3", "main.py", "--process"],
        capture_output=True,
        text=True,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")),
    )

    assert result.returncode == 0
    assert "✅ Processed" in result.stdout

    assert os.path.exists(PROCESSED_PATH)
    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    assert isinstance(articles, list)
    assert len(articles) == 1
    assert articles[0]["title"] == "Integration Article"

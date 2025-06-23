"""
Module: exports.py
Description:
    Handles exporting of cleaned news article data into multiple formats including:
    - CSV
    - JSON
    - Excel (XLSX)

    Output files are saved under the data_output/exports directory.
"""

import os
import json
import pandas as pd
from src.analysis.trends import load_articles
from src.utils.logger import setup_logger

logger = setup_logger()

EXPORT_DIR = "data_output/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)


def export_cleaned_articles():
    """
    Export cleaned articles to CSV, JSON, and Excel formats.

    This function:
    - Loads cleaned article data from the processed JSON file.
    - Saves the data as:
        - CSV → data_output/exports/articles.csv
        - JSON → data_output/exports/articles.json
        - Excel → data_output/exports/articles.xlsx
    - Logs export success or error for each format.
    """
    logger.info("📤 Starting data export...")

    articles = load_articles()
    df = pd.DataFrame(articles)

    try:
        csv_path = os.path.join(EXPORT_DIR, "articles.csv")
        df.to_csv(csv_path, index=False)
        logger.info(f"✅ Exported CSV to {csv_path}")
    except Exception as e:
        logger.error(f"❌ Failed to export CSV: {e}")

    try:
        json_path = os.path.join(EXPORT_DIR, "articles.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Exported JSON to {json_path}")
    except Exception as e:
        logger.error(f"❌ Failed to export JSON: {e}")

    try:
        excel_path = os.path.join(EXPORT_DIR, "articles.xlsx")
        df.to_excel(excel_path, index=False)
        logger.info(f"✅ Exported Excel to {excel_path}")
    except Exception as e:
        logger.error(f"❌ Failed to export Excel: {e}")

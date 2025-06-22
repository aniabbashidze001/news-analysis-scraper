"""
report_generator.py

Generates an HTML summary report of cleaned news articles using Jinja2 templates.
Includes basic statistics and charts like publishing trends and category distribution.
"""

import os
import json
import time
from jinja2 import Environment, FileSystemLoader
import pandas as pd

REPORTS_DIR = "data_output/reports"
TEMPLATES_DIR = "src/templates"
PROCESSED_PATH = "data_output/processed/cleaned_articles.json"

os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_html_report():
    """
    Generate an HTML summary report of cleaned article data.

    - Loads cleaned articles from the processed JSON file.
    - Computes basic statistics:
        - Total articles
        - Article count by category
        - Top 5 publishing dates
    - Embeds charts (e.g., publishing trend, category distribution).
    - Renders the HTML using a Jinja2 template.
    - Saves the report to 'data_output/reports/summary_report.html'.
    """
    start = time.time()
    print("📄 Generating HTML report...", flush=True)

    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    df = pd.DataFrame(articles)[["title", "category", "published"]]

    total_articles = len(df)
    categories = df["category"].value_counts().to_dict()
    top_dates = df["published"].value_counts().nlargest(5).to_dict()

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("report_template.html")

    output = template.render(
        total_articles=total_articles,
        categories=categories,
        top_dates=top_dates,
        chart_paths=["publishing_trend.png", "articles_by_category.png"],
    )

    with open(f"{REPORTS_DIR}/summary_report.html", "w", encoding="utf-8") as f:
        f.write(output)

    print(f"✅ HTML report generated in {time.time() - start:.2f} seconds", flush=True)

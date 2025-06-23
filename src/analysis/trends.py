"""
trends.py

Performs trend analysis on cleaned news articles, including:
- Publishing activity over time
- Keyword frequency in titles
- Article distribution by category

Generates visual reports and data summaries stored in the reports directory.
"""

import json
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
import re

PROCESSED_PATH = "data_output/processed/cleaned_articles.json"
REPORTS_DIR = "data_output/reports"

os.makedirs(REPORTS_DIR, exist_ok=True)


def load_articles():
    """
    Load cleaned article data from the processed JSON file.

    Returns:
        list: A list of article dictionaries.
    """
    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_publishing_activity(articles):
    """
    Analyze and visualize article publishing frequency over time.

    Applies a 7-day moving average to smooth out trends and saves a line chart
    as 'publishing_trend.png' in the reports directory.

    Args:
        articles (list): List of article dictionaries with 'published' dates.
    """
    dates = []
    for a in articles:
        published = a.get("published", "")
        try:
            dt = datetime.fromisoformat(
                published.replace(" +02:00", "").replace(" +00:00", "")
            )
            dates.append(dt.date())
        except Exception:
            continue

    df = pd.DataFrame(dates, columns=["date"])
    trend = df["date"].value_counts().sort_index()
    trend.index = pd.to_datetime(trend.index)

    trend_smoothed = trend.rolling(window=7).mean()

    plt.figure(figsize=(14, 6))
    plt.plot(trend.index, trend_smoothed, color="dodgerblue", label="7-Day Moving Avg")
    plt.fill_between(trend.index, trend_smoothed, color="skyblue", alpha=0.3)

    plt.title("Articles Published per Date (Smoothed)")
    plt.xlabel("Date")
    plt.ylabel("Number of Articles")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/publishing_trend.png")
    plt.close()
    print("📊 Saved: publishing_trend.png")


def trend_top_keywords_in_titles(articles, top_n=10):
    """
    Identify and save the top N most frequent keywords from article titles.

    Filters out common stopwords and generates a CSV file with keyword counts.

    Args:
        articles (list): List of article dictionaries with 'title' fields.
        top_n (int): Number of top keywords to include in the CSV (default: 10).
    """
    print("\n🔍 Trend 2: Top Keywords in Article Titles")

    stopwords = set(
        [
            "the",
            "is",
            "on",
            "at",
            "to",
            "of",
            "and",
            "a",
            "in",
            "with",
            "as",
            "for",
            "from",
            "by",
            "an",
            "this",
            "that",
            "be",
            "are",
            "it",
            "its",
            "or",
            "we",
            "our",
            "but",
            "will",
            "not",
            "has",
            "have",
            "was",
            "you",
            "they",
            "about",
            "how",
            "who",
            "what",
            "when",
            "why",
            "which",
            "can",
            "all",
            "new",
            "more",
            "just",
            "their",
            "out",
        ]
    )

    word_counts = Counter()

    for article in articles:
        title = article.get("title", "")
        words = re.findall(r"\b[a-z]{3,}\b", title.lower())
        keywords = [word for word in words if word not in stopwords]
        word_counts.update(keywords)

    top_keywords = word_counts.most_common(top_n)

    # Save as CSV
    output_path = os.path.join(REPORTS_DIR, "top_keywords_titles.csv")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("keyword,count\n")
        for word, count in top_keywords:
            f.write(f"{word},{count}\n")

    print(f"📊 Saved: top_keywords_titles.csv")


def chart_articles_by_category(articles):
    """
    Generate a horizontal bar chart showing article counts by category.

    Saves the chart as 'articles_by_category.png' in the reports directory.

    Args:
        articles (list): List of article dictionaries with 'category' fields.
    """
    df = pd.DataFrame(articles)
    df["category"] = df["category"].fillna("Unknown")

    plt.figure(figsize=(8, 5))
    df["category"].value_counts().plot(kind="barh", color="lightgreen")
    plt.title("Articles by Category")
    plt.xlabel("Count")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, "articles_by_category.png"))
    print("📊 Saved: articles_by_category.png")


def run_full_analysis():
    """
    Execute the full trend analysis pipeline:
    - Publishing trend
    - Top title keywords
    - Category distribution

    Saves all visualizations and prints progress status to the console.
    """
    articles = load_articles()
    analyze_publishing_activity(articles)
    trend_top_keywords_in_titles(articles)
    chart_articles_by_category(articles)
    print("✅ Full analysis complete.")

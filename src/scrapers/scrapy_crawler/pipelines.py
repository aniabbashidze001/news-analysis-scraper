"""
Scrapy pipeline to collect scraped articles and export them to a JSON file.

This pipeline accumulates all scraped items into a list and writes them to
`data_output/raw/theverge_articles.json` when the spider finishes.
"""

import json
import os


class JsonAndCsvExportPipeline:
    """
        Pipeline that exports all scraped articles to a single JSON file.

        Methods:
            open_spider(spider): Initializes resources before scraping starts.
            close_spider(spider): Writes collected articles to JSON when scraping ends.
            process_item(item, spider): Adds each scraped item to the export list.
    """
    def open_spider(self, spider):
        os.makedirs("data_output/raw", exist_ok=True)
        self.articles = []
        self.json_file = open(
            "data_output/raw/theverge_articles.json", "w", encoding="utf-8"
        )

    def close_spider(self, spider):
        json.dump(self.articles, self.json_file, indent=2, ensure_ascii=False)
        self.json_file.close()

    def process_item(self, item, spider):
        self.articles.append(dict(item))
        return item

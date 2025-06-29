"""
Scrapy settings for the 'scrapy_crawler' project.

This configuration file defines behavior for the generic news spider, including:
- Spider modules and user-agent headers
- Retry strategy and timeout handling
- Pipeline configuration for exporting scraped data

Used by the GenericNewsSpider to crawl and extract articles from The Verge.
"""


BOT_NAME = "scrapy_crawler"
SPIDER_MODULES = ["src.scrapers.scrapy_crawler"]
NEWSPIDER_MODULE = "src.scrapers.scrapy_crawler"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)

RETRY_ENABLED = True
DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 10
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

ITEM_PIPELINES = {
    "src.scrapers.scrapy_crawler.pipelines.JsonAndCsvExportPipeline": 1,
}

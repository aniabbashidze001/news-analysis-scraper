"""
Scrapy spider for crawling news articles from The Verge.

This spider navigates through paginated news archive pages and extracts
article details such as title, link, category, and publication date.
"""

import scrapy
from src.scrapers.scrapy_crawler.items import NewsArticle


class GenericNewsSpider(scrapy.Spider):
    """
        Scrapy spider to extract news article metadata from The Verge.

        Attributes:
            name (str): Identifier for the spider.
            allowed_domains (list): Domains the spider is allowed to crawl.
            start_urls (list): Initial URL(s) to start crawling from.

        Methods:
            parse(response): Extracts article links and handles pagination.
            parse_article(response): Extracts article publish date from individual pages.
    """

    name = "generic_news_spider"
    allowed_domains = ["theverge.com"]
    start_urls = ["https://www.theverge.com/news/archives/1"]

    def parse(self, response):
        self.logger.info(f"📄 Parsing page: {response.url} (status: {response.status})")

        if response.status == 404:
            self.logger.info("❌ Reached 404 — stopping pagination.")
            return

        articles = response.css("a.yy0d3l8")

        if not articles:
            self.logger.info("ℹ️ No more articles found — stopping.")
            return

        self.logger.debug(f"🔗 Found {len(articles)} article links on {response.url}")

        for article in articles:
            title = article.css("::attr(aria-label)").get()
            link = article.css("::attr(href)").get()

            if link:
                full_url = response.urljoin(link)
                self.logger.debug(
                    f"📰 Queuing article: {title[:50] if title else 'N/A'} | {full_url}"
                )

                item = NewsArticle()
                item["title"] = title.strip() if title else "N/A"
                item["link"] = full_url
                item["category"] = "news"

                yield response.follow(
                    full_url, callback=self.parse_article, meta={"item": item}
                )

        # Pagination logic only if URL is in /archives/<n> format
        if "archives" in response.url:
            try:
                current_page = int(response.url.rstrip("/").split("/")[-1])
                next_page = current_page + 1
                next_url = f"https://www.theverge.com/news/archives/{next_page}"
                self.logger.info(f"➡️ Moving to next page: {next_url}")
                yield scrapy.Request(next_url, callback=self.parse)
            except ValueError:
                self.logger.warning(
                    f"⚠️ Could not extract current page from URL: {response.url}"
                )

    def parse_article(self, response):
        item = response.meta["item"]
        try:
            publish_date = response.css("time::attr(datetime)").get()
            item["published"] = publish_date.strip() if publish_date else "N/A"
            self.logger.debug(
                f"✅ Parsed article: {item['title'][:50]} | Published: {item['published']}"
            )
        except Exception as e:
            self.logger.warning(
                f"⚠️ Failed to extract publish date from {response.url}: {e}"
            )
            item["published"] = "N/A"

        yield item

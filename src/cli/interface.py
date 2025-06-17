import argparse
from src.utils.logger import setup_logger

logger = setup_logger()

def run_cli():
    parser = argparse.ArgumentParser(
        description="News Aggregation & Analysis CLI Tool"
    )

    parser.add_argument('--run-static', action='store_true', help='Run static scrapers')
    parser.add_argument('--run-dynamic', action='store_true', help='Run dynamic scrapers')
    parser.add_argument('--run-scrapy', action='store_true', help='Run Scrapy crawler')
    parser.add_argument('--process', action='store_true', help='Process raw data')
    parser.add_argument('--generate-report', action='store_true', help='Generate reports')

    args = parser.parse_args()

    if args.run_static:
        logger.info("Running static scrapers...")
        # from src.scrapers.static_scraper import run_static_scrapers
        # run_static_scrapers()

    if args.run_dynamic:
        logger.info("Running dynamic scrapers...")
        from src.scrapers.selenium_scraper import run_dynamic_scrapers
        run_dynamic_scrapers()

    if args.run_scrapy:
        logger.info("Running Scrapy crawler...")
        # use os.system to run `scrapy crawl` command

    if args.process:
        logger.info("Processing and cleaning data...")
        # from src.data.processors import process_data
        # process_data()

    if args.generate_report:
        logger.info("Generating reports...")
        # from src.analysis.reports import generate_report
        # generate_report()

    if not any(vars(args).values()):
        parser.print_help()

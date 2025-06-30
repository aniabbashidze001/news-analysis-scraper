"""
interface.py

This module defines the command-line interface (CLI) and interactive menu for the News Aggregation & Analysis System.
It provides options to run various scrapers, process and analyze the data, export results, and generate reports.

Modules:
- run_cli(): Parses CLI arguments and triggers the corresponding commands.
- run_interactive_cli(): Displays an interactive menu for users to execute actions step-by-step.

Usage:
    python main.py --run-static
"""

from src.utils.logger import setup_logger
from src.data.database import create_table
from src.scrapers.selenium_scraper import test_form_submission
import argparse

# Initialize
create_table()
logger = setup_logger()


def run_cli():
    """
        Parses command-line arguments and executes the selected data scraping or processing commands.

        Available commands:
        --run-static     Run the BeautifulSoup-based static scraper (NPR)
        --run-dynamic    Run the Selenium-based dynamic scraper (Euronews)
        --run-scrapy     Run the Scrapy spider (The Verge)
        --process        Clean and validate raw scraped data, then store it in the database
        --analyze        Run statistical and trend analysis with charts
        --export         Export cleaned data to CSV, Excel, and JSON formats
        --report         Generate HTML summary report with visualizations
        --test-form      Execute a test form submission to validate scraping with form interactions

        This function also ensures appropriate logging and fallback help display when no command is provided.
    """
    logger.info("🧭 CLI tool started...")
    parser = argparse.ArgumentParser(
        description="📰 News Aggregation & Analysis CLI Tool"
    )

    parser.add_argument("--run-static", action="store_true", help="Run static scrapers")
    parser.add_argument(
        "--run-dynamic", action="store_true", help="Run dynamic scrapers"
    )
    parser.add_argument("--run-scrapy", action="store_true", help="Run Scrapy crawler")
    parser.add_argument(
        "--process", action="store_true", help="Process & clean up raw data and save to DB"
    )
    parser.add_argument(
        "--analyze", action="store_true", help="Generate trends, charts, keyword stats"
    )
    parser.add_argument(
        "--export", action="store_true", help="Save cleaned data in CSV/Excel/JSON"
    )
    parser.add_argument("--report", action="store_true", help="Generate HTML report")
    parser.add_argument(
        "--test-form", action="store_true", help="Run test form submission"
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Run interactive CLI menu"
    )

    args = parser.parse_args()

    any_command_run = False

    if args.run_static:
        logger.info("Running static scrapers...")
        from src.factories.scraper_factory import get_scraper

        scraper = get_scraper("static")
        scraper.run()
        any_command_run = True

    if args.run_dynamic:
        logger.info("Running dynamic scrapers...")
        from src.factories.scraper_factory import get_scraper

        scraper = get_scraper("dynamic")
        scraper.run()
        any_command_run = True

    if args.run_scrapy:
        logger.info("🕷️ Running Scrapy crawler...")
        from src.factories.scraper_factory import get_scraper

        scraper = get_scraper("scrapy")
        scraper.run()
        any_command_run = True

    if args.process:
        logger.info("⚙️ Command triggered: --process (clean + insert)")
        from src.data.processors import process_and_save_all_articles

        process_and_save_all_articles()
        print("✅ Processed and saved cleaned articles.")
        any_command_run = True

    if args.analyze:
        logger.info("📊 Command triggered: analyze")
        from src.analysis.trends import run_full_analysis

        run_full_analysis()
        any_command_run = True

    if args.export:
        logger.info("⚙️ Command triggered: export")
        from src.analysis.export import export_cleaned_articles

        export_cleaned_articles()
        any_command_run = True

    if args.report:
        logger.info("⚙️ Command triggered: report")
        from src.analysis.report_generator import generate_html_report

        generate_html_report()
        any_command_run = True

    if args.test_form:
        logger.info("⚙️ Command triggered: test-form")
        test_form_submission()
        any_command_run = True

    if not any_command_run:
        logger.info("ℹ️ No valid command provided. Showing help.")
        parser.print_help()


def run_interactive_cli():
    """
        Launches an interactive CLI menu for users to perform all available tasks step-by-step.

        Users can select from options to:
        1. Run static scraper (NPR)
        2. Run dynamic scraper (Euronews)
        3. Run Scrapy crawler (The Verge)
        4. Clean and store scraped articles
        5. Run full trend analysis
        6. Export results in multiple formats
        7. Generate a summary HTML report
        8. Test form submission interaction
        9. Quit the menu

        Each option provides feedback and log instructions, and returns the user to the menu until exited.
    """
    from src.factories.scraper_factory import get_scraper
    from src.data.processors import process_and_save_all_articles
    from src.analysis.trends import (
        run_full_analysis,
    )
    from src.analysis.report_generator import generate_html_report
    from src.analysis.export import export_cleaned_articles
    from src.scrapers.selenium_scraper import test_form_submission

    while True:
        print("\n🧠 Interactive CLI Menu:")
        print("1️⃣  Run Static Scraper")
        print("2️⃣  Run Dynamic Scraper")
        print("3️⃣  Run Scrapy Crawler")
        print("4️⃣  Process, Clean & Save Articles to DB")
        print("5️⃣  Run Full Trend Analysis")
        print("6️⃣  Export Cleaned Data (CSV, Excel, JSON)")
        print("7️⃣  Generate HTML Report")
        print("8️⃣  Test Form Submission")
        print("9️⃣  Quit")

        choice = input("👉 Select an option (1–10): ")

        if choice == "1":
            scraper = get_scraper("static")
            scraper.run()
            print("🕐 Running Static Scraper (NPR)...")
            print("📜 Check logs for real-time progress.")
            print("📁 Check: data_output/raw/npr_static.json")
            input("🔁 Press Enter to return to the menu...")
        elif choice == "2":
            scraper = get_scraper("dynamic")
            scraper.run()
            print("🕐 Running Dynamic Selenium Scraper (Euronews)...")
            print("📜 Check logs for real-time progress.")
            print("📁 Check: data_output/raw/euronews_dynamic.json")
            input("🔁 Press Enter to return to the menu...")
        elif choice == "3":
            scraper = get_scraper("scrapy")
            scraper.run()
            print("🕐 Running Scrapy Crawler (The Verge)...")
            print("📜 Check logs for real-time progress.")
            print("📁 Check: data_output/raw/theverge_articles.json")
            input("🔁 Press Enter to return to the menu...")
        elif choice == "4":
            process_and_save_all_articles()
            print("✅ Articles processed, cleaned, and saved to the SQLite database!")
            print(
                "📁 Check: data_output/processed/cleaned_articles.json and data_output/news_articles.db"
            )
            input("🔁 Press Enter to return to the menu...")
        elif choice == "5":
            run_full_analysis()
            print("📊 Trend analysis complete!")
            print("📁 Charts saved in: data_output/reports/")
            input("🔁 Press Enter to return to the menu...")
        elif choice == "6":
            export_cleaned_articles()
            print("✅ Data exported successfully!")
            print("📁 Check: data_output/exports/ for CSV, Excel, and JSON files.")
            input("🔁 Press Enter to return to the menu...")
        elif choice == "7":
            generate_html_report()
            print("📰 HTML report generated successfully!")
            print("📁 Check: data_output/reports/summary_report.html")
            input("🔁 Press Enter to return to the menu...")
        elif choice == "8":
            test_form_submission()
            print(
                "📨 Test form submission complete! Check terminal logs for success or error details."
            )
            input("🔁 Press Enter to return to the menu...")
        elif choice == "9":
            print("👋 Exiting interactive CLI. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please choose a number from 1 to 10.")
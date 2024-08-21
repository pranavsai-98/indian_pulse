import asyncio
from scrapers.url_scraper import scrape_all_states
from processors.url_processor import process_urls
from scrapers.content_scraper import scrape_content
from processors.content_processor import process_and_save_content
import json


async def main():
    print("Step 1: Scraping URLs for all states")
    all_states_data = scrape_all_states()
    with open('all_states_news_urls.json', 'w') as f:
        json.dump(all_states_data, f, indent=2)
    print("URLs for all states have been saved to all_states_news_urls.json")

    print("\nStep 2: Processing and filtering URLs")
    process_urls()

    print("\nStep 3: Scraping content for filtered URLs")
    await scrape_content()

    print("\nStep 4: Processing and saving final content")
    process_and_save_content(
        'all_states_news_output.json', 'processed_news_output.json')

    print("\nAll steps completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())

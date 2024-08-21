import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, Union, List
from aiolimiter import AsyncLimiter
import aiofiles
from config import (
    MAX_CONCURRENT_REQUESTS, RATE_LIMIT, MAX_RETRIES,
    CACHE_SIZE, INPUT_FILE, OUTPUT_FILE, GRAPH_CONFIG,
    SUMMARY_SENTENCES, CATEGORIES
)
from utils.helpers import clean_text, parse_json_safely
from scrapegraphai.graphs import SmartScraperGraph
import backoff

limiter = AsyncLimiter(RATE_LIMIT, 1)


@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=MAX_RETRIES)
async def fetch_url(url: str) -> str:
    async with limiter:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()


async def process_article(url: str) -> Union[Dict, None]:
    try:
        html_content = await fetch_url(url)
        soup = BeautifulSoup(html_content, 'html.parser')

        article_content = soup.find('div', class_='okf2Z') or soup.find(
            'div', class_='_s30J clearfix')
        article_text = clean_text(article_content.get_text(
            strip=True)) if article_content else "Article content not found"

        main_image = soup.find('div', class_='wJnIp') or soup.find(
            'div', class_='uKfQS')
        image_url = main_image.find('img').get(
            'src') if main_image and main_image.find('img') else "Image not found"

        headline = soup.find('h1', class_='HNMDR') or soup.find(
            'h1', class_='_23498')
        headline_text = clean_text(
            headline.text) if headline else "Headline not found"

        pub_date = soup.find('div', class_='xf8Pm') or soup.find(
            'div', class_='byp7W')
        pub_date_text = clean_text(
            pub_date.text) if pub_date else "Published date not found"

        extracted_info = {
            "headline": headline_text,
            "published_date": pub_date_text,
            "main_content": article_text,
            "main_image_url": image_url,
            "url": url
        }

        smart_scraper_graph = SmartScraperGraph(
            prompt=f"""Analyze the provided news article information. Extract the complete main content of the news,
            ignoring any advertisements or irrelevant content like polls, or 'you may like' articles.
            Provide a structured output with the following fields:
            1. Headline
            2. Published Date
            3. Main Content (complete, not summarized)
            4. Main Image URL
            5. Summary ({SUMMARY_SENTENCES} sentences)
            6. News Rating (on a scale of 1-10, where 1 is extremely bad news and 10 is the best news possible)
            7. Category (choose the most appropriate category from the following list: {', '.join(CATEGORIES)})

            Base your rating on the current situation in India and the impact of the news.
            For the category, choose the one that best fits the main focus of the article.

            IMPORTANT: Your output must be a valid JSON object. Do not include any text before or after the JSON object.
            """,
            source=json.dumps(extracted_info),
            config=GRAPH_CONFIG
        )

        result = smart_scraper_graph.run()

        if isinstance(result, dict):
            return result
        elif isinstance(result, str):
            return parse_json_safely(result)
        else:
            print(f"Unexpected result type for {url}: {type(result)}")
            return None

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None


async def process_articles(urls: List[str]) -> List[Dict]:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async def bounded_process_article(url):
        async with semaphore:
            return await process_article(url)

    return await asyncio.gather(*[bounded_process_article(url) for url in urls])


async def process_state(state: str, urls: List[str]) -> Dict:
    print(f"Processing {state}...")
    results = await process_articles(urls)
    valid_results = [r for r in results if r is not None and "error" not in r]
    return {
        "state": state,
        "articles": valid_results
    }


async def scrape_content():
    async with aiofiles.open(INPUT_FILE, mode='r') as file:
        content = await file.read()
        all_urls = json.loads(content)

    tasks = [process_state(state, urls) for state, urls in all_urls.items()]
    state_results = await asyncio.gather(*tasks)

    output = {
        state_result["state"]: state_result["articles"]
        for state_result in state_results
        if state_result["articles"]
    }

    async with aiofiles.open(OUTPUT_FILE, mode='w') as file:
        await file.write(json.dumps(output, indent=4))

    print(f"Processing complete. Output saved to {OUTPUT_FILE}")
    print_summary(output)


def print_summary(output: Dict):
    total_articles = sum(len(articles) for articles in output.values())
    print(f"Total valid articles processed: {total_articles}")
    print("Articles per state:")
    for state, articles in output.items():
        print(f"  {state}: {len(articles)}")


if __name__ == "__main__":
    asyncio.run(scrape_content())

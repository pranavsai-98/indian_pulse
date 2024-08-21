import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INPUT_FILE = "filtered_state_news_urls.json"
OUTPUT_FILE = "all_states_news_output.json"
STATE_IMPORTANCE_FILE = "state_importance.json"
INDIA_NEWS_URLS_FILE = "india_news_urls.json"

MAX_CONCURRENT_REQUESTS = 20
RATE_LIMIT = 10
CACHE_SIZE = 1000
MAX_RETRIES = 3
SUMMARY_SENTENCES = 2

CATEGORIES = [
    "Politics", "Economy", "Technology", "Health",
    "Environment", "Society", "Sports"
]

GRAPH_CONFIG = {
    "llm": {
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "model": "gpt-4o-mini",
    },
    "verbose": False,
    "headless": False,
}

import json
from typing import Dict, List
from models import Article, StateNews, AllStateNews


def process_content(raw_content: Dict[str, List[Dict]]) -> AllStateNews:
    processed_content = {}
    for state, articles in raw_content.items():
        processed_articles = []
        for article in articles:
            processed_article = Article(
                headline=article['Headline'],
                published_date=article['Published Date'],
                main_content=article['Main Content'],
                main_image_url=article['Main Image URL'],
                url=article['url'],
                summary=article['Summary'],
                news_rating=article['News Rating'],
                category=article['Category']
            )
            processed_articles.append(processed_article)
        processed_content[state] = processed_articles
    return AllStateNews(__root__=processed_content)


def load_raw_content(file_path: str) -> Dict[str, List[Dict]]:
    with open(file_path, 'r') as f:
        return json.load(f)


def save_processed_content(processed_content: AllStateNews, file_path: str):
    with open(file_path, 'w') as f:
        json.dump(processed_content.dict(), f, indent=2)


def process_and_save_content(input_file: str, output_file: str):
    raw_content = load_raw_content(input_file)
    processed_content = process_content(raw_content)
    save_processed_content(processed_content, output_file)
    print(f"Processed content saved to {output_file}")


if __name__ == "__main__":
    process_and_save_content(
        'all_states_news_output.json', 'processed_news_output.json')

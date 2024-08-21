import json
from typing import List, Dict
from openai import OpenAI
import re
from config import OPENAI_API_KEY, STATE_IMPORTANCE_FILE

client = OpenAI(api_key=OPENAI_API_KEY)


def load_urls(file_path: str) -> Dict[str, Dict[str, List[str]]]:
    print(f"Loading URLs from {file_path}")
    with open(file_path, 'r') as f:
        urls = json.load(f)
    print(f"Loaded {len(urls)} states")
    return urls


def load_state_importance(file_path: str) -> Dict[str, List[str]]:
    print(f"Loading state importance from {file_path}")
    with open(file_path, 'r') as f:
        importance = json.load(f)
    print(f"Loaded importance for {sum(len(v)
          for v in importance.values())} states")
    return importance


def filter_state_specific_urls(state: str, urls: List[str]) -> List[str]:
    print(f"\nFiltering URLs for {state}")
    print(f"Input URLs: {len(urls)}")
    if not urls:
        print("No URLs to filter")
        return []

    chunk_size = 20
    url_chunks = [urls[i:i + chunk_size]
                  for i in range(0, len(urls), chunk_size)]
    filtered_urls = []

    for chunk in url_chunks:
        prompt = f"""You are an AI assistant tasked with filtering news article URLs that are specifically related to {state}, India.
        Consider the following:
        1. The URL may contain the state name, or names of cities, districts, or regions within {state}.
        2. The article might be about an event, person, or issue specifically related to {state}.
        3. Be aware of similarly named places in other states and don't confuse them.
        4. If unsure, err on the side of exclusion to ensure relevance.

        For each URL, respond with only 'Yes' if it's related to {state}, or 'No' if it's not. Provide your answers as a comma-separated list.

        URLs to evaluate:
        {', '.join(chunk)}
        """

        print(f"Sending prompt to OpenAI (length: {len(prompt)})")
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt}
                ]
            )

            results = response.choices[0].message.content.strip().split(',')
            print(f"Received {len(results)} results from OpenAI")

            if len(results) != len(chunk):
                print(f"Warning: Mismatch in filtering results for {state}.")
                print(f"Expected {len(chunk)} results, got {len(results)}")
                print("OpenAI response:")
                print(response.choices[0].message.content.strip())
                results = results[:len(chunk)]

            chunk_filtered_urls = [url for url, result in zip(
                chunk, results) if result.strip().lower() == 'yes']
            filtered_urls.extend(chunk_filtered_urls)

        except Exception as e:
            print(f"Error filtering URLs for {state}: {e}")
            continue

    print(f"Filtered URLs: {len(filtered_urls)}")
    return filtered_urls


def rank_urls(state: str, urls: List[str], max_urls: int) -> List[str]:
    print(f"\nRanking URLs for {state}")
    print(f"Input URLs: {len(urls)}, Max URLs: {max_urls}")
    if not urls:
        print("No URLs to rank")
        return []

    prompt = f"""You are an AI assistant tasked with ranking news articles about {state} based on their URLs.
    Consider the following factors when ranking:
    1. Relevance to {state}
    2. National importance
    3. Impact on society or economy
    4. Relevance to current events
    5. Uniqueness of the story

    Rank the following URLs in order of importance (most important first). Provide the ranking as a comma-separated list of numbers corresponding to the order of URLs provided.

    URLs:
    {', '.join(urls)}
    """

    print(f"Sending prompt to OpenAI (length: {len(prompt)})")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )

        ranking_str = response.choices[0].message.content.strip()
        print(f"Received ranking from OpenAI: {ranking_str}")
        ranking = [int(x) for x in re.findall(r'\d+', ranking_str)]

        if len(ranking) != len(urls):
            print(f"Warning: Ranking mismatch for {state}.")
            print(f"Expected {len(urls)} rankings, got {len(ranking)}")
            print("Using original order")
            return urls[:max_urls]

        ranked_urls = [urls[i-1] for i in ranking if 1 <= i <= len(urls)]
        print(f"Ranked URLs: {len(ranked_urls)}")
        return ranked_urls[:max_urls]

    except Exception as e:
        print(f"Error ranking URLs for {state}: {e}")
        return urls[:max_urls]


def filter_urls_by_importance(urls: Dict[str, Dict[str, List[str]]], state_importance: Dict[str, List[str]]) -> Dict[str, List[str]]:
    filtered_urls = {}

    for state, sections in urls.items():
        print(f"\nProcessing {state}")
        all_urls = []
        for section, section_urls in sections.items():
            print(f"  Section {section}: {len(section_urls)} URLs")
            all_urls.extend(section_urls)
        print(f"Total URLs for {state}: {len(all_urls)}")

        state_specific_urls = filter_state_specific_urls(state, all_urls)

        if state in state_importance['high']:
            max_urls = 15
            print(f"{state} is high importance")
        elif state in state_importance['medium']:
            max_urls = 7
            print(f"{state} is medium importance")
        else:
            max_urls = 3
            print(f"{state} is low importance")

        if state_specific_urls:
            filtered_urls[state] = rank_urls(
                state, state_specific_urls, max_urls)
        else:
            filtered_urls[state] = []
        print(f"Final URLs for {state}: {len(filtered_urls[state])}")

    return filtered_urls


def process_urls():
    urls = load_urls('all_states_news_urls.json')
    state_importance = load_state_importance(STATE_IMPORTANCE_FILE)
    filtered_urls = filter_urls_by_importance(urls, state_importance)

    print("\nSaving results")
    with open('filtered_state_news_urls.json', 'w') as f:
        json.dump(filtered_urls, f, indent=2)

    print("Filtered URLs have been saved to filtered_state_news_urls.json")
    print(f"Total states processed: {len(filtered_urls)}")
    print(f"Total URLs in result: {sum(len(urls)
          for urls in filtered_urls.values())}")


if __name__ == "__main__":
    process_urls()

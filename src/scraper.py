
import requests
from bs4 import BeautifulSoup
import os
import random
import json
import datetime

root = os.path.dirname(os.path.abspath('scraper.py'))

# RSS feed URLs for different news categories
TOP_NEWS_URL = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"
WORLD_NEWS_URL = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362"
US_NEWS_URL = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15837362"
ECONOMIC_NEWS_URL = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258"
TECHNOLOGY_NEWS_URL = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910"
POLITICS_NEWS_URL = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000113"


def _fetch_news_from_url(url, news_type, max_items=3):
    """
    Internal helper function to fetch news from a specific RSS feed URL.

    Args:
        url (str): The RSS feed URL to fetch news from
        news_type (str): The category/type of news (e.g., "Top News", "World News")
        max_items (int): Maximum number of news items to fetch (default: 3)

    Returns:
        list: A list of news items, where each item is [title, description, news_type]
    """
    news_items = []
    try:
        print(f"Fetching {news_type}...")
        raw = requests.get(url)
        soup = BeautifulSoup(raw.text, 'xml')
        news_list = soup.find_all('item')

        for i, item in enumerate(news_list):
            if i >= max_items:
                break
            title = item.find('title').text
            description = item.find('description').text
            news_items.append([title, description, news_type])
    except Exception as e:
        print(f"Error fetching {news_type}: {e}")

    return news_items


def _deduplicate_news(news_list):
    """
    Remove duplicate news items based on title and description.

    Args:
        news_list (list): List of news items to deduplicate

    Returns:
        list: Deduplicated list of news items
    """
    news_dedup = []
    seen = set()

    for news_item in news_list:
        title = news_item[0]
        description = news_item[1]
        # Create a unique key from title and description
        key = (title, description)

        if key not in seen:
            seen.add(key)
            news_dedup.append(news_item)

    return news_dedup


def get_top_news(max_items=3):
    """
    Fetch top news stories from CNBC.

    Args:
        max_items (int): Maximum number of news items to fetch (default: 3)

    Returns:
        list: A list of news items, where each item is [title, description, news_type]
    """
    return _fetch_news_from_url(TOP_NEWS_URL, "Top News", max_items)


def get_world_news(max_items=3):
    """
    Fetch world news stories from CNBC.

    Args:
        max_items (int): Maximum number of news items to fetch (default: 3)

    Returns:
        list: A list of news items, where each item is [title, description, news_type]
    """
    return _fetch_news_from_url(WORLD_NEWS_URL, "World News", max_items)


def get_us_news(max_items=3):
    """
    Fetch US news stories from CNBC.

    Args:
        max_items (int): Maximum number of news items to fetch (default: 3)

    Returns:
        list: A list of news items, where each item is [title, description, news_type]
    """
    return _fetch_news_from_url(US_NEWS_URL, "US News", max_items)


def get_economic_news(max_items=3):
    """
    Fetch economic news stories from CNBC.

    Args:
        max_items (int): Maximum number of news items to fetch (default: 3)

    Returns:
        list: A list of news items, where each item is [title, description, news_type]
    """
    return _fetch_news_from_url(ECONOMIC_NEWS_URL, "Economic News", max_items)


def get_technology_news(max_items=3):
    """
    Fetch technology news stories from CNBC.

    Args:
        max_items (int): Maximum number of news items to fetch (default: 3)

    Returns:
        list: A list of news items, where each item is [title, description, news_type]
    """
    return _fetch_news_from_url(TECHNOLOGY_NEWS_URL, "Technology News", max_items)


def get_politics_news(max_items=3):
    """
    Fetch politics news stories from CNBC.

    Args:
        max_items (int): Maximum number of news items to fetch (default: 3)

    Returns:
        list: A list of news items, where each item is [title, description, news_type]
    """
    return _fetch_news_from_url(POLITICS_NEWS_URL, "Politics News", max_items)


def get_all_news(max_items=6):
    """
    Fetch all news from all categories and deduplicate them.

    Args:
        max_items (int): Maximum number of news items to fetch per category (default: 3)

    Returns:
        list: A deduplicated list of all news items from all categories
    """
    all_news = []

    # Fetch news from all categories
    all_news.extend(get_top_news(max_items))
    all_news.extend(get_world_news(max_items))
    all_news.extend(get_us_news(max_items))
    all_news.extend(get_economic_news(max_items))
    all_news.extend(get_technology_news(max_items))
    all_news.extend(get_politics_news(max_items))

    # Deduplicate the combined news list
    return _deduplicate_news(all_news)


def choose_random_news(max_items=3):
    """
    Select a random news item from all available news.

    Args:
        max_items (int): Maximum number of news items to fetch per category (default: 3)

    Returns:
        list: A single random news item as [title, description, news_type]
    """
    all_news = get_all_news(max_items)
    if all_news:
        return random.choice(all_news)
    return None


def save_news_to_file(news_data, filename='all_news.json'):
    """
    Save news data to a JSON file in a date-organized directory structure.

    Args:
        news_data (list): List of news items to save
        filename (str): Name of the JSON file (default: 'all_news.json')

    Returns:
        str: Path to the saved file
    """
    # Get current date
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Create data directory for the current date
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, 'data', date)
    os.makedirs(data_dir, exist_ok=True)

    # Convert news data to a more structured JSON format
    news_json = {
        "date": date,
        "total_items": len(news_data),
        "news": [
            {
                "title": item[0],
                "description": item[1],
                "category": item[2]
            }
            for item in news_data
        ]
    }

    # Save the JSON file
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'w') as f:
        json.dump(news_json, f, indent=4)

    print(f"Saved {len(news_data)} news items to {file_path}")
    return file_path




if __name__ == '__main__':
    # Example: Get all news (deduplicated)
    print("=== Getting All News (Deduplicated) ===")
    all_news = get_all_news()
    print(f"Total news items: {len(all_news)}\n")

    # Save all news to file
    save_news_to_file(all_news, 'all_news.json')

    # Example: Get specific category news
    print("\n=== Getting Top News Only ===")
    top_news = get_top_news()
    for item in top_news:
        print(f"Title: {item[0]}")
        print(f"Type: {item[2]}\n")

    # Save top news to separate file
    save_news_to_file(top_news, 'top_news.json')

    # Example: Get a random news item
    print("\n=== Random News Item ===")
    random_news = choose_random_news()
    if random_news:
        print(f"Title: {random_news[0]}")
        print(f"Description: {random_news[1]}")
        print(f"Type: {random_news[2]}")

        # Save random news to file
        save_news_to_file([random_news], 'random_news.json')






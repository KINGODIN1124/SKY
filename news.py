import requests
from config import NEWS_API_KEY

def get_latest_news(query="general", country="us"):
    """
    Get latest news using NewsData.io API.
    """
    if not NEWS_API_KEY:
        return "News API key not configured. Please set NEWS_API_KEY in .env."

    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={query}&country=in&language=en"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and data.get('results'):
            headlines = [article['title'] for article in data['results'][:5]]
            return "Latest News:\n" + "\n".join(f"- {headline}" for headline in headlines)
        else:
            return "No news found or API limit reached."
    except Exception as e:
        return f"Error fetching news: {e}"

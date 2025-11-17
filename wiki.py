import wikipediaapi

def get_wikipedia_summary(topic):
    """
    Fetch Wikipedia summary for a topic.
    """
    try:
        wiki_wiki = wikipediaapi.Wikipedia(user_agent='SKY-AI-Assistant/1.0 (vibhumishra@example.com)', language='en')
        page = wiki_wiki.page(topic)
        if page.exists():
            return page.summary[:500] + "..."  # Limit to 500 chars
        else:
            return f"No Wikipedia page found for '{topic}'."
    except Exception as e:
        return f"Error fetching Wikipedia summary: {e}"

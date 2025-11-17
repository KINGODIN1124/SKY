import requests

def get_sports_scores():
    """
    Fetch latest sports scores from a free API (placeholder: using ESPN API or similar).
    Note: This is a placeholder; real implementation may require API key.
    """
    try:
        # Placeholder URL; replace with actual free sports API
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
        response = requests.get(url)
        data = response.json()
        if 'events' in data:
            scores = []
            for event in data['events'][:5]:  # Limit to 5
                home = event['competitions'][0]['competitors'][0]['team']['displayName']
                away = event['competitions'][0]['competitors'][1]['team']['displayName']
                home_score = event['competitions'][0]['competitors'][0].get('score', 'N/A')
                away_score = event['competitions'][0]['competitors'][1].get('score', 'N/A')
                scores.append(f"{home} {home_score} - {away_score} {away}")
            return "Latest soccer scores:\n" + "\n".join(scores)
        else:
            return "No recent sports scores available."
    except Exception as e:
        return f"Error fetching sports scores: {e}"

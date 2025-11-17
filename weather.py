import requests

def get_weather(city=None):
    """
    Get current weather for a city using a free weather API (no key required).
    Using WeatherAPI as OpenWeatherMap key is invalid.
    """
    if not city:
        city, country = detect_location()
        if not city:
            city = "Kanpur"  # Default fallback
    else:
        country = "India"  # Assume India if city specified

    # Using WeatherAPI with provided key
    url = f"http://api.weatherapi.com/v1/current.json?key=3dc9c0976df746d786882245251711&q={city}&aqi=no"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data['current']['temp_c']
            description = data['current']['condition']['text']
            humidity = data['current']['humidity']
            return f"Weather in {city}: {temp}°C, {description}, Humidity: {humidity}%"
        else:
            return f"Weather data not found for {city}. Error: {data.get('error', {}).get('message', 'Unknown error')}."
    except Exception as e:
        return f"Error fetching weather: {e}"

def detect_location():
    """
    Detect user's location using IP geolocation.
    """
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data['status'] == 'success':
            return data['city'], data['country']
        else:
            return "Kanpur", "India"  # Default fallback
    except Exception as e:
        return "Kanpur", "India"  # Default fallback

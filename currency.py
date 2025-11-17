import requests

def get_exchange_rate(from_currency, to_currency):
    """
    Fetch exchange rate using exchangerate-api.com (free tier).
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url)
        data = response.json()
        if 'rates' in data and to_currency.upper() in data['rates']:
            rate = data['rates'][to_currency.upper()]
            return f"1 {from_currency.upper()} = {rate} {to_currency.upper()}"
        else:
            return f"Exchange rate for {from_currency} to {to_currency} not found."
    except Exception as e:
        return f"Error fetching exchange rate: {e}"

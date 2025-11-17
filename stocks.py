import yfinance as yf

def get_stock_price(symbol):
    """
    Fetch real-time stock price for a given symbol.
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        price = info.get('regularMarketPrice', 'N/A')
        currency = info.get('currency', 'USD')
        return f"The current price of {symbol.upper()} is {price} {currency}."
    except Exception as e:
        return f"Error fetching stock data for {symbol}: {e}"

import requests

# List of API keys
api_keys = [
"ADD MARKET AUX API KEY HERE"
]


def fetch_stock_news(ticker, date):
    base_url = "https://api.marketaux.com/v1/news/all"
    params = {
        "published_on": date,
        "language": "en",
        "search": ticker,
        "exclude_domains": "benzinga.com"
    }

    for api_key in api_keys:
        params["api_token"] = api_key
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 429:  # API rate limit hit
                print(f"API key {api_key} has reached its limit, switching to next key...")
                continue  # Try the next API key

            response.raise_for_status()  # Raise an exception for other errors

            news_data = response.json()
            articles = news_data.get("data", [])

            if articles:
                formatted_result = f"\nNews Articles for {ticker} on {date}:\n"
                for article in articles:
                    if ticker in article['title']:
                        formatted_result += f"Article Title: {article['title']}\n"
                        formatted_result += f"Description: {article['description']}\n"
                        formatted_result += f"Source: {article['source']}\n"
                        formatted_result += f"Snippet: {article['snippet']}\n"
                        formatted_result += "------------------------------\n"
                return formatted_result
            else:
                return f"No articles found for {ticker} on {date}."

        except requests.exceptions.RequestException as e:
            print(f"API key {api_key} failed with error: {e}")

    return f"All API keys have reached their daily limit. Unable to fetch news for {ticker} on {date}."

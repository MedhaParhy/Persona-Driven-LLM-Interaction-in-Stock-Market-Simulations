import requests

# List of API keys
api_keys = [
"kEjWR0ehZeH48EfizQoIbw6hpbFhSferd7djFsnM",
"0YihSPv3B94JP2th8qxIeLYkJcBt8LUrs3NilimJ",
"8NTaRBOROVEHoRkbCGW8sdU0R0vqC9cp0UsPsMdF",
"G5INMq17TW7IFH2BQ1zSJ8wMOa6UiPhCyv0PuDhH",
"7RMKuLQJQapkZvtZlN76jPjqMtEfUBpU2gqKOe7D",
"RUquqfNG0TcTzXGjnWYCI3gw3uYCvVmZbFPVmSEN",
"A44M28dmjq4q9UZEwHKPCi72YBZIcRNA0lzi7ug5",
"KmVfLx9TqhA5Vk82nhuvquS45uviqIWsRJ2kJzRr",
"zT0NiRAhZjKJb7zDJ9S3Oc85ur0Q60VRHTVCBF6M",
"XFlHBtlJEjJCT1fPcYfxNsa9iMxcfBSes5k2QeEk",
"S4oO0MFjdbgLynMAZQ2qxYDbSeCLSq8VOCNO0D4b"
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

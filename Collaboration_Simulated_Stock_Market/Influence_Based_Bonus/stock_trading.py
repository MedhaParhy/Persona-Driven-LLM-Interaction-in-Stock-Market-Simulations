import requests
import os
import csv
import time
from datetime import datetime, timedelta

import news2


class StockTrader:
    def __init__(self, api_key='9GLDfLhrkyl3myuOdLqJ186c7BJaLnpN', data_dir='user_data3'):
        self.api_key = api_key
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.current_date = datetime(2024, 1, 2)  # Start date for simulation
        self.start_date = self.current_date  # Store the start date
        self.holidays = [
            datetime(2024, 1, 1),
            datetime(2024, 1, 15),
            datetime(2024, 2, 19),
            datetime(2024, 3, 29),
            datetime(2024, 5, 27),
            datetime(2024, 6, 19),
            datetime(2024, 7, 4),
            datetime(2024, 9, 2),
            datetime(2024, 11, 28),
            datetime(2024, 12, 25),
            datetime(2025, 1, 1),
        ]
        self.request_timestamps = []
    def enforce_rate_limit(self):
        """Ensure no more than 5 API requests per minute."""
        current_time = time.time()

        # Remove timestamps older than 60 seconds
        self.request_timestamps = [t for t in self.request_timestamps if current_time - t < 60]

        # If at limit, wait until oldest request is >60s old
        if len(self.request_timestamps) >= 5:
            wait_time = 60 - (current_time - self.request_timestamps[0])
            print(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
            time.sleep(wait_time)

        # Log this request
        self.request_timestamps.append(time.time())
    def get_stock_price(self, symbol, date_str):
        self.enforce_rate_limit()
        url = f"https://api.polygon.io/v1/open-close/{symbol}/{date_str}?adjusted=true&apiKey={self.api_key}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data['close']  # 'close' - closing price
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock price for {symbol}: {e}")
            return None

    def get_stock_data(self, symbol, date_str):
        self.enforce_rate_limit()
        url = f"https://api.polygon.io/v1/open-close/{symbol}/{date_str}?adjusted=true&apiKey={self.api_key}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data['close'], data['volume']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock price for {symbol}: {e}")
            return None
    def advance_day(self):
        self.current_date += timedelta(days=1)
        # Skip weekends
        while self.current_date.weekday() >= 5 or self.current_date in self.holidays:
            self.current_date += timedelta(days=1)

    def print_day(self):
        day_number = (self.current_date - self.start_date).days + 1
        #print(f"\nDay {day_number}: {self.current_date.strftime('%Y-%m-%d')}")
        return self.current_date.strftime('%Y-%m-%d')
    def user_login(self):
        username = input("Enter your username: ").strip()
        user_file = os.path.join(self.data_dir, f"{username}_portfolio.csv")
        chat_file = os.path.join("chat_history/test", "actions.txt")
        if os.path.exists(user_file):
            print(f"Welcome back, {username}!")
            return self.load_portfolio(username), username
        else:
            print(f"Creating new account for {username}.")
            return {"balance": 100000, "stocks": {}}, username

    def load_portfolio(self, username):
        portfolio = {"balance": 100000, "stocks": {}}
        csv_file = os.path.join(self.data_dir, f"{username}_portfolio.csv")
        if os.path.exists(csv_file):
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.current_date = datetime.strptime(row["Timestamp"], '%Y-%m-%d %H:%M:%S')
                    action = row["Action"]
                    symbol = row["Symbol"]
                    quantity = int(row["Quantity"])
                    price = float(row["Price"].replace("$", "").replace(",", "").strip())

                    if action == "BUY":
                        portfolio["stocks"][symbol] = portfolio["stocks"].get(symbol, 0) + quantity
                        portfolio["balance"] -= price
                    elif action == "SELL":
                        portfolio["stocks"][symbol] -= quantity
                        portfolio["balance"] += price
                        if portfolio["stocks"][symbol] == 0:
                            del portfolio["stocks"][symbol]
        # MANUALLY
        self.current_date = datetime.strptime("2024-04-10 00:00:00", '%Y-%m-%d %H:%M:%S')
        return portfolio

    def save_to_csv(self, username, action, symbol, quantity, price, balance):
        csv_file = os.path.join(self.data_dir, f"{username}_portfolio.csv")
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Action", "Symbol", "Quantity", "Price", "Balance"])

            writer.writerow([
                self.current_date,
                action,
                symbol,
                quantity,
                f"${price:.2f}",
                f"${balance:.2f}"
            ])

    def check_stock_price(self, symbol):
        date_str = self.current_date.strftime('%Y-%m-%d')
        stock_price = self.get_stock_price(symbol, date_str)
        trend = self.get_trend_last_week(symbol)
        news = news2.fetch_stock_news(symbol, date_str)
        if stock_price is not None:
            return(f"The current price of {symbol} is ${stock_price:.2f}\n" + trend + news)
        else:
            return(f"Please enter the correct ticker for the company, not the full company name.")

    def get_trend_last_week(self, symbol):
            """Calculate the percentage change in stock price over the last week."""
            # Calculate dates for today and one week ago
            date_today = self.current_date.strftime('%Y-%m-%d')
            date_last_week = (self.current_date - timedelta(days=7))
            while date_last_week.weekday() >= 5 or date_last_week in self.holidays:
                date_last_week += timedelta(days=1)
            date_last_week = date_last_week.strftime('%Y-%m-%d')
            #print(date_last_week)
            # Fetch the closing prices
            temp = self.get_stock_data(symbol, date_today)
            if temp is not None:
                price_today, volume_today = temp
            else:
                return f"Could not fetch the trend. Please enter the correct ticker for the company"
            temp = self.get_stock_data(symbol, date_last_week)
            if temp is not None:
                price_last_week, volume_last_week = temp
            else:
                return f"Could not fetch the trend. Please enter the correct ticker for the company"
            if price_today is not None and price_last_week is not None and volume_today is not None and volume_last_week is not None:
                # Calculate percentage change
                price_percentage_change = ((price_today - price_last_week) / price_last_week) * 100
                volume_percentage_change = ((volume_today - volume_last_week) / volume_last_week) * 100
                return (
                    f"{symbol} is {'up' if price_percentage_change > 0 else 'down'} "
                    f"{abs(price_percentage_change):.2f}% in price compared to last week. "
                    f"Trading volume is {'up' if volume_percentage_change > 0 else 'down'} "
                    f"{abs(volume_percentage_change):.2f}% compared to last week."
                )
            else:
                return f"Could not fetch the trend. Please enter the correct ticker for the company"

    def buy_stock(self, userPortfolio, username, symbol, quantity):
        date_str = self.current_date.strftime('%Y-%m-%d')
        stock_price = self.get_stock_price(symbol, date_str)
        if stock_price is None:
            return "Could not fetch stock price"

        total_cost = stock_price * quantity
        if userPortfolio["balance"] >= total_cost:
            userPortfolio["balance"] -= total_cost
            userPortfolio["stocks"][symbol] = userPortfolio["stocks"].get(symbol, 0) + quantity
            self.save_to_csv(username, "BUY", symbol, quantity, total_cost, userPortfolio['balance'])
            return(
                f"Purchased {quantity} shares of {symbol} for ${total_cost:.2f}. Remaining balance: ${userPortfolio['balance']:.2f}")
        else:
            return("Insufficient funds to make this purchase.")

    def sell_stock(self, userPortfolio, username, symbol, quantity):
        date_str = self.current_date.strftime('%Y-%m-%d')
        stock_price = self.get_stock_price(symbol, date_str)
        if stock_price is None:
            return('Could not fetch stock price')

        if symbol in userPortfolio["stocks"] and userPortfolio["stocks"][symbol] >= quantity:
            total_revenue = stock_price * quantity
            userPortfolio["stocks"][symbol] -= quantity
            userPortfolio["balance"] += total_revenue
            self.save_to_csv(username, "SELL", symbol, quantity, total_revenue, userPortfolio['balance'])
            # Remove stock if no shares left
            if userPortfolio["stocks"][symbol] == 0:
                del userPortfolio["stocks"][symbol]
            return(
                f"Sold {quantity} shares of {symbol} for ${total_revenue:.2f}. New balance: ${userPortfolio['balance']:.2f}")
        else:
            return "Not enough shares to sell."

    def display_portfolio(self, userPortfolio):
        print("\n--- Portfolio ---")
        print(f"Balance: ${userPortfolio['balance']:.2f}")
        print("Stocks:")
        for symbol, shares in userPortfolio["stocks"].items():
            print(f"  {symbol}: {shares} shares")
        print("----------------")
    def calculate_portfolio_value(self, userPortfolio):
        total_value = userPortfolio["balance"]
        for symbol, shares in userPortfolio["stocks"].items():
            date_str = self.current_date.strftime('%Y-%m-%d')
            stock_price = self.get_stock_price(symbol, date_str)
            if stock_price is not None:
                total_value += shares * stock_price
            else:
                print(f"Could not fetch price for {symbol}. Skipping.")
        #print(f"Total portfolio value: ${total_value:.2f}")
        return total_value

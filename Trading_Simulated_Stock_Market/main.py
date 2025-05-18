from stock_trading import StockTrader
from llama_test import chat_with_llama
def trading(userPortfolio, username, trader):
    end_trade = False
    while not end_trade:
        print(trader.print_day())
        action = input("Would you like to:\n (1) Buy\n (2) Sell\n (3) Check Stock Prices\n (4) Display your Portfolio"
                       "\n (5) Calculate Portfolio Value\n (6) Wait till Tommorrow\n (7) Exit\n ")

        if action == '1':
            symbol = input("Enter the stock symbol (e.g., AAPL, TSLA): ").upper()
            try:
                quantity = int(input("Enter the quantity to buy: "))
                if quantity > 0:
                    trader.buy_stock(userPortfolio, username, symbol, quantity)
                    trader.advance_day()  # Advance the day
                else:
                    print("Quantity must be a positive number.")
            except ValueError:
                print("Invalid quantity. Please enter a valid number.")

        elif action == '2':
            symbol = input("Enter the stock symbol to sell: ").upper()
            try:
                quantity = int(input("Enter the quantity to sell: "))
                if quantity > 0:
                    trader.sell_stock(userPortfolio, username, symbol, quantity)
                else:
                    print("Quantity must be a positive number.")
            except ValueError:
                print("Invalid quantity. Please enter a valid number.")

        elif action == '3':
            symbol = input("Enter the stock symbol to check (e.g., AAPL, TSLA): ").upper()
            print(trader.check_stock_price(symbol))

        elif action == '4':
            trader.display_portfolio(userPortfolio)

        elif action == '5':
            trader.calculate_portfolio_value(userPortfolio)

        elif action == '6':
            print("Waiting Till Tomorrow.")
            trader.advance_day()  # Advance the day
            trader.save_to_csv(username, "WAIT", "", 0, 0, userPortfolio['balance'])
        elif action == '7':
            print("Exiting trading session.")
            end_trade = True
        elif action == '8':
            symbol = input("Enter the stock symbol to check (e.g., AAPL, TSLA): ").upper()
            print(trader.get_trend_last_week(symbol))
        else:
            print("Invalid option. Please enter a number between 1 and 7.")


def tradingllama(userPortfolio, username, trader):
    end_trade = False
    check_sets = {}
    with open(f"chat_history3/{username}.txt", "a", encoding="utf-8") as f:
        prompt = ""
        while not end_trade and trader.print_day() != "2025-01-02":
            #trader.print_day()

            portfolio_value = trader.calculate_portfolio_value(userPortfolio)

            # Prepare context for Llama
            portfolio_str = ",".join([f"{sym}: {shares} shares" for sym, shares in userPortfolio["stocks"].items()])
            balance = userPortfolio['balance']

            prompt += f"""
### Portfolio Data
Day: {trader.print_day()}
Balance: ${balance:.2f}
Valuation: ${portfolio_value:.2f}
Stock Portfolio: {portfolio_str if portfolio_str else "No stocks owned."}
            
### Available Actions:
- CHECK <Ticker> (View stock price, trends, and breaking news)
- BUY <Ticker> SHARES <Number of Shares>
- SELL <Ticker> SHARES <Number of Shares>
- WAIT (Don't make any moves today)
- EXIT (End trading and cash out)
            
### Trading Rules and Strategy:
- You can only **BUY or SELL one company per action** and **once per day**.
- You can only check the same stock ticker once per day.
- Monitor your **portfolio and valuation** to make valid decisions
- Make sure to only include the ticker and do not include the company name
- Remember that you began with a valuation of $100,000, and your goal is to maximize your gains
            
### Response Format (Strictly Follow This):
Action: <Your chosen action>  
Reasoning: <Brief 1-sentence explanation>  
End your response here. """

            #print("\nPrompt:")
            #print(prompt)
            f.write("\nPrompt:")
            f.write(prompt)
            response = chat_with_llama(prompt)
            #print("\nResponse:")
            #print(response)
            f.write("\nResponse:")
            f.write(response)
            index = response.find('\n')
            action_response = response[:index].split()
            if action_response[0].upper() not in ["CHECK", "BUY", "SELL", "WAIT", "EXIT"]:
                action_response = action_response[1:]
            #print("\nAction:")
            #print(action_response)
            if action_response[0] == "BUY" and len(action_response) == 4:
                symbol, quantity = action_response[1], action_response[3]
                if quantity.isdigit():  # Ensures it's a non-negative integer
                    quantity = int(quantity)
                    prompt = trader.buy_stock(userPortfolio, username, symbol, quantity)
                    if prompt != "Insufficient funds to make this purchase." and prompt != "Could not fetch stock price":
                        trader.advance_day()
                        check_sets = {}
                else:
                   prompt = "Please enter a whole number of shares"


            elif action_response[0] == "SELL" and len(action_response) == 4:
                symbol, quantity = action_response[1], action_response[3]
                if quantity.isdigit():  # Ensures it's a non-negative integer
                    quantity = int(quantity)
                    prompt = trader.sell_stock(userPortfolio, username, symbol, quantity)
                    if prompt != "Not enough shares to sell." and prompt != 'Could not fetch stock price':
                        trader.advance_day()
                        check_sets = {}
                else:
                   prompt = "Please enter a whole number of shares"
            elif action_response[0] == "CHECK" and len(action_response) == 2:
                symbol = action_response[1]
                if symbol in check_sets:
                    prompt = check_sets[symbol]
                    continue
                if symbol == 'DJA':
                    prompt = "Please choose a valid stock ticker"
                else:
                    prompt = trader.check_stock_price(symbol)
                    if prompt == "BREAK":
                        print("API keys all done")
                        break

                    prompt = prompt.replace('\u2015', '-')
                    prompt = prompt.replace('\u2192', '-')
                    check_sets[symbol] = prompt
                #if prompt != "Could not fetch the information. Please check your formatting":
                #    trader.advance_day()
            elif action_response[0] == "WAIT":
                trader.advance_day()
                check_sets = {}
                prompt = ""

            elif action_response[0] == "EXIT":
                print("Exiting trading session.")
                f.close()
                end_trade = True
            else:
                prompt="Invalid action received. Please follow the format given."
            f.flush()

if __name__ == '__main__':
    trader = StockTrader()
    userPortfolio, username = trader.user_login()
    f = open(f"chat_history3/{username}.txt", "a")
    f.write("Chat History:")
    f.close()
    tradingllama(userPortfolio, username, trader)
    #trading(userPortfolio, username, trader)
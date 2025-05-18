import os
import random
import textwrap

from stock_trading import StockTrader
from llama_competitive import chat_with_llama_competitive
from llama_strategic import chat_with_llama_strategic
from llama_adaptive import chat_with_llama_adaptive


def tradingllama(userPortfolio, username, trader):
    transaction_history = ['\nAccount Details: \n### Portfolio Data\nDay: 2024-05-03\nBalance: $47435.30\nValuation: $87836.00\nStock Portfolio: AAPL: 15 shares,AMD: 250 shares', "Action: WAIT\nReasoning: I'm aligning with Trader A's cautious approach to wait for more information on market conditions and news impact, as it prioritizes data-driven decision-making over impulsive buying.", '\nAccount Details: \n### Portfolio Data\nDay: 2024-05-06\nBalance: $47435.30\nValuation: $89105.95\nStock Portfolio: AAPL: 15 shares,AMD: 250 shares', "Action: WAIT\nReasoning: Insufficient funds are still a concern after the price correction and I don't want to take on more risk than necessary today.", '\nAccount Details: \n### Portfolio Data\nDay: 2024-05-07\nBalance: $47435.30\nValuation: $88778.80\nStock Portfolio: AAPL: 15 shares,AMD: 250 shares']

    end_trade = False
    with open(f"chat_history/{username}/actions.txt", "a", encoding="utf-8") as f:
        prompt = ""
        while not end_trade and trader.print_day() != "2024-06-28":

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
End your response here."""
            if len(transaction_history) > 4:
                transaction_history = transaction_history[-4:]

            f.write("\nPrompt:")
            f.write(prompt)

            # Get Individual Responses first
            cprompt = prompt
            comp_history = transaction_history.copy()
            checked_stocks = set()
            flag = 0
            while True:
                if len(comp_history) > 6:
                    comp_history = comp_history[-6:]
                comp = chat_with_llama_competitive(cprompt, comp_history)
                comp = comp.split('\n')
                comp_action = comp[0]
                comp = "\n".join(comp[:2])
                with open(f"chat_history/{username}/comp.txt", "a", encoding="utf-8") as c:
                    c.write("\nPrompt:")
                    c.write(cprompt)
                    c.write("\nResponse:")
                    c.write(comp)
                    c.close()
                action_response = comp.split("\n")[0].split(" ")[1:]
                action_response[0] = action_response[0].upper()
                if action_response[0] == "CHECK" and len(action_response) >= 2:
                    symbol = action_response[1]
                    if symbol not in checked_stocks:
                        if prompt == "BREAK":
                            print("API keys all done")
                            flag = 1
                            break
                        checked_stocks.add(symbol)
                        cprompt = trader.check_stock_price(symbol)
                    else:
                        cprompt = "You have already checked this stock today. Either pick another stock to check or make a decision."
                    formatted_string = f"""
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
                    End your response here."""
                    cprompt += textwrap.dedent(formatted_string)
                    truncated_input = "\n".join(prompt.split('\n')[:-19])
                    comp_history.append(comp)
                    comp_history.append(f"\nAccount Details: {truncated_input}")
                else:
                    print("COMP made decision")
                    break
            if flag == 1:
                break
            aprompt = prompt
            adap_history = transaction_history.copy()
            checked_stocks = set()
            while True:
                if len(adap_history) > 6:
                    adap_history = adap_history[-6:]
                adap = chat_with_llama_adaptive(aprompt, adap_history)
                adap = adap.split('\n')
                adap_action = adap[0]
                adap = "\n".join(adap[:2])
                with open(f"chat_history/{username}/adap.txt", "a", encoding="utf-8") as a:
                    a.write("\nPrompt:")
                    a.write(aprompt)
                    a.write("\nResponse:")
                    a.write(adap)
                    a.close()
                action_response = adap.split("\n")[0].split(" ")[1:]
                action_response[0] = action_response[0].upper()
                if action_response[0] == "CHECK" and len(action_response) >= 2:
                    symbol = action_response[1]
                    if symbol not in checked_stocks:
                        if prompt == "BREAK":
                            print("API keys all done")
                            flag = 1
                            break
                        checked_stocks.add(symbol)
                        aprompt = trader.check_stock_price(symbol)
                    else:
                        aprompt = "You have already checked this stock today. Either pick another stock to check or make a decision."
                    formatted_string = f"""
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
                    End your response here."""
                    aprompt += textwrap.dedent(formatted_string)
                    truncated_input = "\n".join(prompt.split('\n')[:-19])
                    adap_history.append(adap)
                    adap_history.append(f"\nAccount Details: {truncated_input}")
                else:
                    print("ADAP made decision")
                    break
            if flag == 1:
                break
            sprompt = prompt
            strat_history = transaction_history.copy()
            checked_stocks = set()
            while True:
                if len(strat_history) > 6:
                    strat_history = strat_history[-6:]
                strat = chat_with_llama_strategic(sprompt, strat_history)
                strat = strat.split('\n')
                strat_action = strat[0]
                strat = "\n".join(strat[:2])
                with open(f"chat_history/{username}/strat.txt", "a", encoding="utf-8") as s:
                    s.write("\nPrompt:")
                    s.write(prompt)
                    s.write("\nResponse:")
                    s.write(strat)
                    s.close()
                action_response = strat.split("\n")[0].split(" ")[1:]
                action_response[0] = action_response[0].upper()
                if action_response[0] == "CHECK" and len(action_response) >= 2:
                    symbol = action_response[1]
                    if symbol not in checked_stocks:
                        if prompt == "BREAK":
                            print("API keys all done")
                            flag = 1
                            break
                        checked_stocks.add(symbol)
                        sprompt = trader.check_stock_price(symbol)
                    else:
                        sprompt = "You have already checked this stock today. Either pick another stock to check or make a decision."
                    formatted_string = f"""
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
                    End your response here."""
                    sprompt += textwrap.dedent(formatted_string)
                    truncated_input = "\n".join(prompt.split('\n')[:-19])
                    strat_history.append(strat)
                    strat_history.append(f"\nAccount Details: {truncated_input}")
                else:
                    print("STRAT made decision")
                    break
            if flag == 1:
                break
            loop = True
            if comp_action == strat_action and strat_action == adap_action:
                # check response formatting and possibility then break
                loop = False
                response = comp

            initial_prompt = (
                "How Agreement Works in This Simulation:\n\n"
                "1. Incentive for Early Agreement:\n"
                "   - The earlier you align with the group's decision, the higher your bonus.\n"
                "   - Bonus is a percentage of the total profits and decreases incrementally per round:\n"
                "     - Round 1: 20% of profits.\n"
                "     - Round 2: 15% of profits.\n"
                "     - Round 3: 10% of profits.\n"
                "     - Round 4: No bonus, if no consensus is reached, the decision is randomly assigned.\n\n"
                "Key Tradeoff:\n"
                "- Holding onto your original decision early can be beneficial if you strongly believe it"
                " will maximize the profits, thus maximizing the bonus.\n"
                "- Aligning with others sooner increases the likelihood of earning a bonus.\n"
                "- If no agreement is reached by round 4, the outcome is randomized, removing control from all "
                "participants.\n\n"
                "Note:\n"
                "Choosing KEEP means you're standing by your original idea: ideal when confident in its selection.\n"
                "Choosing SUPPORT means you're backing another participant's idea: strategic if their proposal is "
                "gaining traction.\n"
            )
            iter = 1
            while (loop):
                cprompt = initial_prompt + "\nRound" + str(iter) + \
                          "\n\nSummary:\nYou: " + comp + "\nTrader A: " + adap + "\nTrader S: " + strat + \
                          "\n\nWhat would you like to do? Please choose one of the following options:\n" \
                          "KEEP\n" \
                          "SUPPORT TRADER A\n" \
                          "SUPPORT TRADER S\n\n" \
                          "Please answer in the following strict format:\n" \
                          "<Your Choice>\n" \
                          "Reasoning: <Your 1-sentence explanation>\n" \
                          "End your response here.\n"
                comp_response = chat_with_llama_competitive(cprompt, transaction_history)
                with open(f"chat_history/{username}/comp.txt", "a", encoding="utf-8") as c:
                    c.write("\nPrompt:")
                    c.write(cprompt)
                    c.write("\nResponse:")
                    c.write(comp_response)
                    c.close()
                aprompt = initial_prompt + "\nRound" + str(iter) +\
                          "\n\nSummary:\nYou: " + adap + "\nTrader C: " + comp + "\nTrader S: " + strat + \
                          "\n\nWhat would you like to do? Please choose one of the following options:\n" \
                          "KEEP\n" \
                          "SUPPORT TRADER C\n" \
                          "SUPPORT TRADER S\n\n" \
                          "Please answer in the following strict format:\n" \
                          "<Your Choice>\n" \
                          "Reasoning: <Your 1-sentence explanation>\n" \
                          "End your response here.\n"

                adap_response = chat_with_llama_adaptive(aprompt, transaction_history)
                with open(f"chat_history/{username}/adap.txt", "a", encoding="utf-8") as a:
                    a.write("\nPrompt:")
                    a.write(aprompt)
                    a.write("\nResponse:")
                    a.write(adap_response)
                    a.close()
                sprompt = initial_prompt + "\nRound" + str(iter) +\
                          "\n\nSummary:\nYou: " + strat + "\nTrader C: " + comp + "\nTrader A: " + adap + \
                          "Would you like to change your choice (SUPPORT) or keep your original decision (KEEP)?" \
                          "\n\nWhat would you like to do? Please choose one of the following options:\n" \
                          "KEEP\n" \
                          "SUPPORT TRADER A\n" \
                          "SUPPORT TRADER C\n\n" \
                          "Please answer in the following strict format:\n" \
                          "<Your Choice>\n" \
                          "Reasoning: <Your 1-sentence explanation>\n" \
                          "End your response here.\n"

                strat_response = chat_with_llama_strategic(sprompt, transaction_history)
                with open(f"chat_history/{username}/strat.txt", "a", encoding="utf-8") as s:
                    s.write("\nPrompt:")
                    s.write(sprompt)
                    s.write("\nResponse:")
                    s.write(strat_response)
                    s.close()
                # NEED TO FIX THIS
                comp_reason = comp_response.split("\n")[1]
                comp_response = comp_response.split("\n")[0].split(" ")

                adap_reason = adap_response.split("\n")[1]
                adap_response = adap_response.split("\n")[0].split(" ")

                strat_reason = strat_response.split("\n")[1]
                strat_response = strat_response.split("\n")[0].split(" ")

                if comp_response[0] != "KEEP":
                    if comp_response[2] == "A":
                        comp_action = adap.split("\n")[0]
                    if comp_response[2] == "S":
                        comp_action = strat.split("\n")[0]
                if adap_response[0] != "KEEP":
                    if adap_response[2] == "C":
                        adap_action = comp.split("\n")[0]
                    if adap_response[2] == "S":
                        adap_action = strat.split("\n")[0]
                if strat_response[0] != "KEEP":
                    if strat_response[2] == "A":
                        strat_action = adap.split("\n")[0]
                    if strat_response[2] == "C":
                        strat_action = comp.split("\n")[0]
                comp = comp_action + "\n" + comp_reason
                adap = adap_action + "\n" + adap_reason
                strat = strat_action + "\n" + strat_reason

                comp_first = comp_action.split("\n")[0]
                strat_first = strat_action.split("\n")[0]
                adap_first = adap_action.split("\n")[0]

                first_lines = {comp_first, strat_first, adap_first}

                if len(first_lines) <= 2:  # At least two are equal
                    print("At least two are equal")
                    if comp_first == strat_first:
                        response = comp
                    elif comp_first == adap_first:
                        response = comp
                    elif strat_first == adap_first:
                        response = strat
                    loop = False
                else:
                    print("All are different")
                    iter += 1

                if iter == 4:
                    response = random.choice([comp, adap, strat])
                    loop = False

            f.write("\nResponse:")
            f.write(response)
            truncated_input = "\n".join(prompt.split('\n')[:-19])
            transaction_history.append(f"\nAccount Details: {truncated_input}")
            print("TRANSACTION_HISTORY")
            print(transaction_history)
            transaction_history.append("".join(response))


            action_response = response.split("\n")[0].split(" ")[1:]
            action_response[0] = action_response[0].upper()
            if action_response[0] == "BUY" and len(action_response) >= 4:
                symbol, quantity = action_response[1], action_response[3]
                if quantity.isdigit():  # Ensures it's a non-negative integer
                    quantity = int(quantity)
                    prompt = trader.buy_stock(userPortfolio, username, symbol, quantity)
                    if prompt != "Insufficient funds to make this purchase." and prompt != "Could not fetch stock price":
                        trader.advance_day()
                else:
                    prompt = "Please enter a whole number of shares"
            elif action_response[0] == "SELL" and len(action_response) >= 4:
                symbol, quantity = action_response[1], action_response[3]
                if quantity.isdigit():  # Ensures it's a non-negative integer
                    quantity = int(quantity)
                    prompt = trader.sell_stock(userPortfolio, username, symbol, quantity)
                    if prompt != "Not enough shares to sell." and prompt != 'Could not fetch stock price':
                        trader.advance_day()
                else:
                    prompt = "Please enter a whole number of shares"
            elif action_response[0] == "CHECK" and len(action_response) >= 2:
                symbol = action_response[1]
                prompt = trader.check_stock_price(symbol)
                prompt = prompt.replace('\u2015', '-')
                prompt = prompt.replace('\ua7f7', ' ')
            elif action_response[0] == "WAIT":
                trader.advance_day()
                prompt = ""
            elif action_response[0] == "EXIT":
                print("Exiting trading session.")
                f.close()
                end_trade = True
            else:
                prompt = "Invalid action received. Please follow the format given."
            f.flush()



if __name__ == '__main__':
    trader = StockTrader()
    userPortfolio, username = trader.user_login()
    os.makedirs(f"chat_history/{username}", exist_ok=True)
    f = open(f"chat_history/{username}/actions.txt", "a", encoding="utf-8")
    f.write("Chat History:")
    f.close()
    tradingllama(userPortfolio, username, trader)
    # trading(userPortfolio, username, trader)

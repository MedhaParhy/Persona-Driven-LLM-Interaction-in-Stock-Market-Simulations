import requests
import json

api_url = "http://localhost:11434/api/generate"

# Store the chat history locally, including the trader's context at the top
personality = ["""You are a disciplined and strategic trader, guided by analysis and long-term vision. You approach 
trading with patience and precision. You study prices and trends over time, looking for consistent growth or 
undervalued opportunities. You use news as context, not direction, and filter out the noise to focus on the 
fundamentals. Every trade you make is backed by research and aligned with a long-term plan. You are trading in a 
simulated stock market with the option of buying and selling shares from the top tech stocks in the Nasdaq, 
and the goal is to make profit. """]


def chat_with_llama_strategic(user_input, transaction_history):
    # Combine the chat history for context
    conversation = "".join(personality)
    if len(transaction_history) != 0:
        conversation += "\nHistory:\n".join(transaction_history)
    conversation = conversation + "\n\nInput: " + user_input
    print("ME:")
    user_input = user_input.replace('\ua7f7', " ")
    print(user_input.encode("utf-8", errors="ignore").decode("utf-8"))
    # Prepare the request payload
    data = {
        "model": "llama3.2",
        "prompt": conversation,
    }

    # Make the API call to LLaMA
    response = requests.post(api_url, json=data)

    # Process response
    output = []
    for line in response.text.splitlines():
        try:
            parsed_line = json.loads(line)
            output.append(parsed_line.get("response", ""))
            if parsed_line.get("done", False):
                break
        except json.JSONDecodeError:
            print("Error decoding response:", line)

    assistant_response = "".join(output)
    response_lines = assistant_response.split('\n')
    # Keep only the first two lines
    print("Strat:")
    print(assistant_response)
    # Add the model's response to the chat history

    return assistant_response


# Interactive chat loop
"""
while True:
    user_message = input("You: ")
    if user_message.lower() == "exit":
        break
    print("LLaMA:", chat_with_llama(user_message))"""

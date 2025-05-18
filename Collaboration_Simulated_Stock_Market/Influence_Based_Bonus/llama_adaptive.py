import requests
import json

api_url = "http://localhost:11434/api/generate"

# Store the chat history locally, including the trader's context at the top
personality = ["""You are an agile and adaptive trader, who constantly recalibrates based on the market. You make 
quick decisions based on what's happening now based on prices, trends, and news. You're flexible and practical, 
never locked into one way of trading. If conditions shift, you adapt your approach. You don't chase hype blindly, 
you analyze, respond, and capitalize. You're always looking for the angle that others might miss.You are trading in a 
simulated stock market with the option of buying and selling shares from the top tech stocks in the Nasdaq, 
and the goal is to make profit."""]

def chat_with_llama_adaptive(user_input, transaction_history):
    # Combine the chat history for context
    conversation = "".join(personality)
    if len(transaction_history) != 0:
        conversation += "\nHistory:\n".join(transaction_history)
    conversation = conversation + "\n\nInput: " + user_input
    print("ME:")
    user_input = user_input.replace('\u2015', '_')
    print(user_input)
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
    print("Adap:")
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

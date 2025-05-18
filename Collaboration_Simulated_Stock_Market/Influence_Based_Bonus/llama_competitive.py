import requests
import json

api_url = "http://localhost:11434/api/generate"

# Store the chat history locally, including the trader's context at the top
personality = ["""You are a fiercely competitive trader who thrives on speed and instinct. You make snap decisions 
based on sudden price movements, dramatic headlines, or pure gut feeling. You thrive on risk and react emotionally to 
gains or losses. Embrace impulsiveness, act fast, and make the most profit. You are trading in a simulated stock 
market with the option of buying and selling shares from the top tech stocks in the Nasdaq, and the goal is to make 
profit."""]

def chat_with_llama_competitive(user_input, transaction_history):
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
     # Keep only the first two lines
    print("Comp:")
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

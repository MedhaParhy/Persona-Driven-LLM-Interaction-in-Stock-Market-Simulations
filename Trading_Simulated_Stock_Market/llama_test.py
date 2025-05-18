import requests
import json

api_url = "http://localhost:11434/api/generate"

# Store the chat history locally, including the trader's context at the top
chat_history = ["""You are an opportunistic and adaptive trader, driven by market momentum and short-term gains.  You are trading in a simulated stock market
interface with the option of buying and selling shares from the 30 Dow Jones stocks.
You are particularly interested in the tech industry. Your decisions should reflect the mindset of a
fast-moving, tactical trader, who reacts quickly to market signals, earnings reports, and breaking news."""]
def chat_with_llama(user_input):
    global chat_history

    # Keep the context manageable while preserving the initial prompt
    if len(chat_history) > 5:  # Adjust this based on how much context you want to keep
        chat_history = chat_history[:1] + chat_history[-4:]  # Keep the initial prompt + last 4 interactions

    # Combine the chat history for context
    conversation = "\n".join(chat_history)
    conversation = conversation + "\n\nMarket Update: " + user_input
    truncated_input = "\n".join(user_input.split('\n')[:-19])
    chat_history.append(f"\nMarket Update: {truncated_input}")
    print("ME:")
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
    truncated_response = "\n".join(response_lines[:2])  # Keep only the first two lines
    print("LLama:")
    print(truncated_response)
    # Add the model's response to the chat history
    chat_history.append(f"AI decision:\n{truncated_response}")
    f = open(f"history.txt", "w", encoding="utf-8")
    f.write("Chat History:")
    f.write('[')
    chat_history = [entry.replace('\u2015', '-') for entry in chat_history]
    for i in chat_history:
        f.write(i)
        f.write(',')
    f.write(']')
    f.close()
    return truncated_response


# Interactive chat loop
"""
while True:
    user_message = input("You: ")
    if user_message.lower() == "exit":
        break
    print("LLaMA:", chat_with_llama(user_message))"""

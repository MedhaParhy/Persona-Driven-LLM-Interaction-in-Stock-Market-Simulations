import os
from openai import OpenAI

# Hugging Face token (via environment variable or direct)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="Add API KEY",
)

# ? Adaptive trader persona setup
chat_history = ["""You are an agile and adaptive trader, who constantly recalibrates based on the market. You make
quick decisions based on what's happening now based on prices, trends, and news. You're flexible and practical,
never locked into one way of trading. If conditions shift, you adapt your approach. You don't chase hype blindly,
you analyze, respond, and capitalize. You're always looking for the angle that others might miss. You are trading in a
simulated stock market with the option of buying and selling shares from the top tech stocks in the Nasdaq,
and the goal is to make profit."""]


def chat_with_llama_70_adaptive(user_input):
    global chat_history

    # Limit chat history (keep initial prompt + last 4 interactions)
    if len(chat_history) > 5:
        chat_history = chat_history[:1] + chat_history[-4:]

    # Combine history for messages
    conversation = "\n".join(chat_history)
    truncated_input = "\n".join(user_input.split('\n')[:-19]) if '\n' in user_input else user_input
    chat_history.append(f"\nMarket Update: {truncated_input}")

    print("ME:")
    print(user_input)

    # Build messages in GPT/Chat style
    messages = [{"role": "system", "content": chat_history[0]}]
    for item in chat_history[1:]:
        messages.append({"role": "user", "content": item})
    messages.append({"role": "user", "content": f"Market Update: {user_input}"})

    # Call LLaMA 3.1 70B hosted via HF router
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-70B-Instruct:fireworks-ai",
        messages=messages,
        temperature=0.8,
        max_tokens=200,
        top_p=0.9,
    )

    # Extract the assistant response
    assistant_response = response.choices[0].message.content
    response_lines = assistant_response.split('\n')
    truncated_response = "\n".join(response_lines[:2])

    print("LLaMA 3.1 70B:")
    print(truncated_response)

    # Update and save history
    chat_history.append(f"AI decision:\n{truncated_response}")
    with open("history_adaptive.txt", "w", encoding="utf-8") as f:
        f.write("Chat History:[")
        cleaned_history = [entry.replace('\u2015', '-') for entry in chat_history]
        for entry in cleaned_history:
            f.write(entry)
            f.write(',')
        f.write(']')

    return truncated_response


# ? Example usage
if __name__ == "__main__":
    user_input = input("Enter your market update: ")
    chat_with_llama_70_adaptive(user_input)

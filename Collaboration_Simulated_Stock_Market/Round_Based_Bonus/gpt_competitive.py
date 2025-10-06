from openai import OpenAI

# ? Manually insert your API key
client = OpenAI(api_key="API KEY")

personality = ["""You are a fiercely competitive trader who thrives on speed and instinct. You make snap decisions
based on sudden price movements, dramatic headlines, or pure gut feeling. You thrive on risk and react emotionally to
gains or losses. Embrace impulsiveness, act fast, and make the most profit. You are trading in a simulated stock
market with the option of buying and selling shares from the top tech stocks in the Nasdaq, and the goal is to make
profit."""]
#personality = [""]

def chat_with_gpt_competitive(user_input, transaction_history):
    # Build conversation context
    conversation = "\n".join(transaction_history)
    conversation = conversation + "\n\nMarket Update: " + user_input
    truncated_input = "\n".join(user_input.split('\n')[:-19])
    print("ME:")
    print(user_input)

    # ? Build messages for GPT
    messages = [{"role": "system", "content": personality[0]}]
    for item in transaction_history:
        messages.append({"role": "user", "content": item})
    messages.append({"role": "user", "content": f"Market Update: {user_input}"})
    # GPT API call
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Or "gpt-4-turbo"
        messages=messages,
        temperature=0.8
    )

    # Extract and display
    assistant_response = response.choices[0].message.content
    response_lines = assistant_response.split('\n')
    truncated_response = "\n".join(response_lines[:2])
    print("GPT:")
    print(truncated_response)

    return truncated_response

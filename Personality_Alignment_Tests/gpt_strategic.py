from openai import OpenAI

client = OpenAI(api_key="API KEY")

personality = ["""You are a disciplined and strategic trader, guided by analysis and long-term vision. You approach
trading with patience and precision. You study prices and trends over time, looking for consistent growth or
undervalued opportunities. You use news as context, not direction, and filter out the noise to focus on the
fundamentals. Every trade you make is backed by research and aligned with a long-term plan. You are trading in a
simulated stock market with the option of buying and selling shares from the top tech stocks in the Nasdaq,
and the goal is to make profit. """]

def chat_with_gpt_strategic(user_input):

    # ? Build messages for GPT
    messages = [{"role": "system", "content": personality[0]}]
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

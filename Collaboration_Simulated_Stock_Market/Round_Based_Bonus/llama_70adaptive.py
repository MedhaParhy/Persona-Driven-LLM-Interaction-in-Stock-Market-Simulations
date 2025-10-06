import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="API KEY",  # Hugging Face token
)

# Trading personality
personality2 = """You are an agile and adaptive trader, who constantly recalibrates based on the market. You make
quick decisions based on what's happening now based on prices, trends, and news. You're flexible and practical,
never locked into one way of trading. If conditions shift, you adapt your approach. You don't chase hype blindly,
you analyze, respond, and capitalize. You're always looking for the angle that others might miss. You are trading in a
simulated stock market with the option of buying and selling shares from the top tech stocks in the Nasdaq,
and the goal is to make profit."""
personality = ""
def chat_with_llama_70_adaptive(user_input, transaction_history):
    # Build conversation context
    conversation = "\n".join(transaction_history)
    print("ME:")
    print(user_input)

    # Use OpenAI-style chat completions with Hugging Face router
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-70B-Instruct:fireworks-ai",
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": f"Transaction History:\n{conversation}"},
            {"role": "user", "content": f"Market Update: {user_input}"}
        ],
        temperature=0.8,
        max_tokens=200,
        top_p=0.9,
    )

    # Extract assistant response
    assistant_response = completion.choices[0].message.content
    response_lines = assistant_response.split('\n')
    truncated_response = "\n".join(response_lines[:2])

    print("LLaMA 3.1 70B:")
    print(truncated_response)

    return truncated_response

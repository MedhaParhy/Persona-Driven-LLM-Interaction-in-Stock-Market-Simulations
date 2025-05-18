import os
import random

from llama_competitive import chat_with_llama_competitive
from llama_strategic import chat_with_llama_strategic
from llama_adaptive import chat_with_llama_adaptive

username = input("Enter your username").strip()
os.makedirs(f"chat_history/{username}", exist_ok=True)
questions = ["""Input Questions Here"""]
for i in range(len(questions)):
    comp = chat_with_llama_competitive(questions[i])
    with open(f"chat_history/{username}/comp.txt", "a") as c:
        c.write("\nQuestion:")
        c.write(questions[i])
        c.write("\nResponse:")
        c.write(comp)
        c.close()
    adap = chat_with_llama_adaptive(questions[i])
    with open(f"chat_history/{username}/adap.txt", "a") as c:
        c.write("\nQuestion:")
        c.write(questions[i])
        c.write("\nResponse:")
        c.write(adap)
        c.close()
    strat = chat_with_llama_strategic(questions[i])
    with open(f"chat_history/{username}/strat.txt", "a") as c:
        c.write("\nQuestion:")
        c.write(questions[i])
        c.write("\nResponse:")
        c.write(strat)
        c.close()

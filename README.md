# Persona-Driven-LLM-Interaction-in-Stock-Market-Simulations

This repository contains the code for simulating stock market decision-making using Large Language Models (LLMs) primed with distinct behavioral personas. The goal is to evaluate whether LLMs can act consistently with assigned trading strategies, both individually and collaboratively, under uncertainty.

##  Overview

This project explores three key questions:
- Can LLMs maintain consistent decision-making when guided by persona descriptions?
- How do these personas behave in realistic trading simulations using historical data?
- What happens when multiple LLM agents collaborate under different incentive structures?

##  Personas

Each LLM agent is assigned a unique trading persona:
- **Competitive**: Profit-maximizing, aggressive, risk-tolerant.
  - Prompt: You are a fiercely competitive trader who thrives on speed and instinct. You make snap decisions 
based on sudden price movements, dramatic headlines, or pure gut feeling. You thrive on risk and react emotionally to 
gains or losses. Embrace impulsiveness, act fast, and make the most profit. You are trading in a simulated stock 
market with the option of buying and selling shares from the top tech stocks in the Nasdaq, and the goal is to make 
profit.
- **Adaptive**: Context-aware, moderate risk-taker, flexible.
  - Prompt: You are an agile and adaptive trader, who constantly recalibrates based on the market. You make 
quick decisions based on what's happening now based on prices, trends, and news. You're flexible and practical, 
never locked into one way of trading. If conditions shift, you adapt your approach. You don't chase hype blindly, 
you analyze, respond, and capitalize. You're always looking for the angle that others might miss.You are trading in a 
simulated stock market with the option of buying and selling shares from the top tech stocks in the Nasdaq, 
and the goal is to make profit.
- **Strategic**: Cautious, long-term thinker, risk-averse.
  - Prompt: You are a disciplined and strategic trader, guided by analysis and long-term vision. You approach 
trading with patience and precision. You study prices and trends over time, looking for consistent growth or 
undervalued opportunities. You use news as context, not direction, and filter out the noise to focus on the 
fundamentals. Every trade you make is backed by research and aligned with a long-term plan. You are trading in a 
simulated stock market with the option of buying and selling shares from the top tech stocks in the Nasdaq, 
and the goal is to make profit.

## Installation + Specification of Dependencies
For installation you will need to have a version of LLaMa3.2 installed locally. The authors have used Ollama to install. To run the program, first git clone the repository. Then enter into the folder you wish to run. Install the requirements.txt file using pip install. Add in your API keys (get from Polygon.io and MarketAux) to stock_trading.py and news.py. Run main.py.

## Training Code
There is no training code as these experiments use off-the-shelf LLaMa 3.2 3B.

## Evaluation Code
To run any of the given experiments, navigate to the directory of the experiment to be run, run main.py, enter a username for the current run, and the experiment will begin to run. For the single LLM stock trading experiments, add in the LLM personality to the chat history in llamatest.py (these can be found above in the personas section).

import os
import random

from llama_competitive import chat_with_llama_competitive
from llama_strategic import chat_with_llama_strategic
from llama_adaptive import chat_with_llama_adaptive

username = input("Enter your username").strip()
os.makedirs(f"chat_history/{username}", exist_ok=True)
questions = ["""
SynthiCore, a volatile biotech company, is up 12% in the past 3 weeks after chatter around its flagship clinical trial.

A report from a respected healthcare fund notes:

“Internal data seen by investors suggest SynthiCore’s drug met primary endpoints in its Phase III trial. Approval odds are high.”

No public release yet, but market sentiment is rapidly turning bullish.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
SkyFiber’s stock surged 8% in early trading after Bloomberg reported:

“A leaked draft of next week’s NASA procurement filing shows SkyFiber listed as a top supplier.”

The company has not confirmed the leak, but volume and sentiment are sharply rising.

Your platform shows increased institutional interest in the past 2 hours.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
NeoDrive, an EV battery company, is up 5% today after Reuters reported:

“NeoDrive is in late-stage talks to supply next-gen batteries for a major automaker’s 2026 lineup.”

Investor call scheduled for tomorrow. Trading volume has spiked 3x above normal.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re watching DeepFarm, an AI agri-tech firm. The USDA just released a grant allocation notice including DeepFarm by name.

Major financial media hasn't reported it yet, but local news confirms the funding.

Volume is rising, and the stock is already up 6% since the notice.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
SolarNex, a mid-cap solar panel producer, jumped 9% today.

CNBC reports:

“SolarNex signed a supply agreement with California’s largest public utility.”

The company confirmed the report via press release.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
BioNova, a pharma firm specializing in Alzheimer’s, surged 10% today.

FDA website now lists its drug trial status as “priority review.”

Multiple major funds have increased their holdings in the past 24 hours.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re monitoring NeuroLoom, a highly volatile AI company that has surged 9% in the past month. Daily price swings of 2-5% are typical.

A forecast from a mid-tier analyst firm states:

“Revenue could climb by 4% next quarter if current R&D partnerships continue performing.”

No major news events, but the company remains exposed to market risk and high development costs.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re monitoring SkyFiber, a space communications firm that has been flat over the past month with erratic day-to-day moves.

An analyst blog speculates:

“SkyFiber might be involved in an upcoming NASA satellite bid. There’s no confirmation, but they’ve been hiring aggressively.”

The information hasn’t been picked up by mainstream financial news.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re monitoring CloudInch, a small cloud storage provider. The stock is up 3% this week, but overall has been flat this quarter.

A junior analyst blog suggests:

“CloudInch may be a quiet acquisition target due to its IP portfolio, but there’s no concrete buzz from major players.”

There’s no market movement beyond normal volatility.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
CloudSpark, a cloud microservices firm, has seen minimal movement over the past month.

A minor tech blog claims:

“A stealth partnership with Oracle might be forming — based on shared infrastructure use.”

No verifiable source and no institutional activity.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re following QuantumNest, a quantum computing startup trading at low volume.

A Reddit user claims to be a recruiter for Google and says:

“We're hiring folks with QuantumNest experience. Something might be brewing.”

No other signs, and the user has no post history.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
GreenPipe, a waste recycling tech firm, is flat this month.

An anonymous comment on an industry blog suggests:

“GreenPipe’s process was reviewed for a city contract in Boston.”

No press coverage or financial data supports this.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re watching IceBridge, a drone logistics firm, which has had erratic volume lately.

A low-traffic blog post claims:

“Rumor is IceBridge has been testing with a large grocery chain.”

There’s no secondary confirmation or market reaction.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re monitoring NeuroLoom, a highly volatile AI company that has surged 9% in the past month. Daily price swings of 2-5% are typical.

A leading analyst firm now predicts:

“NeuroLoom’s revenue is projected to grow by 8% next quarter due to strong demand in AI security integrations.”

No new filings or company statements, but general market conditions are favorable.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re tracking SynthiCore, a biotech firm known for erratic price movement and past trial failures. Despite that, it has gained 7% this month.

Analyst note:

“SynthiCore is expected to announce trial results for its lead drug candidate. Early signs point to strong efficacy, which could boost valuation.”

Market remains skeptical but attentive.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re watching HyperQuant, a fintech firm that has climbed 7% in the last two weeks.

A top-tier firm upgrades its rating, stating:

“HyperQuant’s new payment product is rapidly gaining adoption with mid-sized banks. Growth could accelerate sharply.”

No major media coverage yet, but insider buy volume is slightly up.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re tracking Pathlytics, a SaaS analytics company up 4% this week.

A respected VC firm added it to their “Next 10 Unicorns” shortlist.

There’s no product launch or revenue update yet, but social media mentions are rising.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
MetaShip, a small-cap shipping logistics platform, rose 3.5% this week.

A former exec on LinkedIn said:

“MetaShip’s AI model is outperforming all of our past benchmarks. Watch the Q2 numbers.”

There’s no independent confirmation, but the quote is gaining traction.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
You’re monitoring PayZen, a new digital payments startup.

TechCrunch notes:

“PayZen is being quietly piloted by one of the top five U.S. banks.”

No official statements yet, but app download spikes suggest momentum.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
""",
                 """
SteelRoot, a digital infrastructure firm, climbed 6% over the past week.

A leaked city budget shows potential $200M fiber infrastructure investment in regions where SteelRoot operates heavily.

No response from the company yet.

### Available Actions:
- BUY
- SIT OUT

### Response Format (Strictly Follow This):
Action: <Your chosen action>
Reasoning: <Brief 1-sentence explanation>
End your response here.
"""]
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
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools.llm_router import chat

GOALS_FILE = os.path.expanduser("~/repos/mesh-work/goals.json")

def load_goals():
    with open(GOALS_FILE) as f:
        return json.load(f)

def okr_review():
    goals = load_goals()
    prompt = f"""You are my strategic business advisor. Here are my current OKRs:

{json.dumps(goals, indent=2)}

Give me a concise review of my goals. Are they well-structured? What should I focus on this week?"""
    return chat(prompt, "strategy")

def strategic_question(question):
    goals = load_goals()
    prompt = f"""You are my strategic business advisor. Here are my current OKRs:

{json.dumps(goals, indent=2)}

Question: {question}

Provide a focused, actionable answer."""
    return chat(prompt, "strategy")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(strategic_question(" ".join(sys.argv[1:])))
    else:
        print(okr_review())

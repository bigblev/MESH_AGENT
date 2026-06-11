import os
from dotenv import load_dotenv
import ollama
from tools.context_loader import get_context

load_dotenv()

MODELS = {
    "default": "llama3.2:latest",
    "strategy": "nous-hermes2:34b",
    "strategy-deep": "llama3.1:70b",
    "code": "nous-hermes2:34b",
    "fast": "llama3.2:latest",
}

def chat(prompt, task_type="default"):
    model = MODELS.get(task_type, MODELS["default"])
    context = get_context(prompt)
    full_prompt = context + prompt if context else prompt

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response["message"]["content"]

if __name__ == "__main__":
    import sys
    task = sys.argv[1] if len(sys.argv) > 1 else "default"
    prompt = sys.argv[2] if len(sys.argv) > 2 else input("Prompt: ")
    print(chat(prompt, task))

import os
from dotenv import load_dotenv
import ollama

load_dotenv()

MODELS = {
    "default": "ollama:llama3.2:latest",
    "strategy": "ollama:nous-hermes2:34b",  # Good balance of speed vs quality
    "strategy-deep": "ollama:llama3.1:70b",  # Full power, slower
    "code": "ollama:nous-hermes2:34b",
    "fast": "ollama:llama3.2:latest",
}

def chat(prompt, task_type="default"):
    model = MODELS.get(task_type, MODELS["default"])
    model_name = model.replace("ollama:", "")

    response = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

if __name__ == "__main__":
    import sys
    task = sys.argv[1] if len(sys.argv) > 1 else "default"
    prompt = sys.argv[2] if len(sys.argv) > 2 else input("Prompt: ")
    print(chat(prompt, task))

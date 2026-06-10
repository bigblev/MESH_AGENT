#!/usr/bin/env python3
import sys
import argparse
from tools.llm_router import chat
from agents.strategy_agent import okr_review, strategic_question

def main():
    parser = argparse.ArgumentParser(description="MESH Agent CLI")
    parser.add_argument("prompt", nargs="*", help="Your prompt")
    parser.add_argument("--task", "-t", default="default",
			choices=["default", "strategy", "strategy-deep", "code", "fast"],
                        help="Task type (affects model selection)")
    parser.add_argument("--okr", action="store_true", help="Run OKR review")
    args = parser.parse_args()

    if args.okr:
        print(okr_review())
    elif args.prompt:
        prompt = " ".join(args.prompt)
        if args.task == "strategy":
            print(strategic_question(prompt))
        else:
            print(chat(prompt, args.task))
    else:
        prompt = input("MESH> ")
        print(chat(prompt, "default"))

if __name__ == "__main__":
    main()

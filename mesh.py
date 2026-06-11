#!/usr/bin/env python3
from agents.email_agent import triage_inbox, summarize_email
import sys
import argparse
import subprocess
from agents.memory_agent import save_memory, recall_memory, list_memories
from tools.llm_router import chat
from agents.strategy_agent import okr_review, strategic_question
from agents.github_agent import list_repos, summarize_repo, github_question, list_issues

def sync_memory():
    subprocess.run("git -C ~/repos/mesh-identity pull --ff-only 2>/dev/null", shell=True)
    subprocess.run("git -C ~/repos/mesh-work pull --ff-only 2>/dev/null", shell=True)

def interactive_mode():
    print("MESH Agent — type 'exit' to quit, 'help' for commands")
    while True:
        try:
            user_input = input("\nMESH> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
            elif user_input == 'help':
                print("""
Commands:
  <question>                    General chat
  !okr                          Review OKRs
  !gh-list                      List GitHub repos
  !gh-summarize <repo>          Summarize a repo
  !gh-issues <repo>             List issues
  !gh-ask <question>            GitHub question
  !email-triage                 Triage inbox
  !email-summarize <search>     Summarize email
  !mem-save <content>           Save memory
  !mem-recall <query>           Recall memory
  !mem-list                     List memories
  !strategy <question>          Strategy question (34B)
  !deep <question>              Deep strategy (70B)
                """)
            elif user_input == '!okr':
                print(okr_review())
            elif user_input == '!gh-list':
                print(list_repos())
            elif user_input.startswith('!gh-summarize '):
                print(summarize_repo(user_input[14:]))
            elif user_input.startswith('!gh-issues '):
                print(list_issues(user_input[11:]))
            elif user_input.startswith('!gh-ask '):
                print(github_question(user_input[8:]))
            elif user_input == '!email-triage':
                print(triage_inbox())
            elif user_input.startswith('!email-summarize '):
                print(summarize_email(user_input[17:]))
            elif user_input.startswith('!mem-save '):
                print(save_memory(user_input[10:]))
            elif user_input.startswith('!mem-recall '):
                print(recall_memory(user_input[12:]))
            elif user_input == '!mem-list':
                print(list_memories())
            elif user_input.startswith('!strategy '):
                print(strategic_question(user_input[10:]))
            elif user_input.startswith('!deep '):
                print(chat(user_input[6:], 'strategy-deep'))
            else:
                print(chat(user_input, 'default'))
        except KeyboardInterrupt:
            print("\nType 'exit' to quit")

def main():
    sync_memory()
    parser = argparse.ArgumentParser(description="MESH Agent CLI")
    parser.add_argument("prompt", nargs="*", help="Your prompt")
    parser.add_argument("--task", "-t", default="default",
                        choices=["default", "strategy", "strategy-deep", "code", "fast"],
                        help="Task type (affects model selection)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--email-triage", action="store_true", help="Triage inbox")
    parser.add_argument("--email-summarize", metavar="SEARCH", help="Summarize an email")
    parser.add_argument("--okr", action="store_true", help="Run OKR review")
    parser.add_argument("--gh-list", action="store_true", help="List GitHub repos")
    parser.add_argument("--gh-summarize", metavar="REPO", help="Summarize a GitHub repo")
    parser.add_argument("--gh-issues", metavar="REPO", help="List issues for a repo")
    parser.add_argument("--gh-ask", metavar="QUESTION", help="Ask a GitHub question")
    parser.add_argument("--mem-save", metavar="CONTENT", help="Save a memory")
    parser.add_argument("--mem-recall", metavar="QUERY", help="Recall a memory")
    parser.add_argument("--mem-list", action="store_true", help="List all memories")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.okr:
        print(okr_review())
    elif args.gh_list:
        print(list_repos())
    elif args.gh_summarize:
        print(summarize_repo(args.gh_summarize))
    elif args.gh_issues:
        print(list_issues(args.gh_issues))
    elif args.gh_ask:
        print(github_question(args.gh_ask))
    elif args.mem_save:
        print(save_memory(args.mem_save))
    elif args.mem_recall:
        print(recall_memory(args.mem_recall))
    elif args.mem_list:
        print(list_memories())
    elif args.email_triage:
        print(triage_inbox())
    elif args.email_summarize:
        print(summarize_email(args.email_summarize))
    elif args.prompt:
        prompt = " ".join(args.prompt)
        if args.task == "strategy" or args.task == "strategy-deep":
            print(strategic_question(prompt))
        else:
            print(chat(prompt, args.task))
    else:
        interactive_mode()

if __name__ == "__main__":
    main()

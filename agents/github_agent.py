import os
import sys
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools.llm_router import chat

def run_gh(command):
    env = os.environ.copy()
    env.pop("GITHUB_TOKEN", None)  # Remove conflicting token
    result = subprocess.run(
        f"gh {command}",
        shell=True,
        capture_output=True,
        text=True,
        env=env
    )
    return result.stdout or result.stderr

def list_repos():
    return run_gh("repo list")

def list_issues(repo):
    return run_gh(f"issue list --repo {repo}")

def create_issue(repo, title, body):
    return run_gh(f'issue create --repo {repo} --title "{title}" --body "{body}"')

def summarize_repo(repo):
    readme = run_gh(f"api repos/{repo}/readme --jq '.content' | base64 -d")
    issues = run_gh(f"issue list --repo {repo}")
    prompt = f"""Summarize this GitHub repository for me.

README:
{readme}

Open Issues:
{issues}

Give a concise summary of what this repo does and what needs attention."""
    return chat(prompt, "fast")

def github_question(question):
    repos = list_repos()
    prompt = f"""You are my GitHub assistant. Here are my repositories:

{repos}

Question: {question}

Provide a focused, actionable answer. If you need to run gh commands, suggest them."""
    return chat(prompt, "fast")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python github_agent.py <command> [args]")
        print("Commands: list, issues <repo>, summarize <repo>, ask <question>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        print(list_repos())
    elif cmd == "issues" and len(sys.argv) > 2:
        print(list_issues(sys.argv[2]))
    elif cmd == "summarize" and len(sys.argv) > 2:
        print(summarize_repo(sys.argv[2]))
    elif cmd == "ask":
        print(github_question(" ".join(sys.argv[2:])))

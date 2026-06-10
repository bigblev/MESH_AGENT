import os
import sys
import json
import subprocess
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools.llm_router import chat

IDENTITY_DIR = os.path.expanduser("~/repos/mesh-identity")
WORK_DIR = os.path.expanduser("~/repos/mesh-work")

def git_push(repo_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    cmd = f"cd {repo_dir} && git add . && git commit -m '[arni] memory update {timestamp}' && git push"
    subprocess.run(cmd, shell=True, capture_output=True)

def git_pull(repo_dir):
    subprocess.run(f"cd {repo_dir} && git pull --ff-only", 
                   shell=True, capture_output=True)

def save_memory(content, domain="work", filename=None):
    git_pull(WORK_DIR if domain == "work" else IDENTITY_DIR)
    repo_dir = WORK_DIR if domain == "work" else IDENTITY_DIR
    if not filename:
        filename = f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(repo_dir, filename)
    with open(filepath, "w") as f:
        f.write(f"---\ndate: {datetime.now().isoformat()}\ndomain: {domain}\n---\n\n{content}")
    update_index(repo_dir, filename, content[:80])
    git_push(repo_dir)
    return f"Memory saved to {filename}"

def update_index(repo_dir, filename, summary):
    index_path = os.path.join(repo_dir, "MEMORY.md")
    with open(index_path, "r") as f:
        contents = f.read()
    entry = f"\n- [{filename}]({filename}) — {summary}"
    if filename not in contents:
        with open(index_path, "a") as f:
            f.write(entry)

def recall_memory(query, domain="work"):
    git_pull(WORK_DIR if domain == "work" else IDENTITY_DIR)
    repo_dir = WORK_DIR if domain == "work" else IDENTITY_DIR
    memories = []
    for f in os.listdir(repo_dir):
        if f.endswith(".md") and f != "MEMORY.md":
            with open(os.path.join(repo_dir, f)) as fh:
                memories.append(fh.read())
    if not memories:
        return "No memories found."
    combined = "\n\n---\n\n".join(memories)
    prompt = f"""Here are my saved memories:

{combined}

Question: {query}

Answer based only on what is in my memories."""
    return chat(prompt, "fast")

def list_memories(domain="work"):
    repo_dir = WORK_DIR if domain == "work" else IDENTITY_DIR
    index_path = os.path.join(repo_dir, "MEMORY.md")
    with open(index_path) as f:
        return f.read()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python memory_agent.py <save|recall|list> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "save":
        content = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else input("Memory content: ")
        print(save_memory(content))
    elif cmd == "recall":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else input("What do you want to recall? ")
        print(recall_memory(query))
    elif cmd == "list":
        print(list_memories())

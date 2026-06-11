import os
import yaml

MEMORY_DIRS = [
    os.path.expanduser("~/repos/mesh-work"),
    os.path.expanduser("~/repos/mesh-identity"),
]
MEMORY_MAP = os.path.expanduser("~/repos/MESH_AGENT/config/memory_map.yaml")

def load_memory_map():
    with open(MEMORY_MAP) as f:
        return yaml.safe_load(f)

def read_memory_file(filename):
    for directory in MEMORY_DIRS:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
    return None

def get_context(prompt):
    try:
        memory_map = load_memory_map()
    except Exception:
        return ""

    loaded_files = set()
    context_parts = []

    # Always load base context
    for filename in memory_map.get("base_context", []):
        if filename not in loaded_files:
            content = read_memory_file(filename)
            if content:
                context_parts.append(content)
                loaded_files.add(filename)

    # Load keyword-matched context
    prompt_lower = prompt.lower()
    for keyword, files in memory_map.get("keywords", {}).items():
        if keyword in prompt_lower:
            for filename in files:
                if filename not in loaded_files:
                    content = read_memory_file(filename)
                    if content:
                        context_parts.append(content)
                        loaded_files.add(filename)

    if not context_parts:
        return ""

    return "## My Context\n\n" + "\n\n---\n\n".join(context_parts) + "\n\n## Your Question\n\n"

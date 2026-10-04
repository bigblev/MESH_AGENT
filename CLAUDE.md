# MESH_AGENT — instructions for Claude

## ⛔ THIS REPOSITORY IS PUBLIC. NEVER COMMIT CLIENT OR BUSINESS MATERIAL HERE.

Anything committed here is readable by anyone on the internet, immediately and permanently. Deleting a branch afterwards does **not** remove it — the objects stay fetchable by commit SHA until GitHub Support garbage-collects the repo.

**Never put in this repo:**
- Client work of any kind — Pixelworks, Chaos, Leica, Grade A Pictures, or any other engagement
- Meeting notes, transcripts, call summaries, strategy, pricing, org charts, or named contacts
- Credentials: tokens, API keys, passwords, secret URLs. `.env` is gitignored and must stay untracked — use `.env.example` for the template
- Anything from the private Hive Mind repos (mesh-work, mesh-identity, mesh-private, mesh-home, mesh-playtime)

**Where that material goes instead** (private repos, on James's machines, not in this container):
| Content | Repo |
|---|---|
| Clients, projects, meetings, business | `mesh-work` |
| Preferences, feedback, cross-machine to-dos | `mesh-identity` |
| Credentials and access procedures | `mesh-private` |
| House, home network, Home Assistant | `mesh-home` |
| Games and hobbies | `mesh-playtime` |

**If you have client material to save and those repos are not available in this session — which is normal in a Cowork/cloud container — do not improvise a location. Say so and hand the content back to James.** Do not create a `memory/` directory here, do not append it to an existing file here, and do not open a branch for it.

**Why this file exists:** on 2026-07-16 a Cowork session with no knowledge of the Hive Mind repos needed somewhere to save Pixelworks notes, found no `memory/` directory, created one, and committed a client meeting transcript to a branch of this public repo. It stayed public for about eleven weeks. The content was already captured in `mesh-work` and in Craft, so nothing was lost — but it should never have been published.

## What this repo is for
MESH Agent CLI: a local agent stack that runs on Arni (Framework desktop, Ubuntu, Ollama). Agents for email, calendar, GitHub, memory, and strategy, plus an LLM router and a context loader. Code, configuration, and documentation only.

## Working notes
- Python venv at `venv/`, untracked. Rebuild with `python3 -m venv venv && venv/bin/pip install -r requirements.txt`.
- `tools/context_loader.py` reads memory files from the private Hive Mind clones at `~/repos/`. Those paths are referenced here but their content belongs there, never committed here.
- `agents/github_agent.py` deliberately strips `GITHUB_TOKEN` from the environment and relies on the `gh` CLI login. Keep it that way.

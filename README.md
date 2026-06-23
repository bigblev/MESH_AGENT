# MESH AGENT 🤖
### Multi-model Enterprise Strategy & Handler

> **MESH** — **M**ulti-model **E**nterprise **S**trategy & **H**andler

MESH is a personal business automation agent designed to handle the operational overhead of running a business — so you can focus on strategy, decisions, and growth. It is **model-agnostic**, meaning you can swap between Claude, GPT-4, Gemini, or any future model without changing your workflows.

MESH also includes **Hive Mind** — a git-backed memory sync layer that keeps your agent's context consistent across every machine you work from.

---

## 🧭 Vision

Most business owners spend 60–70% of their time on reactive work: sorting emails, scheduling meetings, chasing updates. MESH flips this by handling the reactive layer and surfacing only what truly needs your attention — turning your time toward strategy, goal-setting, and high-value decisions.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        MESH AGENT                           │
│                                                             │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────────┐  │
│  │  LLM ROUTER  │   │  TOOL LAYER  │   │   HIVE MIND    │  │
│  │              │   │              │   │  (Memory Sync) │  │
│  │  • Claude    │   │  • Gmail     │   │                │  │
│  │  • GPT-4     │   │  • Calendar  │   │  • Goals/OKRs  │  │
│  │  • Gemini    │   │  • Slack     │   │  • Contacts    │  │
│  │  • Local LLM │   │  • GitHub    │   │  • Decisions   │  │
│  └──────────────┘   │  • CRM       │   │  • Context     │  │
│                     └──────────────┘   └────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    AGENT MODULES                     │   │
│  │                                                      │   │
│  │  📧 EMAIL AGENT      📊 STRATEGY AGENT               │   │
│  │  • Triage & sort     • Goal tracking (OKRs)          │   │
│  │  • Priority scoring  • Business reviews              │   │
│  │  • Draft replies     • Decision logging              │   │
│  │  • Auto-labels       • Market/competitor intel       │   │
│  │                                                      │   │
│  │  📅 CALENDAR AGENT   🔗 INTEGRATIONS AGENT           │   │
│  │  • Meeting prep      • GitHub project sync           │   │
│  │  • Agenda summaries  • CRM updates                   │   │
│  │  • Scheduling assist • Slack digests                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Agent Modules

### 1. 🔀 LLM Router (Model-Agnostic Core)
The heart of MESH. All agent calls go through the router, which selects and calls the appropriate model based on task type, cost, and configured preference.

**Key design decisions:**
- All prompts are stored as templates in `/prompts/` — model-independent
- Model selection can be set per-task-type (e.g., "use Claude for strategy, GPT-4 for code")
- Supports fallback chains (primary model → secondary model → tertiary)
- API keys managed via `.env` — never hardcoded

**Supported Models:**
| Provider | Models | Best For |
|----------|--------|----------|
| Anthropic | claude-sonnet-4-6, claude-opus-4-6 | Strategy, writing, analysis |
| OpenAI | gpt-4o, o1, o3-mini | Coding, structured output |
| Google | gemini-1.5-pro, gemini-flash | Multimodal, long context |
| Local | Ollama (llama3, mistral) | Private/sensitive tasks |

---

### 2. 📧 Email Agent
Handles the full email lifecycle — triage, prioritization, drafting, and follow-up tracking.

**Capabilities:**
- **Triage**: Scans inbox and classifies emails by type (action required, FYI, newsletter, etc.)
- **Priority Scoring**: Scores emails 1–5 based on sender importance, urgency signals, and business context
- **Draft Replies**: Generates context-aware reply drafts for high-priority emails
- **Labels & Folders**: Auto-applies Gmail labels based on classification
- **Follow-up Tracking**: Flags emails awaiting response after N days

**Priority Scoring Criteria:**
```
Score 5 (Urgent)   : Client issues, legal, time-sensitive opportunities
Score 4 (High)     : Key partners, active deals, team blockers
Score 3 (Normal)   : General business, colleagues, scheduled items
Score 2 (Low)      : Newsletters, non-urgent FYI
Score 1 (Archive)  : Promotional, spam-adjacent
```

**Scheduled Tasks:**
- `morning_triage` — Runs 7:30am, summarizes overnight emails + priority queue
- `eod_digest` — Runs 5pm, flags unanswered high-priority emails

---

### 3. 📊 Strategy Agent
Your AI business partner for goal setting, strategic planning, and decision support.

**Capabilities:**
- **OKR Management**: Define and track Objectives & Key Results by quarter
- **Weekly Business Reviews**: Auto-generates review docs from connected data
- **Decision Log**: Records major decisions with context and rationale
- **Strategic Briefings**: On-demand analysis of market trends, competitors, or opportunities
- **Goal Accountability**: Weekly check-ins on progress against stated goals

**Goal Framework:**
```
Annual Vision
└── Q1 Objectives (3–5)
    └── Key Results (3–5 per Objective, measurable)
        └── Weekly Initiatives (specific actions)
```

---

### 4. 📅 Calendar Agent
Optimizes your time and ensures you're prepared for every meeting.

**Capabilities:**
- **Meeting Prep**: Generates briefing docs before meetings (attendees, agenda, context)
- **Scheduling Suggestions**: Finds optimal meeting times based on preferences
- **Agenda Builder**: Creates structured agendas from meeting objectives
- **Post-Meeting Actions**: Extracts and logs action items after meetings

---

### 5. 🔗 Integrations Agent
Keeps all your tools in sync without manual effort.

| Tool | Purpose |
|------|---------|
| **GitHub** | Code/config storage, project management, agent versioning |
| **Slack** | Team digests, notifications, async updates |
| **Google Calendar** | Scheduling, meeting prep |
| **Gmail** | Email triage (see Email Agent) |
| **CRM (HubSpot / Notion / other)** | Contact sync, deal tracking |

---

## 🧠 Hive Mind — Cross-Machine Memory Sync

MESH uses a git-backed memory sync system so your agent's context stays consistent across every machine you work from. Without this, context learned on one machine doesn't exist on others — you'd be re-explaining who you are, how you work, and what you're building every time you switch devices.

**The key insight: not all memory should go everywhere.** Different machines have different roles and security boundaries. Hive Mind uses domain-scoped repos with an access matrix so each machine sees only what it should.

### Memory Architecture

Instead of one shared folder, memory is split into domains — each gets its own private GitHub repo:

| Repo | Domain | Contents |
|------|--------|----------|
| `mesh-identity` | Universal | User profile, preferences, feedback rules |
| `mesh-work` | Business / MESH | OKRs, decisions, client context, strategies |
| `mesh-private` | Sensitive | API keys, credentials, personal data |

### How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Work Laptop   │     │  Home Desktop   │     │  Headless/CI    │
│                 │     │                 │     │                 │
│  Claude/MESH    │     │  Claude/MESH    │     │  Automated jobs │
│  ↕ read/write   │     │  ↕ read/write   │     │  ↕ read-only    │
│  mesh-work      │     │  mesh-work      │     │  mesh-identity  │
│  mesh-identity  │     │  mesh-identity  │     │                 │
│  mesh-private   │     │  mesh-private   │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
                          ┌──────┴──────┐
                          │   GitHub    │
                          │  (private   │
                          │   repos)    │
                          └─────────────┘
```

1. **Session start** → Hook fires on first `Read` call → `git pull --ff-only` on all memory repos
2. **Agent needs context** → Reads `MEMORY.md` index → Reads specific memory files
3. **Agent writes a memory** → Writes to correct repo → Commits with `[machine-name]` prefix → Pushes to GitHub
4. **Next session on any machine** → Hook pulls → Memory is available everywhere

### Quickstart

**Step 1 — Create your memory repos:**
```bash
gh repo create mesh-identity --private
gh repo create mesh-work --private
```

**Step 2 — Clone on each machine:**
```bash
mkdir -p ~/repos
gh repo clone bigblev/mesh-identity ~/repos/mesh-identity
gh repo clone bigblev/mesh-work ~/repos/mesh-work
```

**Step 3 — Create `~/.claude/CLAUDE.md`:**
```markdown
## MESH Memory

This machine has access to the following memory repos:
- **mesh-identity**: ~/repos/mesh-identity/ (read-write)
- **mesh-work**: ~/repos/mesh-work/ (read-write)

### Rules
- On session start, pull memory repos before reading
- When you need context, read the relevant repo's MEMORY.md index first
- After writing memories, commit and push to the appropriate repo
- Use [machine-name] prefix in all commit messages
```

**Step 4 — Add the auto-pull hook to `~/.claude/settings.json`:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Read",
      "hooks": [{
        "type": "command",
        "command": "git -C ~/repos/mesh-identity pull --ff-only 2>/dev/null; git -C ~/repos/mesh-work pull --ff-only 2>/dev/null; true"
      }]
    }]
  }
}
```

### Memory File Format

Each memory is a separate `.md` file with frontmatter. The `MEMORY.md` in each repo is a short index of one-line pointers.

**User memory** (who you are):
```markdown
---
name: User profile
description: James's background, goals, and collaboration style
type: user
---
Business owner at MESH VP. Building model-agnostic agentic workflows.
Prefers concise responses. Uses Claude as primary agent via Cowork.
```

**Feedback memory** (how to work with you):
```markdown
---
name: Response style
description: Preferred response format and length
type: feedback
---
Keep responses concise. No trailing summaries after completing tasks.

**Why:** Reduces noise, faster to scan.
**How to apply:** State result, then stop. Don't recap what was just done.
```

**Project memory** (current work):
```markdown
---
name: MESH Agent status
description: Current phase and next priorities
type: project
---
Phase 1 in progress. Strategy Hub live. Calendar connected.
Next: email triage automation, push README to GitHub.

**Why:** Tracking active build state.
**How to apply:** Reference when planning next tasks.
```

### Commit Convention

Tag every commit with the machine name so `git log` shows which Claude wrote what:
```
[work-laptop] updated OKRs after Q2 review
[home-desktop] added decision log entry — Hallstone partnership
[cowork] saved new contact context for Chaos team
```

---

## 🗂️ Repository Structure

```
MESH_AGENT/
├── README.md                  ← You are here
├── .env.example               ← API key template (never commit .env)
│
├── config/
│   ├── models.yaml            ← LLM routing rules
│   ├── integrations.yaml      ← Tool connection settings
│   └── agent_settings.yaml    ← Per-agent config
│
├── agents/
│   ├── email_agent.py         ← Email triage & reply logic
│   ├── strategy_agent.py      ← OKR & strategy logic
│   ├── calendar_agent.py      ← Calendar management
│   └── integrations_agent.py  ← Cross-tool sync
│
├── prompts/
│   ├── email_triage.md        ← Email classification prompt
│   ├── priority_scoring.md    ← Email priority prompt
│   ├── strategy_review.md     ← Business review prompt
│   ├── okr_coach.md           ← OKR coaching prompt
│   └── meeting_prep.md        ← Meeting briefing prompt
│
├── memory/
│   ├── goals.json             ← Current OKRs and goals
│   ├── decisions.json         ← Decision log
│   ├── contacts.json          ← Key contact context
│   └── context.md             ← Business context for LLM grounding
│
├── tools/
│   ├── gmail_client.py        ← Gmail API wrapper
│   ├── calendar_client.py     ← Google Calendar wrapper
│   ├── slack_client.py        ← Slack API wrapper
│   ├── github_client.py       ← GitHub API wrapper
│   └── llm_router.py          ← Model-agnostic LLM caller
│
├── schedules/
│   ├── morning_triage.yaml    ← 7:30am email digest
│   ├── eod_digest.yaml        ← 5pm follow-up check
│   └── weekly_review.yaml     ← Friday strategy review
│
├── hive-mind/
│   ├── settings.json          ← Claude hook template (auto-pull)
│   ├── CLAUDE.md.template     ← CLAUDE.md template for each machine
│   └── headless-sync.sh       ← Cron/launchd sync helper
│
└── ui/
    └── strategy_hub.html      ← Business Strategy Hub dashboard
```

---

## 🚀 Getting Started

### Step 1: Clone the repo
```bash
git clone https://github.com/bigblev/MESH_AGENT.git
cd MESH_AGENT
```

### Step 2: Set up your environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

**Required API Keys** (add to `.env`):
```
# Choose your primary LLM
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_AI_API_KEY=...

# Tool integrations
GMAIL_CREDENTIALS_PATH=./credentials/gmail_oauth.json
SLACK_BOT_TOKEN=xoxb-...
GITHUB_TOKEN=ghp_...
```

### Step 3: Configure your model preferences
Edit `config/models.yaml`:
```yaml
default_model: claude-sonnet-4-6   # Primary model for most tasks
strategy_model: claude-opus-4-6    # Deep reasoning tasks
code_model: gpt-4o                 # Code generation
fast_model: claude-haiku-4-5       # Quick classifications
fallback_model: gpt-4o-mini        # If primary fails
```

### Step 4: Set up Hive Mind memory sync
Follow the [Hive Mind Quickstart](#quickstart) above to create your memory repos and configure the auto-pull hook on each machine.

### Step 5: Add your business context
Edit `memory/context.md` with:
- What your business does
- Key clients and partners
- Current priorities and goals
- Tone and communication style preferences

### Step 6: Set your goals
Edit `memory/goals.json` with your current OKRs:
```json
{
  "annual_vision": "Build the leading model-agnostic agentic platform for business operators",
  "q2_2026": {
    "objectives": [
      {
        "title": "Establish MESH Agent foundation",
        "key_results": [
          "Email triage automation live by May 31",
          "Strategy Hub in daily use",
          "Hive Mind syncing across all machines"
        ]
      }
    ]
  }
}
```

---

## 🔄 Workflows

### Morning Routine (automated)
```
7:30am → Email Agent runs triage
       → Scores and labels all overnight emails
       → Sends Slack digest: "Good morning! You have X priority emails"
       → Prepares draft replies for Score 4–5 emails
       → Shows today's calendar with meeting prep notes
```

### Weekly Strategy Review (automated)
```
Friday 4pm → Strategy Agent runs review
           → Checks OKR progress (from goals.json)
           → Summarizes week's decisions
           → Highlights blockers and risks
           → Drafts next week's key priorities
           → Saves review doc to GitHub
```

### On-Demand Queries (via Cowork / Claude)
- "Summarize my inbox from the last 24 hours"
- "Draft a reply to [contact] about [topic]"
- "How are we tracking against Q2 OKRs?"
- "Help me think through this strategic decision: [context]"
- "Prepare me for my 2pm meeting with [company]"

---

## 🧩 Design Principles

1. **Model-Agnostic**: Prompts, logic, and data are decoupled from any specific LLM
2. **Memory Everywhere**: Hive Mind keeps context consistent across every machine
3. **Privacy First**: Sensitive context stays in private repos; choose which data goes where
4. **Human-in-the-Loop**: Agent drafts and suggests; you approve and send
5. **Transparent**: Every agent action is logged; nothing happens silently
6. **Composable**: Each module works standalone; combine as needed
7. **Version-Controlled**: All configs, prompts, goals, and memories live in Git

---

## 🔐 Token Security

GitHub 2FA is more than adequate for most personal projects — it protects your repo from unauthorized access and is the right baseline for any public or private repository.

That said, some security strategies require a step further: **keeping tokens somewhere secret and separately accessible** from the codebase itself.

This matters when:
- You're running agents on a headless server or shared machine where file system access is broader
- Your repo is public (like this one) and a `.gitignore` miss could expose credentials
- You need tokens accessible across machines without committing them to git

**Options worth knowing:**

| Approach | Best For |
|----------|----------|
| `.env` file + `.gitignore` | Local dev — simple and sufficient for private machines |
| OS keychain (macOS Keychain, Linux Secret Service) | Single-machine setups where you want system-level encryption at rest |
| Password manager with CLI API (1Password, Bitwarden) | Multi-machine access — retrieve tokens programmatically without storing them in files |
| Private `mesh-private` git repo (Hive Mind domain) | Secrets that need to sync across machines but stay out of the main codebase |
| Secret management service (HashiCorp Vault, AWS Secrets Manager) | Team or production deployments where multiple services need credential access |

MESH follows the `.env` + `.gitignore` + `credentials/` gitignore approach by default. If your threat model requires stronger isolation, the `mesh-private` Hive Mind repo pattern gives you git-synced secrets in a private repo that never touches the public `MESH_AGENT` codebase.

---

## 📍 Roadmap

### Phase 1 — Foundation (In Progress)
- [x] Repository structure & README
- [x] Business Strategy Hub dashboard (Cowork artifact)
- [x] Gmail + Google Calendar connected
- [ ] Hive Mind memory repos created & syncing
- [ ] OKRs populated in Strategy Hub
- [ ] Email triage automation (morning digest)

### Phase 2 — Automation
- [ ] LLM router with model switching
- [ ] Morning email digest (scheduled)
- [ ] Weekly strategy review automation
- [ ] Meeting prep agent

### Phase 3 — Intelligence
- [ ] Contact relationship mapping
- [ ] Deal/opportunity tracking from email
- [ ] Competitor intelligence briefings
- [ ] Predictive priority scoring

### Phase 4 — Expansion
- [ ] CRM integration (HubSpot/Notion)
- [ ] Voice interface (briefings on the go)
- [ ] Mobile notifications
- [ ] Team collaboration features

---

## 📄 License

Private — for personal business use.

---

*Built with Claude (Anthropic). Designed to work with any LLM. Memory synced with Hive Mind.*


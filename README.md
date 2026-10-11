# 💼 Autonomous CRM Lead Qualification Agent

> *"The intelligent sales enablement layer that autonomously synthesizes B2B enrichment data, CRM history, and deterministic business rules into executive-ready discovery briefs."*

---

## Part 1: Project Overview & Value Proposition

### 1️⃣ Project Title & Value Proposition
* **Agent Type:** Stateful Agentic Orchestrator with Mock Tool Calling (OpenRouter / GPT-4o-mini)
* **Primary User:** Sales Development Representatives (SDRs) & Revenue Operations
* **Outcome:** Reduces manual lead research time by ~70% and standardizes qualification criteria across outbound pipelines.

### 2️⃣ Background & Problem Context
In high-velocity outbound sales environments, SDRs waste 3 to 4 hours daily manually cross-referencing prospect email domains across third-party enrichment tools (like Clearbit) and CRM databases (like Salesforce). This manual friction leads to inconsistent qualification, missed historical interactions, and poorly prepared discovery calls.

### 3️⃣ Target User & Job To Be Done (JTBD)
* **Primary User:** Sales Development Representatives managing high-volume outbound campaigns.
* **JTBD:** Instantly input a prospect email, trigger automated firmographic enrichment and CRM history retrieval, and receive an AI-synthesized sales briefing within seconds.

### 4️⃣ Why an Agentic Approach
Traditional scripts break down when data fields are missing, and rigid workflow automation tools lack the contextual reasoning required to interpret ambiguous CRM statuses (e.g., reconciling a "Cold Lead" history with a high-revenue enterprise domain). An orchestrator pattern is necessary to sequence tool execution dynamically and apply robust fallback logic.

### 5️⃣ Agent Role, Scope & Autonomy Level
* **Autonomy Level:** Semi-autonomous research and synthesis. The agent extracts domains, executes mock API lookups, applies business scoring rules, and generates executive summaries while keeping human SDRs strictly in control of final outreach.

### 6️⃣ Agent Architecture & Components
* **Planner & Orchestrator (`agent_orchestrator.py`):** Coordinates regex domain extraction, tool invocation, score computation, and LLM prompt generation.
* **Executor Layer (`enrichment_tool.py`, `crm_tool.py`):** Idempotent mock tool functions returning structured B2B firmographic profiles and CRM interaction logs.
* **Presentation Layer (`app.py`):** Interactive Streamlit web interface featuring sidebar preset testing, metric scorecards, and expandable raw tool data views.

### 7️⃣ Tools, Models & Stack
* **Streamlit (`1.38.0`):** Lightweight internal UI framework for rapid agent prototyping.
* **LangChain & LangChain OpenAI (`0.3+`):** Robust abstraction layers for prompt management and LLM integration.
* **OpenRouter Gateway:** Unified API routing providing flexibility to switch between high-performance reasoning models without vendor lock-in.
* **Python RegEx & Pydantic:** Core utilities for string parsing and type validation.

---

## Part 2: Repository Structure & Getting Started

### Project Layout
```text
CRMLeadAgent/
├── .env                    # Secure environment configuration (ignored by git)
├── .gitignore              # Git exclusion rules (.venv/, .env)
├── .venv/                  # Python virtual environment
├── requirements.txt        # Tracked project dependencies
└── src/                    # Enterprise source package
    ├── core/
    │   └── config.py       # Centralized configuration & OpenRouter settings
    ├── services/
    │   ├── enrichment_tool.py # Mock Clearbit B2B enrichment API
    │   ├── crm_tool.py        # Mock Salesforce CRM lookup API
    │   └── agent_orchestrator.py # Core reasoning, scoring & LLM synthesis loop
    └── ui/
        └── app.py          # Streamlit SDR dashboard presentation layer
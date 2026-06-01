# 🔬 Research Agent — Multi-Agent AI System

**An intelligent research assistant that autonomously searches, scrapes, writes, and critiques research reports.**

Powered by **LangChain**, **Groq LLM**, and **Streamlit**, this system orchestrates four specialized AI agents to produce polished, fact-based research reports on any topic.

---

## ✨ Features

- **🔍 Search Agent** — Gathers recent, reliable information via Tavily web search
- **📄 Reader Agent** — Intelligently selects and scrapes deep content from URLs
- **✍️ Writer Agent** — Synthesizes findings into a structured, professional report
- **🧐 Critic Agent** — Evaluates report quality and provides constructive feedback
- **🎨 Interactive UI** — Beautiful Streamlit dashboard with real-time pipeline progress
- **💻 CLI Support** — Pure Python execution for headless/automation workflows

---

## 🏗️ Architecture

**Agent Stack:**

- **LLM**: Groq (meta-llama/llama-4-scout-17b-16e-instruct)
- **Framework**: LangChain + LangGraph
- **Search**: Tavily API
- **Scraping**: trafilatura, readability-lxml, BeautifulSoup4
- **UI**: Streamlit

---

## 🚀 Setup

### Prerequisites

- Python 3.10+
- pip or conda
- API keys for **Groq** and **Tavily**

### 1. Clone & Install

```bash
cd Research-Agent-Multi-Agent-AI-System
python -m venv .venv

# On Windows
.\.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment

- Create a .env file in the project root:

```bash
API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

📁 Project Structure

```bash
Research-Agent-Multi-Agent-AI-System/
├── main.py # CLI entry point
├── app.py # Streamlit UI
├── requirements.txt # Dependencies
├── .env # API keys (not in repo)
└── src/
├── agents/
│ └── agents.py # Search, Reader, Writer, Critic
├── pipelines/
│ └── pipeline.py # Orchestration logic
└── tools/
└── tools.py # web_search & scrape_url

```

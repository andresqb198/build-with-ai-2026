# Build with AI Medellín 2026

**AI Reliability & Observability Workshop**

A hands-on workshop where you act as the new AI Reliability Team at Google Cloud. Your mission: stabilize and observe a flawed AI incident response system using LangGraph, Gemini, and Langfuse.

## Architecture

```
START → classify_incident
  ├──[low severity]──→ propose_mitigation ──→ generate_summary → END
  └──[med/high/critical]──→ analyze_logs → propose_mitigation
                                ↑                    │
                                └──[reanalysis loop]─┘
                                         │
                                    [done or max 3]
                                         ↓
                                  generate_summary → END
```

**Agents:**
- **Incident Classifier** — Categorizes incidents by type and severity
- **Log Analyzer** — Analyzes traces, spans, and metrics to identify root causes
- **Mitigation Specialist** — Proposes fixes based on analysis and runbooks
- **Executive Summary** — Creates leadership-ready summaries

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

## Quick Start

```bash
# 1. Clone and enter the project
git clone https://github.com/andresqb198/build-with-ai-2026.git
cd build-with-ai-2026

# 2. Setup environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 3. Install dependencies and start services
make setup
make start

# 4. Open Langfuse and create an account
# Visit http://localhost:3000
# Create a project and copy the API keys to your .env file

# 5. Run the system
make run
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Gemini API key |
| `LANGFUSE_PUBLIC_KEY` | Yes* | From Langfuse project settings |
| `LANGFUSE_SECRET_KEY` | Yes* | From Langfuse project settings |
| `LANGFUSE_HOST` | No | Default: `http://localhost:3000` |

*Required for tracing. Configure after Langfuse first launch.

## Langfuse Setup

1. Run `make start` to launch Langfuse
2. Open http://localhost:3000
3. Create an account (local only, no email verification needed)
4. Create a new project
5. Go to **Settings → API Keys** and copy the keys to your `.env` file

## Available Commands

```bash
make help       # Show all commands
make setup      # Install dependencies
make start      # Start Langfuse + validate env
make run        # Run the incident response system
make stop       # Stop Langfuse
make reset      # Reset all Langfuse data
make validate   # Check environment setup
```

## Project Structure

```
app/
├── agents/         # Agent implementations (classifier, analyzer, mitigation, summary)
├── graphs/         # LangGraph orchestration and state definition
├── prompts/        # Prompt templates for each agent
├── tools/          # Tool functions (data loading, trace analysis, runbooks)
├── datasets/       # Local JSON datasets (incidents, traces, metrics)
├── telemetry/      # Langfuse integration
├── main.py         # CLI entry point
└── config.py       # Environment configuration
langfuse/
└── docker-compose.yml
scripts/
├── start.sh        # Full setup script
├── reset.sh        # Reset workshop state
└── validate_env.sh # Environment validation
```

## Workshop

Select an incident from the dashboard, run the agent pipeline, and observe the execution in Langfuse. Look for:

- Execution traces and span timelines
- Token usage per agent step
- Latency patterns across the pipeline
- Agent decision flows and routing
- Anomalies in the trace data

The system has intentional issues for you to discover through observability. Happy debugging!

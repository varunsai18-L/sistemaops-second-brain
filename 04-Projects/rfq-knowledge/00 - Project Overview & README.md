# Project Viability Management System

Base setup for an AI-powered RFQ evaluation and competency matching system.

Prepared by: Palak Nagar

## PVMS 2.0

Advanced RFQ Intelligence, an explainable 5-dimension AI Risk Engine,
role-based Smart Cost Estimation, Historical Project Matching, Capacity
Planning, Proposal Generation, an Executive Dashboard, Competitive
Intelligence and a lightweight Knowledge Graph have all been added on
top of the base system below, coordinated by a Parser/Technical/Finance/
Risk/Proposal/Reviewer multi-agent pipeline (`src/pvms/agents/`). See
[`docs/PVMS_2_0_IMPLEMENTATION_STATUS.md`](docs/PVMS_2_0_IMPLEMENTATION_STATUS.md)
for exactly what shipped vs. what still needs real infrastructure
(Postgres/Neo4j/FastAPI/React) to go further.

## Purpose

This project is planned to help the team review client RFQs before accepting a project. The system will read the RFQ, identify the main requirements, compare them with available employee skills, check basic risk and budget fit, suggest a possible team, and finally give one of these recommendations:

- `GO`
- `GO WITH CAUTION`
- `NO-GO`

For the base setup, I have kept the project Python-based and arranged the folders so each major part of the system has a clear place.

- Streamlit can be used for the first internal UI.
- Ollama can be used for running the AI model locally.
- LangGraph can be used for the RFQ analysis workflow.
- MongoDB can store employee skills, availability, past projects, and assessment results.
- PyMuPDF, pdfplumber, and python-docx can be used for reading RFQ documents.
- Mermaid or Graphviz can be used later for diagrams.

## Requirement Mapping

| Requirement from proposal | Folder/module |
| --- | --- |
| Upload and parse RFQs | `app/`, `src/pvms/parsers/` |
| Extract requirements, constraints, skills, timelines, deliverables | `src/pvms/ai/`, `src/pvms/workflows/` |
| Classify project type and complexity | `src/pvms/scoring/`, `src/pvms/domain/` |
| Match required skills to employees and availability | `src/pvms/repositories/`, `src/pvms/scoring/` |
| Assess financial, technical, resource, and delivery risk | `src/pvms/scoring/` |
| Compare with past project experience | `src/pvms/repositories/` |
| Generate feasibility report and diagrams | `src/pvms/reports/`, `docs/` |
| Produce final recommendation | `src/pvms/scoring/`, `src/pvms/workflows/` |
| Keep setup local | `.env.example`, `docs/local-deployment.md` |

## Project Structure

```text
.
├── app/                         # Streamlit app files
├── data/
│   └── samples/                 # Sample files for testing
├── docs/                        # Notes about requirements, architecture, and setup
├── scripts/                     # Utility scripts
├── src/
│   └── pvms/
│       ├── ai/                  # AI model related code
│       ├── config/              # Environment and settings
│       ├── domain/              # Common models used across the project
│       ├── parsers/             # PDF, DOCX, and text parsing
│       ├── repositories/        # Database related code
│       ├── reports/             # Report and diagram generation
│       ├── scoring/             # Capability, resource, finance, risk scoring
│       └── workflows/           # Main RFQ assessment workflow
└── tests/                       # Test files
```

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -e ".[dev]"`.
3. Copy `.env.example` to `.env` and adjust local values.
4. Start MongoDB locally.
5. Start Ollama locally and make sure the configured model is available.
6. Run the UI with `streamlit run app/main.py`.

## Development Commands

```bash
pip install -e ".[dev]"
ruff check .
pytest
streamlit run app/main.py
```

## Docker Deployment

Use Docker when moving the project to a server.

1. Build and start the services.

```bash
docker compose up --build -d
```

2. Pull the Ollama model inside Docker.

```bash
docker compose --profile setup run --rm ollama-pull
```

3. Open the app.

```text
http://localhost:8501
```

On a remote server, replace `localhost` with the server IP or domain.

The Docker setup runs:

- `app`: Streamlit PVMS web app
- `ollama`: local LLM runtime
- `mongo`: MongoDB database service

Runtime settings are stored in `.env.docker`.

Useful commands:

```bash
docker compose logs -f app
docker compose restart app
docker compose down
```

## Current Status

This repository currently contains the base project setup. The actual RFQ processing, AI workflow, scoring formulas, and report generation will be implemented next.

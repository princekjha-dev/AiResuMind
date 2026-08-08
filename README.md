<div align="center">

# AiResuMind Pro v5.0

**AI Career Intelligence Platform — Build better applications. Make smarter career decisions.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Version-5.0--Pro-0071E3?style=flat-square)]()
[![OpenRouter](https://img.shields.io/badge/AI-OpenRouter%20%7C%20Gemini%20%7C%20Groq-4F8CFF?style=flat-square)]()

*Know how your resume performs. Find the gaps before recruiters do.*

</div>

---

## Overview

**AiResuMind Pro v5.0** is an executive-grade AI career intelligence operating system. Built with an Apple and Linear-inspired dark glassmorphic interface, it connects resume parsing, ATS benchmarking, job discovery, role optimization, and recruiter outreach into a unified workflow.

---

## Table of Contents

- [Core Principles](#core-principles)
- [Platform Modules](#platform-modules)
- [Design System](#design-system)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [License](#license)

---

## Core Principles

1. **Zero Fabrication**: No fake statistics or filler data. All metrics represent verified candidate telemetry.
2. **Editorial Aesthetics**: Stark dark canvas (`#0B0C0F`), high-contrast SF Pro / Inter typography, and generous negative space. Zero emojis.
3. **Structured AI Responses**: Observational insight model (`OBSERVATION` → `WHY IT MATTERS` → `RECOMMENDATION` → `ACTION`).

---

## Platform Modules

- **AI Career Command Center** — Centralized dashboard for application readiness, score telemetry, and prioritized career recommendations.
- **Resume Intelligence & Analyzer** — Benchmarks documents against 50+ ATS screening criteria, producing keyword gap matrices and before/after bullet rewrites.
- **Resume Builder Workspace** — Step-by-step optimization flow (`01 Resume` → `02 Target Role` → `03 Optimize` → `04 Generate`).
- **Outreach Intelligence (Cold Mail)** — Tailored recruiter cold emails and LinkedIn outreach messages with personalization scoring.
- **Job Discovery Engine** — High-precision job search with AI match scoring and strengths vs. gaps breakdown.

---

## Design System

| Token | Value | Description |
|---|---|---|
| `--bg` | `#0B0C0F` | Main dark background canvas |
| `--surface` | `#141519` | Structural panel container |
| `--surface-elevated` | `#191A1F` | Callout and highlight cards |
| `--text-primary` | `#F5F5F7` | Primary high-contrast text |
| `--text-secondary` | `#86868B` | Secondary editorial copy |
| `--border` | `rgba(255, 255, 255, 0.08)` | Low-contrast glass border |

---

## Architecture

```mermaid
flowchart TD
    User([Candidate / User]) -->|Browser Navigation| StreamlitApp["AiResuMind Pro v5.0 App\napp.py"]

    StreamlitApp -->|Upload Resume / JD| Extractor["Document Extractor\nutils/resume_parser.py"]
    Extractor -->|Parsed Content| ATSEngine["ATS Analysis Engine\nutils/ai_resume_analyzer.py"]
    Extractor -->|Structured Skills| LLMManager["Multi-Provider LLM Router\nOpenRouter · Gemini · Groq"]

    LLMManager -->|Outreach Drafts| ColdMail["pages/cold_mail.py"]
    LLMManager -->|Resume Rewrites| ResumeBuilder["pages/resume_builder.py"]
    LLMManager -->|ATS Insights| ResumeAnalyzer["pages/resume_analyzer.py"]

    ATSEngine -->|Candidate Telemetry| CommandCenter["dashboard/dashboard.py"]
    StreamlitApp -->|Read / Write| SQLiteDB[("SQLite Database\nresume_data.db")]
```

---

## Setup & Execution

```bash
# Clone & enter directory
git clone https://github.com/princekjha-dev/AiResuMind.git
cd AiResuMind

# Activate virtual environment
source .venv/bin/activate

# Run AiResuMind Pro v5.0
streamlit run app.py
```

Available at **http://localhost:8501**.

---

## License

This project is licensed under the [MIT License](LICENSE).

# Customer Support LLMOps

A production-ready LLMOps implementation for customer support with proper monitoring, prompt management, and evaluation capabilities.

## Overview

This project demonstrates key LLMOps (Large Language Model Operations) concepts by implementing a customer support assistant with robust infrastructure for monitoring, evaluation, and feedback collection. It serves as a practical example of how to operationalize LLMs in a production environment.

![LLMOps Architecture](https://mermaid.ink/img/pako:eNp1kb1uwjAQx1_l5KVDWDKwpgIJFqYsLJ2MLQfnHIkbx0a2Q1VVfXc-QtrSwYs_9-_7uTsV1muUrD9LGDUNmIFwA3XtRhpBa3cCN4Ja46IgWK2ugtL9lVQ-vJH2a2hqRRmCamHrjR-0cdRYf6y57AxJZ8oS-xWsGdgFJk9iUoZrjqj7h2Xeg1QvecXAJSgYiOh8CyXYhkf8R_yt4nYHQ6nRutFaDR7-dn--8cTlMoNhYsBs1fH9kQNMKWZP0Tw1N0FEJVb-JXr_ZjT36ENcn0rPaRGbLTwH5uQbOzJ7iMtnrvnK6SsXj_F5kHCF9Z20DL7PJb0XZTIryr7vP2T9xKv7dXpXP_h3p_Yz2jTa5Vc-CRt5VJLxT46YVtSB_gHI_ZjQ?type=png)

## Features

- **Prompt Management and Versioning**: Track and version prompt templates
- **Response Monitoring**: Measure latency, token usage, and other metrics
- **Feedback Collection**: Gather user feedback on LLM responses
- **Evaluation System**: Flag problematic interactions for review
- **API Endpoints**: Clean interface for interacting with the system
- **Docker Support**: Containerized deployment for consistent environments

## Project Structure

```
customer-support-llmops/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   └── __init__.py
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── templates.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── feedback.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py
│   │   └── prompt_service.py
│   └── utils/
│       ├── __init__.py
│       └── monitoring.py
├── data/
│   └── kb/
│       └── support_articles.json
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   └── test_prompts.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (optional, for containerized deployment)
- OpenAI API key

## Installation

### Option 1: Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/customer-support-llmops.git
   cd customer-support-llmops
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file to add your OpenAI API key
   ```

### Option 2: Docker Setup

1. Clone
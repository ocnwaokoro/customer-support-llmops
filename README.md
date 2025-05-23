# Customer Support LLMOps

A production-ready LLMOps implementation for customer support with proper monitoring, prompt management, and evaluation capabilities.

## Overview

This project demonstrates key LLMOps (Large Language Model Operations) concepts by implementing a customer support assistant with robust infrastructure for monitoring, evaluation, and feedback collection. It serves as a practical example of how to operationalize LLMs in a production environment.

```mermaid
flowchart TD
    A[User Request] --> B[API Gateway]
    B --> C[Prompt Management]
    C --> D[LLM Service]
    D --> E[Response Generation]
    E --> F[User Response]
    
    B --> G[Monitoring]
    E --> G
    
    F --> H[Feedback Collection]
    H --> I[Evaluation System]
    I --> C
    
    J[Knowledge Base] --> C
```

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

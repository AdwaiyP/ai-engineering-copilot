# CodePilot — AI Engineering Copilot

An AI-native developer assistant that analyzes GitHub repositories using **Retrieval-Augmented Generation (RAG), semantic search, and agentic workflows**.

CodePilot can clone and index a GitHub repository, retrieve relevant source code using vector similarity search, autonomously inspect files, and answer natural-language questions about the codebase.

![CodePilot Demo](docs/screenshots/codepilot-agent.png)

---

## Features

- Clone and index public GitHub repositories
- Ask natural-language questions about a codebase
- Semantic code search using vector embeddings
- Retrieval-Augmented Generation (RAG)
- Agentic repository investigation
- Autonomous repository inspection
- Source-file reading and code exploration
- Visible agent activity / tool execution
- Groq-powered LLM responses
- REST API built with FastAPI
- React-based developer interface
- Dockerized frontend and backend

---

## How It Works

```text
GitHub Repository
        │
        ▼
Repository Cloning
        │
        ▼
Source Code Parsing
        │
        ▼
Code Chunking
        │
        ▼
Sentence Transformer Embeddings
        │
        ▼
FAISS Vector Index
        │
        ├───────────────┐
        ▼               │
Semantic Retrieval      │
        │               │
        ▼               │
   AI Agent             │
        │               │
        ├─ list_files   │
        ├─ read_file    │
        └─ search_code ─┘
        │
        ▼
Groq LLM
        │
        ▼
Repository-Aware Answer
```

---

## Agentic Workflow

CodePilot goes beyond a standard RAG chatbot.

The agent can investigate a repository by selecting and executing tools such as:

- `list_files` — inspect repository structure
- `read_file` — read relevant source files
- `search_code` — perform semantic retrieval over indexed code

The results of these actions are returned to the agent, allowing it to gather additional context before generating an answer.

The frontend exposes these actions through the **Agent Activity** panel.

---

## RAG Pipeline

When a repository is indexed:

1. CodePilot clones the GitHub repository.
2. Source files are discovered and parsed.
3. Code is divided into searchable chunks.
4. Sentence Transformer embeddings are generated.
5. Embeddings are stored in a FAISS vector index.
6. A user submits a natural-language question.
7. Relevant code chunks are retrieved using semantic similarity.
8. The agent can perform additional repository investigation.
9. Retrieved context is provided to the LLM.
10. A repository-aware response is generated.

---

## Tech Stack

### Frontend

- React
- JavaScript
- Vite
- Lucide React
- HTML / CSS

### Backend

- Python
- FastAPI
- REST APIs
- Pydantic

### AI / GenAI

- Retrieval-Augmented Generation (RAG)
- Agentic workflows
- Groq LLM API
- Sentence Transformers
- Prompt engineering
- Tool calling

### Vector Search

- FAISS
- Semantic embeddings

### Repository Processing

- GitPython
- GitHub repository ingestion

### DevOps

- Docker
- Docker Compose
- Nginx

---

## Project Structure

```text
ai-engineering-copilot/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── api/
│   │   ├── llm/
│   │   ├── services/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   ├── Dockerfile
│   └── package.json
│
├── docs/
│   └── screenshots/
│       └── codepilot-agent.png
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Running Locally with Docker

### 1. Clone the project

```bash
git clone <YOUR-CODEPILOT-GITHUB-URL>
cd ai-engineering-copilot
```

### 2. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Configure:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model
```

Never commit your real `.env` file.

### 3. Build

```bash
docker compose build
```

### 4. Start

```bash
docker compose up -d
```

### 5. Open CodePilot

Frontend:

```text
http://localhost:5173
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

### 6. Stop

```bash
docker compose down
```

---

## Example

Index a public GitHub repository:

```text
https://github.com/AdwaiyP/semantic-search-engine
```

Then ask:

```text
Explain how semantic search is implemented in this repository.
```

CodePilot can retrieve relevant code and use repository tools to investigate the implementation before producing its response.

---

## Why I Built This

Modern AI applications require more than simply sending prompts to an LLM.

I built CodePilot to explore how **RAG, embeddings, vector search, agentic tool use, REST APIs, and modern frontend development** can be combined into an end-to-end AI-native application.

The project demonstrates the complete workflow from repository ingestion and semantic retrieval to autonomous code investigation and an interactive developer interface.

---

## Future Improvements

- Support multiple concurrent repository sessions
- Private GitHub repository integration
- Persistent vector indexes
- Streaming LLM responses
- Conversation history
- Source citations in generated answers
- Authentication and user workspaces
- Cloud deployment
- Automated testing and CI/CD

---

## Author

**Adwaiy P**

AI & Data Science Engineering  
GitHub: `AdwaiyP`
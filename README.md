# Compass — Navigate Any GitHub Repository with AI

> An AI-powered repository understanding tool that helps developers explore unfamiliar GitHub projects, understand architecture, and plan new features using Retrieval-Augmented Generation (RAG).

Compass enables developers to analyze any public GitHub repository by simply pasting its URL. Instead of manually reading hundreds of source files, Compass indexes the repository, builds a semantic search database, and allows developers to ask natural language questions about the codebase. Every response is grounded in the repository and includes file and line citations for transparency.

---

# 🚀 1. Description

Understanding an unfamiliar codebase is one of the biggest challenges developers face.

Compass simplifies this process by transforming a GitHub repository into an AI-searchable knowledge base. Developers can ask questions about architecture, authentication, APIs, folder structure, or implementation details, and receive repository-specific answers backed by verifiable source citations.

Unlike generic AI coding assistants, Compass does not generate answers from general programming knowledge. Instead, it retrieves relevant source code from the repository and uses it as context for the language model, ensuring responses remain grounded in the actual codebase.

---

# 💡 2. Motivation & Problem

## The Problem

Developers frequently work with repositories they have never seen before.

Common questions include:

- Where should I start reading the project?
- How does authentication work?
- Where are the API routes defined?
- Which files are responsible for database operations?
- How can I integrate a new feature such as Stripe or Google Login?

Finding these answers usually requires reading dozens or even hundreds of files.

Traditional AI assistants often lack repository context, leading to generic or hallucinated answers that cannot be verified.

## The Solution

Compass bridges the gap between modern AI and software engineering.

It clones a public GitHub repository, indexes the source code using embeddings, stores semantic vectors in ChromaDB, and retrieves the most relevant code snippets whenever a developer asks a question.

Every answer is grounded in repository context and includes file names and line ranges, making responses transparent and trustworthy.

---

# 🛠️ 3. Tech Stack

## Frontend

- React (Vite)
- Tailwind CSS
- Axios
- Framer Motion
- React Markdown
- Highlight.js

## Backend

- FastAPI
- Uvicorn
- GitPython
- Pydantic

## AI & Retrieval

- Groq API (Llama 3.3 70B Versatile)
- HuggingFace Sentence Transformers
- all-MiniLM-L6-v2 Embedding Model
- ChromaDB Vector Database

---

# ⚙️ 4. How It Works

Compass follows a Retrieval-Augmented Generation (RAG) pipeline designed specifically for software repositories.

```text
                GitHub Repository URL
                         │
                         ▼
          Shallow Clone Repository (--depth 1)
                         │
                         ▼
          Filter Supported Source Code Files
                         │
                         ▼
           Parse & Structural Code Chunking
                         │
                         ▼
            Generate Semantic Embeddings
                         │
                         ▼
             Store Vectors in ChromaDB
                         │
                         ▼
            User Asks Repository Question
                         │
                         ▼
            Retrieve Relevant Code Chunks
                         │
                         ▼
            Build Repository-Aware Prompt
                         │
                         ▼
                 Groq Llama 3.3 70B
                         │
                         ▼
            Answer + File & Line Citations
```

## Repository Ingestion

After receiving a GitHub repository URL, Compass performs a shallow clone to avoid downloading unnecessary Git history.

Only supported source files are indexed while generated folders such as `node_modules`, `dist`, `.git`, and other irrelevant files are ignored.

## Structural Chunking

Instead of splitting code into arbitrary character chunks, Compass groups code into logical units such as:

- Functions
- Classes
- Methods
- Components

Each chunk stores metadata including:

- File path
- Programming language
- Symbol name (when available)
- Start line
- End line

This metadata enables accurate source citations.

## Embedding Generation

Each code chunk is converted into a semantic vector using the HuggingFace **all-MiniLM-L6-v2** embedding model.

The generated vectors and metadata are stored inside ChromaDB.

## Semantic Retrieval

Whenever a developer asks a question, Compass:

1. Converts the question into an embedding.
2. Performs semantic similarity search in ChromaDB.
3. Retrieves the most relevant code chunks.
4. Builds repository-aware context.

## AI Response Generation

The retrieved repository context is sent to **Groq's Llama 3.3 70B** model.

The model is instructed to:

- Answer only using retrieved repository context.
- Clearly separate repository facts from implementation suggestions.
- Provide file and line citations for every explanation.

Example:

```
Authentication uses JWT middleware.

Sources

controllers/auth.py
Lines 18–74

middleware/auth.py
Lines 10–42
```

---

# 📁 5. Backend Structure

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── ingest.py
│   │   └── qa.py
│   │   └── vectorstore.py
│   │   └── endpoints.py
│   │
│   ├── services/
│   │   ├── backgroud_service.py
│   │   ├── ingestion_service.py
│   │   ├── chunking_service.py
│   │   ├── qa_services.py
│   │   └── task_service.py
│   │
│   ├── core/
│   │   └── config.py
|   |
│   ├── prompts/
│   │   └── qa_prompts.py
|   |
│   ├── schemas/
│   │   └── repository.py
│   │
│   └── utils/
│   |   └── repo_utils.py
│   │
│   └── vectorstore/
│       └── chroma_service.py
│
├── chroma_db/
├── temp/
├── requirements.txt
├── Dockerfile
└── .env
```

### Core Services

- **github.py** – Repository cloning, validation, cleanup.
- **ingestion.py** – File parsing, structural chunking, embeddings, indexing.
- **rag.py** – Semantic retrieval and repository context generation.
- **llm.py** – Prompt construction and Groq API integration.

---

# ⚡ 6. Local Setup

## Clone the Repository

```bash
git clone https://github.com/your-username/compass.git
cd compass
```

---

## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the backend directory:

```env
GROQ_API_KEY=your_groq_api_key

CHROMA_DB_PATH=./chroma_db

TEMP_DIR=./temp

MAX_REPOSITORY_SIZE_MB=100

MAX_FILES=500
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## Frontend Setup

Open a new terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create a `.env` file:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

Start the development server:

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🌟 Features

- Analyze any public GitHub repository
- AI-powered repository understanding
- Retrieval-Augmented Generation (RAG)
- Semantic code search
- Repository-specific Q&A
- Architecture explanations
- Feature integration guidance
- File & line citations
- Repository summary generation
- Minimal, single-page interface

---

# 📄 License

This project is licensed under the MIT License.
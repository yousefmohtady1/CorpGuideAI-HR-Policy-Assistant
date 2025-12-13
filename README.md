# CorpGuideAI - HR Policy Assistant

**CorpGuideAI** is an advanced AI-powered assistant designed to help employees navigate and understand internal HR policies. Leveraging **Retrieval-Augmented Generation (RAG)**, it provides accurate, context-aware answers based on your organization's PDF documents.

## 🚀 Features

- **RAG Architecture**: Combines vector search with generative AI for precise answers.
- **LLM Integration**: Powered by **Groq** (using Llama models) for fast and efficient inference.
- **Vector Database**: Uses **ChromaDB** for efficient document storage and retrieval.
- **Smart Ingestion**:
  - Extracts text from PDFs.
  - Improves retrieval speed and accuracy with semantic chunking.
  - Uses `Alibaba-NLP/gte-multilingual-base` for robust multilingual support.
- **Interactive Web UI**: A modern, clean chat interface to interact with the assistant.
- **Chat History Management**: Maintains context across the conversation session (Reset supported).
- **FastAPI Backend**: A high-performance API to serve requests.
- **Docker Support**: Containerized for easy deployment.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Backend**: FastAPI, Uvicorn
- **AI/ML**: LangChain, HuggingFace, ChromaDB, Groq
- **Tools**: `pypdf`, `sentence-transformers`, Docker

## 📂 Project Structure

```bash
CorpGuideAI-HR-Policy-Assistant/
├── api/
│   ├── main.py              # FastAPI application & entry point
│   ├── schemas.py           # Pydantic models
├── config/
│   ├── settings.py          # Configuration settings
├── core/
│   ├── rag_pipeline.py      # Core RAG logic & Chat History
│   ├── prompts.py           # Prompt templates
├── data/                    # PDF documents storage
├── services/
│   ├── document_processor.py
│   ├── vector_store.py
│   ├── llm_client.py
├── web_ui/                  # Frontend Application
│   ├── index.html
│   ├── script.js
│   ├── style.css
├── ingest.py                # Document ingestion script
├── Dockerfile               # Docker container configuration
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

## ⚡ Prerequisites

- **Python 3.10+**
- **Groq API Key**: Get it from [Groq Console](https://console.groq.com/).

## 📦 Installation & Usage

### Option 1: Local Installation

1.  **Clone & Setup**:

    ```bash
    git clone <repository-url>
    cd CorpGuideAI-HR-Policy-Assistant
    python -m venv venv

    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate

    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file:

    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

3.  **Ingest Documents**:
    Place PDFs in `data/` and run:

    ```bash
    python ingest.py
    ```

4.  **Run Server**:
    ```bash
    uvicorn api.main:app --reload
    ```
    Access the Web UI at: `http://localhost:8000`

### Option 2: Docker

1.  **Build Image**:

    ```bash
    docker build -t corpguide-ai .
    ```

2.  **Run Container**:
    ```bash
    docker run -p 7860:7860 --env-file .env corpguide-ai
    ```
    Access at: `http://localhost:7860`

## 🔗 API Endpoints

- `GET /`: Serves the Web UI.
- `POST /chat`: Chat endpoint.
  - Body: `{ "question": "..." }` (History managed internally)
- `POST /reset`: Clears current chat history.

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

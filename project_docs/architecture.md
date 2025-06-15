# 📐 CUAssist – AI Member Support Agent

**Project Architecture Overview**

---

## 🗂️ File & Folder Structure

```bash
├── app/
│   ├── main.py
│   ├── prompt_manager.py
│   ├── pushover_alerts.py
│   ├── state.py
│   └── utils.py
├── agent/
│   ├── AI_Agent_Identity_Profile_Alexa.md
│   ├── faq_chunks.json
│   ├── embedder.py
│   ├── retriever.py
│   └── pdf_processor.py
├── data/
│   ├── knowledge_base/
│   ├── embeddings/
│   └── logs/
├── config/
│   ├── secrets.env
│   └── constants.py
├── tests/
│   ├── test_prompt.py
│   ├── test_rag.py
│   ├── test_pushover.py
│   └── test_pdf_processor.py
├── .env
├── requirements.txt
├── README.md
└── run.sh
```

---

## ⚙️ Module Responsibilities

### `app/main.py`

- Launches the Gradio UI
- Handles user input/output loop
- Passes user message to LLM with context

### `app/prompt_manager.py`

- Loads Alexa's system prompt
- Injects retrieved FAQ content for RAG queries

### `app/pushover_alerts.py`

- Sends Pushover alerts for unknown questions and escalation

### `app/state.py`

- In-memory session state: history, flags, context

---

## 🤖 Agent Layer

### `agent/AI_Agent_Identity_Profile_Alexa.md`

- Alexa's tone and responsibilities
- Forms the base system prompt

### `agent/embedder.py`

- Loads vector DB
- Creates embeddings for FAQ chunks
- Stores embeddings in ChromaDB

### `agent/retriever.py`

- Performs similarity search using ChromaDB
- Returns top-N relevant chunks for queries
- Handles query embedding and result formatting

### `agent/pdf_processor.py`

- Processes PDF documents into text chunks for RAG
- Handles PDF parsing, text extraction, and chunking

### `agent/faq_chunks.json`

- Preprocessed support data used for RAG

---

## 📚 Data Layer

### `data/raw_faqs/`

- Original PDF/markdown source docs

### `data/embeddings/`

- Vector index (FAISS or ChromaDB)

### `data/logs/`

- Stores logs for unknown questions & contact requests

---

## 🔧 Config & Settings

### `config/secrets.env`

- Pushover keys, API tokens

### `config/constants.py`

- Embedding model, chunk sizes, etc.

---

## 🧠 Where State Lives

| Component            | State Handled                   | Persistence |
| -------------------- | ------------------------------- | ----------- |
| `state.py`           | Chat history, session ID, flags | In-memory   |
| `logs/*.json`        | Unknown Qs, user details        | File-based  |
| `embeddings/*.index` | Document embeddings (RAG)       | Vector DB   |

---

## 🔌 Service Flow & Integration

```mermaid
flowchart TD
    A[User Message] --> B[main.py (UI)]
    B --> C[prompt_manager.py]
    C --> D[retriever.py: Fetch relevant FAQs]
    C --> E[Build system prompt with identity + FAQ]
    E --> F[Send to LLM API]
    F --> G[LLM Response]
    G --> B
    G -->|Unknown?| H[pushover_alerts.py: record_unknown_question()]
    G -->|Escalation?| I[pushover_alerts.py: record_user_details()]

    J[PDF Documents] --> K[pdf_processor.py]
    K --> L[Text Chunks]
    L --> M[embedder.py: Create Embeddings]
    M --> N[Vector Database]
    D --> N
```

---

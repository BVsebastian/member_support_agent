# 📐 Member Support Agent – AI Architecture (Tool-Driven)

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
├── tools.py
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
- Integrates tool schema + handles tool call responses

### `app/prompt_manager.py`

- Loads Alexa's system prompt
- Injects retrieved FAQ content for RAG queries

### `app/pushover_alerts.py`

- Sends Pushover alerts for unknown questions and escalation

### `app/state.py`

- In-memory session state: history, flags, context

### `tools.py`

- Contains callable functions: `send_notification`, `record_user_details`, `log_unknown_question`
- Each tool has a defined JSON schema for LLM registration
- Includes `handle_tool_call()` to route tool calls

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

- Vector index (ChromaDB)

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

## 🔌 Tool-Driven Service Flow

```mermaid
flowchart TD
    A[User Message] --> B[main.py (UI)]
    B --> C[prompt_manager.py]
    C --> D[retriever.py: Fetch relevant FAQs]
    C --> E[Build system prompt with identity + FAQ]
    E --> F[Send to LLM API + Tool Schemas]
    F --> G[LLM Response]

    G -->|Tool Call?| H[handle_tool_call()]
    H --> I[Execute corresponding function (send_notification, record_user_details, etc.)]
    I --> J[Update state/logs or trigger alert]

    G -->|Final Reply| B

    subgraph Tools
        K1[send_notification]
        K2[record_user_details]
        K3[log_unknown_question]
    end
```

---

## 🔧 Tool-Driven Architecture Benefits

- Decouples business logic from UI
- LLM determines when tools should be used
- Functions can be reused or extended without touching main logic
- Easier debugging and scaling

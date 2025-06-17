# 📐 Member Support Agent – AI Architecture (Tool-Driven)

**Project Architecture Overview**

---

## 🗂️ File & Folder Structure

```bash
├── app/
│   ├── main.py              # Gradio UI + chat loop
│   ├── prompt_manager.py    # System prompt + tool guidelines
│   ├── pushover_alerts.py   # Notification handling
│   ├── state.py            # Session state management
│   └── utils.py            # Helper functions
├── agent/
│   ├── AI_Agent_Identity_Profile_Alexa.md
│   ├── embedder.py         # Embedding creation
│   ├── retriever.py        # Similarity search
│   └── pdf_processor.py    # PDF chunking
├── data/
│   ├── knowledge_base/     # PDF source files
│   ├── embeddings/         # Persistent ChromaDB storage
│   └── logs/              # Application logs
├── config/
│   ├── secrets.env        # Environment variables
│   └── constants.py       # Configuration constants
├── tests/
│   ├── test_prompt.py
│   ├── test_rag.py
│   ├── test_pushover.py
│   └── test_pdf_processor.py
├── tools.py               # Tool definitions + handler
├── .env                   # Local environment
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

---

## ⚙️ Module Responsibilities

### `app/main.py`

- Launches the Gradio UI
- Handles user input/output loop
- Passes user message to LLM with context
- Integrates tool schema + handles tool call responses
- Initializes RAG pipeline on startup
- Manages session state and chat history

### `app/prompt_manager.py`

- Loads Alexa's system prompt
- Injects retrieved FAQ content for RAG queries
- Includes tool usage guidelines
- Maintains consistent agent tone

### `app/pushover_alerts.py`

- Sends Pushover alerts for unknown questions and escalation
- Handles multiple issue types
- Prevents duplicate notifications
- Formats messages for support team

### `app/state.py`

- In-memory session state: history, flags, context
- Session ID generation and management
- Chat history tracking
- Tool call state management

### `tools.py`

- Contains callable functions: `send_notification`, `record_user_details`, `log_unknown_question`
- Each tool has a defined JSON schema for LLM registration
- Includes `handle_tool_call()` to route tool calls
- Error handling and logging
- Duplicate notification prevention

---

## 🤖 Agent Layer

### `agent/AI_Agent_Identity_Profile_Alexa.md`

- Alexa's tone and responsibilities
- Forms the base system prompt
- Tool usage guidelines
- Response formatting rules

### `agent/embedder.py`

- Creates embeddings for FAQ chunks
- Uses OpenAI's embedding model
- Persistent storage in ChromaDB
- Error handling and logging

### `agent/retriever.py`

- Performs similarity search using ChromaDB
- Returns top-N relevant chunks for queries
- Handles query embedding and result formatting
- Uses persistent vector storage

### `agent/pdf_processor.py`

- Processes PDF documents into text chunks for RAG
- Handles PDF parsing, text extraction, and chunking
- Optimized chunk size and overlap
- Error handling for malformed PDFs

---

## 📚 Data Layer

### `data/knowledge_base/`

- Original PDF source docs
- Processed on first run
- Chunked for RAG

### `data/embeddings/`

- Persistent storage for document embeddings
- Uses ChromaDB for efficient similarity search
- Error handling and logging

### `data/logs/`

- Stores logs for unknown questions & contact requests
- Timestamped entries
- JSON format for easy parsing

---

## 🔧 Config & Settings

### `config/secrets.env`

- Pushover keys
- OpenAI API token
- Environment-specific settings

### `config/constants.py`

- Embedding model settings
- Chunk sizes
- Tool configuration
- Session parameters

---

## 🧠 Where State Lives

| Component          | State Handled                   | Persistence |
| ------------------ | ------------------------------- | ----------- |
| `state.py`         | Chat history, session ID, flags | In-memory   |
| `logs/*.json`      | Unknown Qs, user details        | File-based  |
| `data/embeddings/` | Document embeddings (RAG)       | Persistent  |

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
    H --> I[Execute corresponding function]
    I --> J[Update state/logs or trigger alert]

    G -->|Final Reply| B

    subgraph Tools
        K1[send_notification]
        K2[record_user_details]
        K3[log_unknown_question]
    end

    subgraph RAG Pipeline
        L1[pdf_processor.py]
        L2[embedder.py]
        L3[retriever.py]
    end

    subgraph Session Management
        M1[state.py]
        M2[Session ID]
        M3[Chat History]
    end
```

---

## 🚀 Deployment Architecture

### HuggingFace Spaces

- Gradio app deployment
- Environment variable management
- Persistent RAG pipeline storage
- Session management
- Easy restart capability

### Security

- API keys via environment variables
- No persistent storage of sensitive data
- Secure tool execution
- Input validation

### Performance

- Efficient persistent embeddings
- Optimized chunk retrieval
- Session-based state management
- Tool call caching

---

## 🔧 Tool-Driven Architecture Benefits

- Decouples business logic from UI
- LLM determines when tools should be used
- Functions can be reused or extended without touching main logic
- Easier debugging and scaling
- Robust error handling
- Efficient session management

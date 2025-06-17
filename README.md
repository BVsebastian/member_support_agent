# Member Support Agent

An AI-powered member support agent for Horizon Bay Credit Union that handles member inquiries, escalations, and provides support using a tool-driven architecture.

## Features

- 🤖 AI-powered member support using OpenAI's GPT models
- 🔍 RAG (Retrieval-Augmented Generation) for accurate FAQ responses
- ⚙️ Tool-driven architecture for handling escalations and notifications
- 💬 Natural conversation flow with context awareness
- 🔔 Pushover notifications for escalations and unknown questions
- 🔄 Automated RAG pipeline initialization
- 🚀 HuggingFace Spaces deployment ready

## Environment Variables

The following environment variables need to be set in HuggingFace Spaces:

- `OPENAI_API_KEY`: Your OpenAI API key
- `PUSHOVER_TOKEN`: Your Pushover API token
- `PUSHOVER_USER`: Your Pushover user key
- `HF_TOKEN`: Your HuggingFace access token (for deployment)

## Local Development

1. Clone the repository
2. Create and activate virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

4. Set up environment variables in `.env` file
5. Run the application:

```bash
python -m app.main
```

The application will automatically:

- Process PDFs in `data/knowledge_base/` if needed
- Create embeddings if they don't exist
- Initialize the RAG pipeline on first run

## HuggingFace Spaces Deployment

1. Visit https://huggingface.co and set up an account

2. From the Avatar menu on the top right, choose Access Tokens. Choose "Create New Token". Give it WRITE permissions.

3. Add the token to your .env file:

```
HF_TOKEN=hf_xxx
```

4. From your project root directory, run:

```bash
uv run gradio deploy
```

5. When prompted:
   - Name your space (e.g., "member_support_agent")
   - Specify `app/main.py` as the entry point
   - Choose cpu-basic as the hardware
   - Say Yes to needing to supply secrets
   - Provide your secrets:
     - OPENAI_API_KEY
     - PUSHOVER_TOKEN
     - PUSHOVER_USER
   - Say "no" to github actions

The application will automatically initialize the RAG pipeline on first deployment.

## Project Structure

```
├── app/                 # Main application code
│   ├── main.py         # Gradio UI and chat loop
│   ├── prompt_manager.py # System prompt management
│   ├── pushover_alerts.py # Notification handling
│   ├── rag_setup.py    # RAG pipeline initialization
│   └── state.py        # Session state management
├── agent/              # AI agent components
│   ├── embedder.py     # FAQ embedding generation
│   ├── retriever.py    # FAQ retrieval
│   └── pdf_processor.py # PDF processing
├── data/               # Data storage
│   ├── knowledge_base/ # FAQ documents
│   └── embeddings/     # Vector database
└── tests/              # Test suite
```

## RAG Pipeline

The RAG pipeline is automatically initialized when needed:

1. **PDF Processing**:

   - PDFs in `data/knowledge_base/` are processed into chunks
   - Chunks are saved to `data/faq_chunks.json`

2. **Embedding Creation**:

   - Chunks are embedded using OpenAI's text-embedding-ada-002
   - Embeddings are stored in ChromaDB at `data/embeddings/`

3. **Retrieval**:
   - The Retriever uses ChromaDB to find relevant chunks
   - Results are used to augment LLM responses

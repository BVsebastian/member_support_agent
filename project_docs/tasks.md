# 🧱 CUAssist MVP Build Plan – Step-by-Step

Each task is atomic, testable, and has a clear start and end.  
**Project Root:** `member_support_agent/`

---

## 🗂️ SETUP PHASE

### Task 1: Initialize Project Structure

- **Start:** Create `member_support_agent/` root directory with subfolders:
  - `app/`, `agent/`, `data/`, `config/`, `tests/`
- **End:** Folders are in place and committed to version control.

### Task 2: Create `requirements.txt` + Setup UV Environment with ChromaDB

- **Start:** Add dependencies to `requirements.txt`:
  ```txt
  openai
  gradio
  chromadb
  python-dotenv
  requests
  ```
- **End:** Run:
  ```bash
  uv venv
  uv pip install -r requirements.txt
  ```

### Task 3: Add `.env` + `config/secrets.env`

- **Start:** Create `.env` and `config/secrets.env` with:
  ```env
  OPENAI_API_KEY=
  PUSHOVER_TOKEN=
  PUSHOVER_USER=
  ```
- **End:** Variables are loaded using `dotenv`.

---

## 🧠 SYSTEM PROMPT + IDENTITY

### Task 4: (Removed – Already Complete)

- Identity Profile PDF: `AI_Agent_Identity_Profile_Alexa.pdf`

### Task 5: Implement `prompt_manager.py`

- **Start:** Build `get_system_prompt()` to return formatted prompt.
- **End:** Outputs identity prompt string.

### Task 6: Unit Test for Prompt

- **Start:** `tests/test_prompt.py` verifies key phrases in prompt.
- **End:** Tests pass.

---

## 🔍 RAG PIPELINE

### Task 7: Chunk PDF FAQ Documents

- Source PDFs from `data/knowledge_base/`:
  - `Horizon Bay CU Account Support Manual.pdf`
  - `Horizon Bay CU Member Services Toolkit.pdf`
  - `Why Join Horizon Bay Credit Union.pdf`
- **End:** Save to `data/faq_chunks.json`

### Task 8: Embed Chunks

- **Start:** Vectorize chunks using OpenAI embeddings.
- **End:** Each chunk includes vector metadata.

### Task 9: Build ChromaDB Vector Index

- **Start:** Insert vectors into Chroma index.
- **End:** Persisted to `data/embeddings/`

### Task 10: Implement Retriever

- **Start:** `retrieve_top_chunks(query)` returns top-N matches.
- **End:** Matches include chunk text + metadata.

### Task 11: Unit Test for RAG

- **Start:** Assert test query returns known match.
- **End:** Test passes.

---

## 💬 MAIN CHAT LOOP

### Task 12: Build Minimal Gradio UI

- **Start:** Build textbox + output window.
- **End:** Submits message and returns dummy reply.

### Task 13: Add Prompt Flow

- **Start:** Combine system prompt, RAG, and OpenAI call.
- **End:** Chat works with prompt + FAQ support.

### Task 14: Add Session State

- **Start:** Track conversation and flags in `state.py`.
- **End:** Session memory is functional.

---

## 🚨 ALERTS + LOGGING

### Task 15: Create `pushover_alerts.py`

- **Start:** Implement:
  - `record_unknown_question(question)`
  - `record_user_details(email, name?, notes?)`
- **End:** Triggers Pushover alert.

### Task 16: Integrate Alerts in Chat

- **Start:** Detect escalation or unknowns in chat.
- **End:** Alerts and logs are triggered.

### Task 17: Log to `data/logs/`

- **Start:** Save alert events as JSON with timestamp.
- **End:** Files stored under `data/logs/`

---

## ✅ FINAL QA + DEPLOY

### Task 18: Add `run.sh`

- **Start:** Launch script for dev environment.
- **End:** Runs Gradio UI with `./run.sh`

### Task 19: Manual QA

- **Start:** Test:
  - FAQ response
  - Unknown question alert
  - Contact escalation
- **End:** All cases pass

### Task 20: Create `README.md`

- **Start:** Document setup, `.env`, UV setup, run instructions.
- **End:** Fully onboardable for devs.

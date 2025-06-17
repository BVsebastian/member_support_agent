# 🧱 Member Support Agent – Build Plan (Tool-Driven)

Each task is atomic, testable, and has a clear start and end.  
**Project Root:** `member_support_agent/`

---

## 🗂️ SETUP PHASE

### Task 1: Initialize Project Structure

- Create `member_support_agent/` root directory with subfolders:
  - `app/`, `agent/`, `data/`, `config/`, `tests/`

### Task 2: Create `requirements.txt` + Setup UV Environment

- Add dependencies:
  ```txt
  openai
  gradio
  chromadb
  python-dotenv
  requests
  ```
- Run:
  ```bash
  uv venv
  uv pip install -r requirements.txt
  ```

### Task 3: Add `.env` + `config/secrets.env`

- Populate:
  ```env
  OPENAI_API_KEY=
  PUSHOVER_TOKEN=
  PUSHOVER_USER=
  ```

---

## 🧠 SYSTEM PROMPT + IDENTITY

### Task 4: (Removed - Already Complete)

### Task 5: Implement `prompt_manager.py`

- Function: `get_system_prompt()` returns formatted identity prompt

### Task 6: Unit Test for Prompt

- Test `test_prompt.py` for expected system prompt phrases

---

## 🔍 RAG PIPELINE

### Task 7: Chunk PDF FAQ Documents

- Chunk: `data/knowledge_base/*.pdf`
- Output: `faq_chunks.json`

### Task 8: Embed Chunks

- Vectorize using OpenAI embeddings
- Store with metadata

### Task 9: Build ChromaDB Index

- Persist index to `data/embeddings/`

### Task 10: Implement Retriever

- Function: `retrieve_top_chunks(query)`
- Output: chunk text + metadata

### Task 11: Unit Test RAG

- Validate known query returns expected result

---

## 💬 MAIN CHAT LOOP

### Task 12: Build Minimal Gradio UI

- Textbox + output window
- Submit message, return dummy reply

### Task 13: Add Prompt Flow

- Combine system prompt, RAG, and OpenAI call

### Task 14: Add Session State

- Store chat history and flags using `state.py`

---

## ⚠️ ALERTS + LOGGING

### Task 15: Create `pushover_alerts.py`

- `record_unknown_question(question)`
- `record_user_details(email, name?, notes?)`

### Task 16: Integrate Alerts in Chat

- Detect escalation or unknown question triggers

### Task 17: Log to `data/logs/`

- Save event JSONs with timestamps

---

## 🔧 TOOL-DRIVEN LOGIC

### Task 18: Define Tool Functions

- File: `tools.py`
- Functions:
  - `send_notification(params)`
  - `record_user_details(params)`
  - `log_unknown_question(params)`

### Task 19: Define Tool Schemas

- Define JSON schemas describing inputs + purpose
- Register during LLM invocation

### Task 20: Implement Tool Handler

- `handle_tool_call(tool_call_obj)`
- Route to correct function and return result

### Task 21: Update Chat Loop

- Modify `main.py` to:
  - Pass tool schema to LLM
  - Detect tool calls in response
  - Call `handle_tool_call()`

---

## ✅ FINAL QA + DEPLOY

### Task 22: Add `run.sh`

- Launches Gradio app

### Task 23: Manual QA

- Test full flow:
  - FAQ success
  - Unknown detection
  - Escalation + tool execution

### Task 24: Write `README.md`

- Setup, dependencies, usage
- Document tool-driven approach

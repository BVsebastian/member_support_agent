# 📝 Product Requirements Document (PRD)

**Project Name**: Member Support Agent  
**Organization**: Horizon Bay Credit Union  
**Owner**: Benedict Sebastian  
**Date**: June 17, 2024

---

## 1. Objective

Build a web-based AI assistant named **Alexa** to act as a virtual Member Support Representative for Horizon Bay Credit Union. Alexa answers frequently asked questions using internal documents, maintains a consistent professional tone, and dynamically performs tool-based actions (e.g., notifications, escalation) based on user interactions.

---

## 2. Scope

### ✅ In Scope

- LLM-powered chatbot trained to simulate Horizon Bay CU agent
- Agent tone from "Alexa's Identity Profile"
- Tool-based decision system for key actions:
  - `record_user_details`
  - `log_unknown_question`
  - `send_notification`
- Push notifications via Pushover for unresolved queries and escalations
- Retrieval-Augmented Generation (RAG) using internal knowledge base
- Automated RAG pipeline initialization
- Web UI (Gradio) with HuggingFace Spaces deployment
- Session management and chat history
- Efficient RAG pipeline with in-memory embeddings

### ❌ Out of Scope

- Secure transactions, account-level authentication
- Live human chat
- Real-time banking integrations
- Persistent chat history across deployments

---

## 3. Features

### 🔹 Feature 1: Agent Identity Prompt

- Alexa is a virtual rep
- Tone and values from Identity Profile
- System prompt injected in every session
- Tool usage guidelines integrated into prompt

### 🔹 Feature 2: Tool - Log Unknown Question

- Tool: `log_unknown_question(question)`
- Logs query + context + timestamp
- Pushes alert to support team
- Prevents duplicate notifications

### 🔹 Feature 3: Tool - Log Contact Escalation

- Tool: `record_user_details(email, name?, notes?)`
- Invoked when user requests follow-up/escalation
- Pushover alert with captured details
- Handles multiple issue types (fraud, loan, card, etc.)

### 🔹 Feature 4: RAG-Based FAQ Support

- Uses curated docs:
  - Account Support Manual
  - Member Toolkit
  - Why Join Horizon Bay CU
- Chunked, embedded via OpenAI, queried via ChromaDB
- Automated pipeline initialization:
  - PDF processing on first run
  - Embedding creation if needed
  - Persistent storage in ChromaDB
  - Efficient retrieval with similarity search

### 🔹 Feature 5: Tool-Driven Framework

- System registers tool schemas with LLM
- LLM returns `tool_call` in response
- System executes tools dynamically via handler
- Easily extensible: add tools without touching core logic
- Robust error handling and logging

### 🔹 Feature 6: Automated Deployment

- HuggingFace Spaces deployment
- Environment variable management
- Automated RAG pipeline setup
- Persistent storage handling
- Session management
- Easy restart capability

---

## 4. Required Documents

- Alexa's Identity Profile
- Account Support Manual
- Member Services Toolkit
- Membership Benefits Guide

---

## 5. Success Criteria

- ≥80% accuracy on FAQs
- Unknown questions logged and alerted
- Contact escalations trigger tool + alert
- Tools executed only when appropriate context is detected
- System is extensible with new tools
- LLM maintains tone and logic across sessions
- RAG pipeline initializes automatically on first run
- Successful deployment on HuggingFace Spaces
- Efficient session management
- Proper handling of tool calls and notifications

---

## 6. Deliverables

- Web app chatbot (Member support agent)
- Tool-driven chat framework
- RAG engine (embeddings + retriever)
- Automated RAG pipeline initialization
- Tools module + handler
- Pushover integration
- HuggingFace Spaces deployment
- Complete documentation + `README.md`
- Session management system
- Error handling and logging

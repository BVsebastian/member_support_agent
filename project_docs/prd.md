# 📝 Product Requirements Document (PRD)

**Project Name**: Member Support Ai Agent  
**Organization**: Horizon Bay Credit Union  
**Owner**: Benedict Sebastian  
**Engineer**: [AI Engineer Name]  
**Date**: [Insert Date]

---

## 1. Objective

Develop a web-based AI assistant named **Alexa** that serves as a Member Support Representative for Horizon Bay Credit Union. Alexa will respond to frequently asked questions using internal knowledge, maintain a consistent professional tone, and notify human staff when escalation or follow-up is needed.

---

## 2. Scope

**✅ In Scope**

- LLM-powered chatbot trained to simulate a Horizon Bay CU support agent
- Identity and tone built from an internal resource (Alexa’s Identity Profile)
- Push notifications via Pushover for:
  - Unresolved or unknown questions
  - Contact details or human support requests
- Retrieval-Augmented Generation (RAG) using vector-based knowledge base from curated FAQs and support manuals
- Web-based front-end using Gradio or Streamlit

**❌ Out of Scope**

- Secure transactions, live account access, or authentication
- Real-time human chat (this version only logs and notifies)
- Integration with core banking systems

---

## 3. Features

### 🔹 Feature 1: Agent Identity via System Prompt

- Alexa represents a virtual member support rep
- Behavior, tone, and values based on the “AI Agent Identity Profile” document
- System prompt injected at every conversation session to ensure consistent tone and behavior

### 🔹 Feature 2: Unknown Question Logging

- Tool: `record_unknown_question(question)`
- Logs unknown queries with timestamp and context
- Pushes alert to Pushover support channel

### 🔹 Feature 3: Contact Logging for Escalation

- Tool: `record_user_details(email, name?, notes?)`
- Triggered when user shares contact or requests escalation
- Sends Pushover alert with captured details

### 🔹 Feature 4: RAG-based FAQ Support

- Documents:
  - Horizon Bay CU Account Support Manual
  - Why Join Horizon Bay Credit Union
  - Horizon Bay CU Member Services Toolkit
- Process:
  - Documents are chunked and embedded using OpenAI/HuggingFace
  - Stored in ChromaDB or FAISS
  - Top-N relevant chunks are retrieved and appended to the AI’s context

---

## 4. Required Documents

- AI Agent Identity Profile: Alexa
- Account Support Manual
- Membership Benefits Guide
- Member Services Toolkit

---

## 5. Success Criteria

- 80%+ FAQ accuracy in test sessions
- All unknown questions logged and alerted
- Contact escalation triggers notifications reliably
- RAG response quality improves with additional knowledge base inputs
- Agent tone consistently matches identity profile across sessions

---

## 6. Deliverables

- CUAssist chatbot (web app frontend)
- Fully functional system prompt and personality model for Alexa
- Working integration with Pushover for alerts
- Vectorized knowledge base and RAG query handler
- Deployment-ready codebase with setup instructions

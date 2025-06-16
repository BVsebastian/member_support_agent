import gradio as gr
from agent.retriever import Retriever
from app.prompt_manager import get_system_prompt
from app.state import SessionState
from openai import OpenAI
import os
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
session_state = SessionState()

def update_session_state(message, role):
    session_state.add_message(role, message)

def get_session_info():
    return session_state.get_session_info()

def respond(message, history):
    print(f"\nUser Question: {message}")  # Print the question

    # Add user message to session state
    session_state.add_message("user", message)
    
    # 1. Get system prompt with Alexa's identity
    system_prompt = get_system_prompt()
    
    # 2. Retrieve relevant FAQ chunks
    retriever = Retriever()
    relevant_chunks = retriever.retrieve_top_chunks(message)
    
    # 3. Build context with system prompt and FAQ chunks
    context = f"{system_prompt}\n\nRelevant Information:\n"
    for chunk in relevant_chunks:
        context += f"- {chunk['text']}\n"

    # Add session history to context
    context += "\n\nConversation History:\n"
    for msg in session_state.get_messages():
        context += f"{msg['role']}: {msg['content']}\n"
    
    # Add session info
    context += f"\nSession Duration: {session_state.get_session_duration()} seconds\n"
    context += f"Total Messages: {len(session_state.get_messages())}\n"

    # 4. Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": message}
        ]
    )
    
    answer = response.choices[0].message.content
    print(f"\nAssistant Response: {answer}")  # Print the response


    # Add assistant response to session state
    session_state.add_message("assistant", answer)

    # Check if the response is an escalation
    if "escalate" in answer.lower():
        session_state.set_flag("has_escalated", True)
        return "I'm sorry, I can't handle that question. Please contact our support team for assistance.", history==[]
    
    return answer

# Create the Gradio interface
iface = gr.ChatInterface(
    fn=respond,
    title="Member Support AI Agent",
    description="Ask me anything about Horizon Bay Credit Union services!",
    examples=[
        "What documents do I need to open an account?",
        "How do I reset my password?",
        "What are the fees for a checking account?",
    ]
)

if __name__ == "__main__":
    iface.launch()
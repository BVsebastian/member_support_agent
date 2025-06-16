import gradio as gr
from agent.retriever import Retriever
from app.prompt_manager import get_system_prompt
from app.state import SessionState
from openai import OpenAI
import os
from dotenv import load_dotenv
import app.pushover_alerts as pushover
from datetime import datetime

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

    # Add session history
    context += "\n\nConversation History:\n"
    for msg in session_state.get_messages():
        context += f"{msg['role']}: {msg['content']}\n"

    # Add session info
    context += f"\nSession Duration: {session_state.get_session_duration()} seconds\n"
    context += f"Total Messages: {len(session_state.get_messages())}\n"

    # Add escalation status
    context += f"\nEscalation Status: {'Escalated' if session_state.get_flag('has_escalated') else 'Not Escalated'}\n"
    

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

    # Check for escalation
    if "[ESCALATION]" in answer:
        # Set escalation flag and store original request if this is first escalation
        if not session_state.get_flag("has_escalated"):
            # Store the first message that mentions escalation
            session_state.set_flag("original_request", message)
            session_state.set_flag("has_escalated", True)
        
        # Initialize contact info dictionary
        contact_info = {}
        
        # Extract user details from the response
        user_details = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_state.session_id,
            "original_request": session_state.get_flag("original_request") or "No specific issue mentioned"
        }
        print(f"\noriginal request: {session_state.get_flag('original_request')}")

        # Extract formatted user details from the response if they exist
        if "[USER_DETAILS]" in answer:
            details_section = answer.split("[USER_DETAILS]")[1].split("[/USER_DETAILS]")[0]
            # Parse the details into a dictionary
            for item in details_section.split(","):
                if "=" in item:
                    key, value = item.split("=")
                    contact_info[key.strip()] = value.strip()
            
            # Add contact info to user_details
            user_details["contact_info"] = contact_info
            
            # Create a user-friendly summary of the details
            details_summary = "\nHere are the details I've collected:\n"
            if "name" in contact_info:
                details_summary += f"- Name: {contact_info['name']}\n"
            if "email" in contact_info:
                details_summary += f"- Email: {contact_info['email']}\n"
            if "phone" in contact_info:
                details_summary += f"- Phone: {contact_info['phone']}\n"
            
            # Remove the USER_DETAILS section and add our summary
            answer = answer.replace(f"[USER_DETAILS]{details_section}[/USER_DETAILS]", "").strip()
            answer = answer + details_summary

            # Send notification with whatever details we have
            print(f"\nUser Details: {user_details}")
            pushover.record_user_details(user_details)
        
        # Remove the ESCALATION tag from the response
        answer = answer.replace("[ESCALATION]", "").strip()

    # Add assistant response to session state
    session_state.add_message("assistant", answer)

    print(f"\nSession State: {session_state.get_session_info()}")
    print(f"\nAssistant Response: {answer}")

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
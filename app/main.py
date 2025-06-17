import gradio as gr
from agent.retriever import Retriever
from app.prompt_manager import get_system_prompt
from app.state import session_state  
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from tools import handle_tool_call

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define tool schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "send_notification",
            "description": "Send a notification about an escalation request",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_request": {
                        "type": "string",
                        "description": "The user's original request/issue"
                    },
                    "contact_info": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"}
                        }
                    }
                },
                "required": ["original_request"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Record user details for follow-up",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_details": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"},
                            "notes": {"type": "string"}
                        }
                    }
                },
                "required": ["user_details"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log_unknown_question",
            "description": "Log questions that couldn't be answered",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The unanswered question"
                    },
                    "context": {
                        "type": "object",
                        "description": "Additional context about the question"
                    }
                },
                "required": ["question"]
            }
        }
    }
]

def update_session_state(message, role):
    session_state.add_message(role, message)

def get_session_info():
    return session_state.get_session_info()

def respond(message, history):
    print(f"\nUser Question: {message}")

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

    # 4. Call OpenAI API with tools
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": message}
    ]

    done = False
    while not done:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools
        )
        
        message = response.choices[0].message
        
        if response.choices[0].finish_reason == "tool_calls":
            # Handle tool calls
            tool_calls = message.tool_calls
            for tool_call in tool_calls:
                # Execute the tool call
                result = handle_tool_call({
                    "name": tool_call.function.name,
                    "params": json.loads(tool_call.function.arguments)
                })
                
                # Add the tool call and its result to the conversation
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id
                })
                
                # Log the tool call result
                print(f"\nTool Call Result ({tool_call.function.name}): {result}")
                
                # If this was a notification and it failed because one was already sent,
                # we should let the LLM know to adjust its response
                if (tool_call.function.name == "send_notification" and 
                    not result.get("success") and 
                    "already sent" in result.get("message", "").lower()):
                    messages.append({
                        "role": "system",
                        "content": "A notification has already been sent for this escalation. Please acknowledge this to the user and continue with the conversation."
                    })
        else:
            done = True

    # Add assistant response to session state
    session_state.add_message("assistant", message.content)

    print(f"\nSession State: {session_state.get_session_info()}")
    print(f"\nAssistant Response: {message.content}")

    return message.content

# Create the Gradio interface
iface = gr.ChatInterface(
    fn=respond,
    title="Member Support AI Agent",
    description="Ask me anything about Horizon Bay Credit Union services!",
    examples=[
        "What documents do I need to open an account?",
        "How do I reset my password?",
        "What are the fees for a checking account?",
    ],
    type="messages"  # Use the new message format
)

if __name__ == "__main__":
    iface.launch()
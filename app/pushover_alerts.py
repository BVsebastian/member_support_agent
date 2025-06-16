import json
import datetime
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

def record_user_details(details):
    """Record user details and send alert."""
    # Get contact info if available
    contact_info = details.get("contact_info", {})
    
    # Format the message with the contact information
    message = f"New Escalation Request\n\n"
    message += f"Time: {details.get('timestamp', 'Unknown')}\n"
    message += f"Session ID: {details.get('session_id', 'Unknown')}\n\n"
    
    # Add contact information if available
    message += f"Contact Details:\n"
    if contact_info:
        message += f"- Name: {contact_info.get('name', 'Not provided')}\n"
        message += f"- Email: {contact_info.get('email', 'Not provided')}\n"
        message += f"- Phone: {contact_info.get('phone', 'Not provided')}\n"
    else:
        message += "No contact details provided\n"
    message += "\n"
    
    # Add the user's original request
    message += f"User's Request:\n{details.get('original_request', 'No specific issue mentioned')}"
    
    # Send the push notification
    push(message)
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}
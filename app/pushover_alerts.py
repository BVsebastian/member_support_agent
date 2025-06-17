import json
import datetime
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def push(text, title="Member Support Alert"):
    """
    Send a push notification via Pushover.
    
    Args:
        text (str): The message content
        title (str): The notification title
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": os.getenv("PUSHOVER_TOKEN"),
                "user": os.getenv("PUSHOVER_USER"),
                "message": text,
                "title": title,
                "priority": 1  # High priority for escalations
            }
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        return False

def record_user_details(details):
    """
    Record user details and send alert.
    
    Args:
        details (dict): Dictionary containing:
            - original_request (str): The user's original request/issue
            - contact_info (dict): Dictionary of contact details
            - timestamp (str): ISO format timestamp
            - session_id (str): Session identifier
    
    Returns:
        dict: Result of the operation
    """
    try:
        # Get contact info if available
        contact_info = details.get("contact_info", {})
        
        # Format the message with the contact information
        message = f"New Escalation Request\n\n"
        message += f"Time: {details.get('timestamp', 'Unknown')}\n"
        message += f"Session ID: {details.get('session_id', 'Unknown')}\n\n"
        
        # Add contact information if available
        if contact_info:
            message += f"Contact Details:\n"
            message += f"- Name: {contact_info.get('name', 'Not provided')}\n"
            message += f"- Email: {contact_info.get('email', 'Not provided')}\n"
            message += f"- Phone: {contact_info.get('phone', 'Not provided')}\n"
        else:
            message += "No contact details provided\n"
        message += "\n"
        
        # Add the user's original request
        message += f"User's Request:\n{details.get('original_request', 'No specific issue mentioned')}"
        
        # Send the push notification
        success = push(message)
        
        return {
            "success": success,
            "message": "Notification sent successfully" if success else "Failed to send notification"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error processing notification: {str(e)}"
        }

def record_unknown_question(question):
    """
    Record an unanswered question and send alert.
    
    Args:
        question (dict): Dictionary containing:
            - question (str): The unanswered question
            - context (dict, optional): Additional context
    
    Returns:
        dict: Result of the operation
    """
    try:
        message = f"Unanswered Question\n\n"
        message += f"Question: {question.get('question', 'Unknown')}\n"
        
        if context := question.get('context'):
            message += f"\nContext:\n{json.dumps(context, indent=2)}"
        
        success = push(message, title="Unanswered Question Alert")
        
        return {
            "success": success,
            "message": "Question logged successfully" if success else "Failed to log question"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error processing question: {str(e)}"
        }
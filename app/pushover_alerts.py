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
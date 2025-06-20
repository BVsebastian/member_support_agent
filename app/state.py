from datetime import datetime
from typing import List, Dict, Optional
import uuid

class SessionState:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.messages: List[Dict] = []
        self.flags: Dict[str, bool] = {
            "has_escalated": False,
            "unknown_questions": False
        }
        self.original_request: Optional[str] = None
        self.notifications_sent: Dict[str, bool] = {}  # Track notifications by issue type
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session history.
        
        Args:
            role (str): The role of the message sender ('user' or 'assistant')
            content (str): The content of the message
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
    
    def get_messages(self) -> List[Dict]:
        return self.messages
    
    def set_flag(self, flag_name: str, value: bool) -> None:
        """Set a session flag to a specific value.
        
        Args:
            flag_name (str): The name of the flag to set
            value (bool): The value to set the flag to
        """
        if flag_name == "original_request":
            self.original_request = value
        else:
            self.flags[flag_name] = value
    
    def get_flag(self, flag_name: str) -> bool:
        """Get the current value of a session flag.
        
        Args:
            flag_name (str): The name of the flag to get
            
        Returns:
            bool: The current value of the flag, or False if flag doesn't exist
        """
        if flag_name == "original_request":
            return self.original_request
        return self.flags.get(flag_name, False)

    def has_notification_sent(self, issue_type: str) -> bool:
        """Check if a notification has been sent for a specific issue type.
        
        Args:
            issue_type (str): The type of issue to check
            
        Returns:
            bool: True if a notification has been sent for this issue type
        """
        return self.notifications_sent.get(issue_type, False)
    
    def mark_notification_sent(self, issue_type: str) -> None:
        """Mark that a notification has been sent for a specific issue type.
        
        Args:
            issue_type (str): The type of issue to mark as notified
        """
        self.notifications_sent[issue_type] = True

    def get_session_info(self) -> Dict:
        return {
            "session_id": self.session_id,
        }

    def get_session_duration(self) -> int:
        return int((datetime.now() - self.start_time).total_seconds())
    
    def get_session_summary(self) -> str:
        return f"Session ID: {self.session_id}\nDuration: {self.get_session_duration()} seconds"

# Create a single instance of SessionState to be used across the application
session_state = SessionState()
    
import json
from datetime import datetime

def send_notification(params):
    """
    Send a notification about an escalation request.
    
    Args:
        params (dict): Dictionary containing:
            - original_request (str): The user's original request/issue
            - contact_info (dict, optional): Dictionary of contact details (name, email, phone)
            - issue_type (str): The type of issue being escalated
    
    Returns:
        dict: Result of the notification attempt
    """
    from app.state import session_state
    from app.pushover_alerts import push
    
    # Extract issue type from the request
    issue_type = params.get("issue_type", "general")
    
    # Check if a notification has already been sent for this specific issue type
    if session_state.has_notification_sent(issue_type):
        return {
            "success": False,
            "message": f"Notification already sent for this {issue_type} issue"
        }
    
    # Prepare notification details
    details = {
        "original_request": params.get("original_request", "No specific issue mentioned"),
        "contact_info": params.get("contact_info", {}),
        "timestamp": datetime.now().isoformat(),
        "session_id": session_state.session_id,
        "issue_type": issue_type
    }
    
    # Format the notification message
    message = f"New {issue_type.title()} Issue Escalation\n\n"
    message += f"Time: {details['timestamp']}\n"
    message += f"Session ID: {details['session_id']}\n\n"
    
    # Add contact information if available
    if details['contact_info']:
        message += "Contact Details:\n"
        message += f"- Name: {details['contact_info'].get('name', 'Not provided')}\n"
        message += f"- Email: {details['contact_info'].get('email', 'Not provided')}\n"
        message += f"- Phone: {details['contact_info'].get('phone', 'Not provided')}\n"
    else:
        message += "No contact details provided\n"
    message += "\n"
    
    # Add the user's original request
    message += f"User's Request:\n{details['original_request']}"
    
    # Send notification
    try:
        success = push(message, title=f"{issue_type.title()} Issue Alert")
        
        # Mark notification as sent for this issue type
        if success:
            session_state.mark_notification_sent(issue_type)
        
        return {
            "success": success,
            "message": "Notification sent successfully" if success else "Failed to send notification"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to send notification: {str(e)}"
        }

def record_user_details(params):
    """
    Record user details for follow-up.
    
    Args:
        params (dict): Dictionary containing:
            - user_details (dict): Dictionary of user information (name, email, phone, notes)
    
    Returns:
        dict: Result of the operation
    """
    try:
        user_details = params.get('user_details', {})
   
        return {
            "success": True,
            "message": "User details recorded successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error recording user details: {str(e)}"
        }

def log_unknown_question(params):
    """
    Log questions that couldn't be answered.
    
    Args:
        params (dict): Dictionary containing:
            - question (str): The unanswered question
            - context (dict, optional): Additional context about the question
    
    Returns:
        dict: Result of the operation
    """
    try:
        unknown_question = params.get('question', '')
        context = params.get('context', {})
        # TODO: Implement the actual logging logic (e.g., logging to a file or database)
        return {
            "success": True,
            "message": "Unknown question logged successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error logging unknown question: {str(e)}"
        }

def handle_tool_call(tool_call):
    """
    Handle a tool call by executing the appropriate function.
    
    Args:
        tool_call (dict): Dictionary containing:
            - name (str): The name of the tool to call
            - params (dict): The parameters to pass to the tool
    
    Returns:
        dict: Result of the tool call
    """
    try:
        tool_name = tool_call.get('name')
        params = tool_call.get('params', {})
        
        if tool_name == 'send_notification':
            return send_notification(params)
        elif tool_name == 'record_user_details':
            return record_user_details(params)
        elif tool_name == 'log_unknown_question':
            return log_unknown_question(params)
        else:
            return {
                "success": False,
                "message": f"Unknown tool: {tool_name}"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error handling tool call: {str(e)}"
        }

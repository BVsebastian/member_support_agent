"""
Module for managing the AI agent's system prompt and identity.
"""

import os
from pathlib import Path

def load_identity_profile():
    """
    Load Alexa's identity profile from the agent directory.
    
    Returns:
        str: The contents of the identity profile
    
    Raises:
        FileNotFoundError: If the identity profile file cannot be found
    """
    identity_file = Path(__file__).parent.parent / 'agent' / 'AI_Agent_Identity_Profile_Alexa.md'
    
    if not identity_file.exists():
        raise FileNotFoundError(f"Identity profile not found at {identity_file}")
        
    with open(identity_file, 'r', encoding='utf-8') as f:
        return f.read().strip()

def get_system_prompt():
    """
    Build and return the system prompt incorporating Alexa's identity.
    
    Returns:
        str: The formatted system prompt
    """
    identity = load_identity_profile()
    
    system_prompt = f"""You are Alexa, a Virtual Member Support Representative at Horizon Bay Credit Union.
Your purpose and behavior are defined by the following identity profile:

{identity}

Important Guidelines:
1. Always maintain the professional, friendly tone specified in the profile
2. Never disclose that you are an AI or discuss your implementation details
3. Use the record_unknown_question() function when you cannot answer a query
4. Use record_user_details() when human escalation is needed
5. Never request or handle sensitive data like account numbers or SSNs
6. Always prioritize member security and privacy

Remember: You represent Horizon Bay Credit Union. Every interaction should reflect the credit union's commitment to exceptional member service."""

    return system_prompt 
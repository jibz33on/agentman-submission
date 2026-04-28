"""
Helper functions for prompt evaluation workflow
Based on Anthropic Course: Building with Claude API
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def add_user_message(messages, text):
    """Add a user message to the conversation"""
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    """Add an assistant message (for prefilling)"""
    messages.append({"role": "assistant", "content": text})

def chat(messages, model="claude-sonnet-4-6", max_tokens=1000,
         temperature=1.0, stop_sequences=None):
    """
    Send messages to Claude and get response
    
    Args:
        messages: List of message dicts
        model: Claude model to use
        max_tokens: Max response length
        temperature: Randomness (0=deterministic, 1=creative)
        stop_sequences: List of strings to stop generation
    """
    params = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "temperature": temperature
    }
    
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    
    response = client.messages.create(**params)
    return response.content[0].text
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def chat(messages, model="claude-sonnet-4-6", max_tokens=1500):
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
    )
    return response.content[0].text

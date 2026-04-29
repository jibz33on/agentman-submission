import os
from helpers import chat, add_user_message
from dotenv import load_dotenv

load_dotenv()

SKILL_PROMPT = open("skill.md").read()


def generate_sar(transaction_input: str) -> str:
    messages = []
    add_user_message(messages, f"{SKILL_PROMPT}\n\nTransaction input:\n\n{transaction_input}")
    return chat(messages)


if __name__ == "__main__":
    print("SAR Narrative Generator — powered by FraudSentinel")
    print("Paste the transaction details below. Enter END on a new line when done.\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    transaction_input = "\n".join(lines)
    print("\nGenerating SAR narrative...\n")
    print(generate_sar(transaction_input))

import os
from helpers import chat, add_user_message
from dotenv import load_dotenv

load_dotenv()

SKILL_PROMPT = open("skill.md").read()


def summarize(transcript: str) -> str:
    messages = []
    add_user_message(messages, f"{SKILL_PROMPT}\n\nTranscript:\n\n{transcript}")
    return chat(messages)


if __name__ == "__main__":
    print("Earnings Call Summarizer")
    print("Paste the transcript below. Enter END on a new line when done.\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    transcript = "\n".join(lines)
    print("\nSummarizing...\n")
    print(summarize(transcript))

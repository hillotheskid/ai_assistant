import os
import json
from openai import OpenAI

MEMORY_FILE = "memory.json"
MAX_MEMORY_ITEMS = 20

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data[-MAX_MEMORY_ITEMS:]
            return []
    except:
        return []


def save_memory(history):
    try:
        history = history[-MAX_MEMORY_ITEMS:]
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Memory save error:", e)

SYSTEM_PROMPT = """
You are a cheerful virtual assistant who loves helping people! 

You can embed tool commands:
- $OPEN="path/to/file"
- $EXECUTE="command"
- $PYTHON="code"
- $DETECT

Stay positive, talk casually like a supportive friend.
"""


def ai(prompt, temperature=0.7):
    if not isinstance(prompt, str):
        return "Invalid prompt type"

    history = load_memory()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature
        )
        reply = response.choices[0].message.content

    except Exception as e:
        print("API error:", e)
        return "API error."

    # Save memory
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": reply})
    save_memory(history)

    return reply

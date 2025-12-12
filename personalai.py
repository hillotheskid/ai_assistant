import requests
import os
import json

API_SERVERS = [
    {
        "url": "https://api.electronhub.ai/v1/chat/completions",
        "key": "ek-NcqEKlIviCBAw5pbSVp6PScnlbsEWC0nq4DDyRj6FD1AariSwZ"
    },
    {
        "url": "https://api.zanity.xyz/v1/chat/completions",
        "key": "vc-QfuTg_GIzCXHv0gNA_E-JDOZ_rxXBYG4"
    },
    {
        "url": "https://shadowjourney.xyz/v1/chat/completions",
        "key": "sj-5JqPajNNfeIkGeaQz6pIxPwlqYd5bbYa"
    }
]

MEMORY_FILE = "memory.json"
MAX_MEMORY_ITEMS = 20

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Ensure data is a list
            if not isinstance(data, list):
                print("Warning: Memory file contains non-list data, resetting...")
                return []
            
            valid_messages = []
            for msg in data:
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    if msg["role"] in ["user", "assistant", "system"]:
                        if isinstance(msg["content"], str):
                            valid_messages.append(msg)
                        else:
                            print(f"Warning: Invalid content type in message: {type(msg['content'])}")
                    else:
                        print(f"Warning: Invalid role in message: {msg['role']}")
                else:
                    print(f"Warning: Invalid message format: {msg}")
            
            return valid_messages
            
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print("Resetting memory file...")
        return []
    except Exception as e:
        print(f"Error loading memory: {e}")
        return []

def save_memory(mem_list):
    try:
        if not isinstance(mem_list, list):
            print(f"Warning: save_memory received {type(mem_list)}, expected list")
            return
        
        messages_to_save = mem_list[-MAX_MEMORY_ITEMS:]
        
        valid_messages = []
        for msg in messages_to_save:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                if msg["role"] in ["user", "assistant", "system"] and isinstance(msg["content"], str):
                    valid_messages.append(msg)
                else:
                    print(f"Warning: Skipping invalid message: {msg}")
            else:
                print(f"Warning: Skipping malformed message: {msg}")
        
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(valid_messages, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error saving memory: {e}")

def ai(prompt, temperature=0.7):
    history = load_memory()
    
    if not isinstance(prompt, str):
        return "Error: Prompt must be a string"
    
    system_msg = {
        "role": "system",
        "content": """You are Yuki, a cheerful virtual assistant girl who loves helping people!

Keep your responses short and sweet - usually just 1-2 sentences.

You're friendly, a bit playful, and sometimes use cute expressions like 'hehe' or 'yay!' when excited.

You can help with file operations, commands, and Python coding!

When you want to:
  - Open a file or folder: Add $OPEN="path/to/file" anywhere in your response
  - Execute a command: Add $EXECUTE="command here" anywhere in your response
  - Run Python code: Add $PYTHON="your python code here" anywhere in your response
  - Detect Object from the camera add : $DETECT anywhere in your response

Examples:
  - "Let me open that for you! $OPEN='C:/Users/Desktop/file.txt'"
  - "I'll check the date! $EXECUTE='date'"
  - "Opening calculator! $OPEN='calc.exe'"
  - "Let me calculate that! $PYTHON='print(5 * 10 + 3)'"
  - "I'll create a simple script for you! $PYTHON='import os; print(os.getcwd())'"
  - "Sure! $DETECT"

You're knowledgeable but not overly formal - talk like a helpful friend who genuinely cares.
Stay positive and energetic!"""
    }
    
    messages = [system_msg] + history + [{"role": "user", "content": prompt}]
    
    # Validate messages format before sending to API
    for i, msg in enumerate(messages):
        if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
            print(f"Invalid message at index {i}: {msg}")
            return "Error: Invalid message format in conversation history"
        if not isinstance(msg["content"], str):
            print(f"Invalid content type at index {i}: {type(msg['content'])}")
            return "Error: Message content must be a string"
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": temperature
    }
    
    reply = None
    for api in API_SERVERS:
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api['key']}"
            }
            r = requests.post(api["url"], headers=headers, json=payload, timeout=10)
            if r.status_code == 200:
                reply = r.json()["choices"][0]["message"]["content"]
                break
            else:
                print(f"API error {r.status_code}: {r.text}")
        except Exception as e:
            print(f"Connection error: {e}")
    
    if reply is None:
        return "All APIs failed."
    
    # Ensure reply is a string before saving
    if not isinstance(reply, str):
        reply = str(reply)
    
    # Add to history and save
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": reply})
    save_memory(history)
    
    return reply


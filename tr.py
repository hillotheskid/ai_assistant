import colorama
from colorama import Fore, Style
import requests
import time

def transcribe_wav(filename):
    print(Fore.CYAN + "[DEBUG] Starting transcription..." + Style.RESET_ALL)
    
    try:
        with open(filename, "rb") as f:
            audio_data = f.read()
        
        headers = {
            "Authorization": f"Bearer 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",
            "Content-Type": "audio/wav"
        }
        
        response = requests.post(
            "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo",
            headers=headers,
            data=audio_data
        )
        
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"[DEBUG] Response content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict) and "text" in result:
                return result["text"]
            elif isinstance(result, list) and len(result) > 0:
                return result[0].get("text", "")
            else:
                return str(result)
        elif response.status_code == 503:
            print(Fore.YELLOW + "[DEBUG] Model is loading, waiting 5 seconds..." + Style.RESET_ALL)
            time.sleep(5)
            return ""
        else:
            print(Fore.RED + f"API ERROR: {response.status_code}" + Style.RESET_ALL)
            print(f"Response: {response.text}")
            return ""
            
    except Exception as e:
        print(Fore.RED + f"[ERROR] Transcription failed: {e}" + Style.RESET_ALL)
        return ""
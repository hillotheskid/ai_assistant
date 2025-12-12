import winsound
import time
from ai import ai
import os
from tts import tts
import random
from deep_translator import GoogleTranslator
import colorama
from colorama import Fore, Style
from cmds import detect_and_process_commands
from tr import transcribe_wav
import keyboard


def sleep(seconds=1):
    time.sleep(seconds) 

colorama.init(autoreset=True)

def translate(text, target_lang):
    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
    return translated

AUDIO_FILE = "input.wav"
OUTPUT_FILE = "out.wav"

def translate(text, target_lang):
    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
    return translated

def is_speaking():
    if os.path.exists(OUTPUT_FILE):
        file_age = time.time() - os.path.getmtime(OUTPUT_FILE)
        return file_age < 10
    return False




def record_chunk(seconds=5, output_filename="input.wav"):
    import pyaudio, wave, os

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    if os.path.exists(output_filename):
        os.remove(output_filename)

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        frames_to_record = int(RATE / CHUNK * seconds)

        print(f"Recording {seconds} second(s)…")
        for _ in range(frames_to_record):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        sampwidth = p.get_sample_size(FORMAT)
        p.terminate()

        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(sampwidth)
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        print(f"Saved recording to {output_filename}")
        return output_filename

    except Exception as e:
        print("Recording failed:", e)
        p.terminate()
        if os.path.exists(output_filename):
            os.remove(output_filename)
        return None


def run_text_mode():
    print("Text Mode Active")
    while True:
        user = input("\nYou: ").strip()
        if user.lower() == "exit":
            print("Exiting Text Mode")
            break

        print("AI is processing...")
        raw_reply = ai(user)
        clean_reply, pending_commands = detect_and_process_commands(raw_reply)
        print("AI:", clean_reply)

        try:
            jp = translate(clean_reply, "ja")
            tts(jp)

            winsound.PlaySound(OUTPUT_FILE, winsound.SND_FILENAME)

            time.sleep(0.1)
            if os.path.exists(OUTPUT_FILE):
                os.remove(OUTPUT_FILE)
        except Exception as e:
            print("TTS error:", e)

        for result in pending_commands:
            print("Command:", result)



def run_voice_mode():
    print("Voice Mode Active")
    print("Hold Left Shift to record")

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    while True:
        if keyboard.is_pressed("shift"):
            if is_speaking():
                time.sleep(0.1)
                continue

            print("[RECORDING]")
            audio_file = record_chunk()
            print("[STOPPED]")

            if not audio_file:
                print("Recording failed")
                continue

            text = transcribe_wav(audio_file)
            if not text:
                continue

            if text.lower() == "end conversation":
                print("Ending Voice Mode")
                break

            print("Heard:", text)
            print("AI is processing...")

            raw_reply = ai(text)
            clean_reply, pending_commands = detect_and_process_commands(raw_reply)
            print("AI:", clean_reply)

            try:
                jp = translate(clean_reply, "ja")
                tts(jp)

                winsound.PlaySound(OUTPUT_FILE, winsound.SND_FILENAME)

                time.sleep(0.1)
                if os.path.exists(OUTPUT_FILE):
                    os.remove(OUTPUT_FILE)
            except Exception as e:
                print("TTS error:", e)

            for result in pending_commands:
                print("Command:", result)

        time.sleep(0.05)

def runvoicevox():
    from runvoicevox import run_voicevox
    return run_voicevox()

def main():
    response = input("Would you like to run voicevox? (y/n): ").strip().lower()
    if response == "y":
        runvoicevox()
    elif response == "n":
        pass
    else:
        print("Invalid response")

    print("Select mode:")
    print("1. Text Mode")
    print("2. Voice Mode")
    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        run_text_mode()
    elif mode == "2":
        run_voice_mode()
    else:
        print("Invalid mode")


main()


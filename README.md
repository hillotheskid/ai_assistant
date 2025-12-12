# 🎙️ AI Voice/Text Assistant

A modular Python assistant capable of:

-   **voice recognition**
-   Multi-language **text interaction**
-   AI-generated responses
-   Automatic **command execution** (open apps, run paths, etc.)
-   Automatic **translation → Japanese → TTS**
-   VoiceVox integration
-   Smart executable path detection using both filesystem search + AI
    reasoning

This project includes both **Text Mode** and **Voice Mode**, allowing
you to talk to the AI through your keyboard or microphone.

------------------------------------------------------------------------

## 🚀 Features

### **1. Text Mode**

-   Type messages directly
-   AI generates responses
-   System detects embedded commands in replies
-   Replies are translated to Japanese → spoken using VoiceVox TTS

### **2. Voice Mode**

-   Hold **Left Shift** to record
-   Audio gets transcribed
-   Assistant replies verbally using TTS
-   Automatic noise-aware recording
-   Recording safety checks (avoid overlapping speech)

### **3. Intelligent Executable Detection**

The assistant can **find and launch apps** on your system.

The logic includes: - Local executable search - AI-assisted path
selection if multiple matches exist - Automatic Roblox version folder
detection - Fallback: AI generates an exact Windows 11 file path using
your real username

### **4. AI Command Processor**

The `cmds.py` module can detect commands embedded in AI output such as:

    <run:roblox player>
    <open:discord>
    <execute:"C:/path/to/app.exe">

The system then executes them automatically.

------------------------------------------------------------------------

## 📁 Project Structure

    project/
    │   main.py
    │   setup.py
    │   requirements.txt
    │
    ├── ai/
    │   ai.py               # AI logic / model wrapper
    │
    ├── tts/
    │   tts.py              # Japanese TTS generator
    │
    ├── cmds/
    │   cmds.py             # Command detection + app launching
    │
    ├── tr/
    │   transcribe_wav.py   # Audio transcription
    │
    └── runvoicevox/
        runvoicevox.py      # Optional VoiceVox standalone runner

------------------------------------------------------------------------

## 🔧 Installation & Setup

### **1. Install Python 3.9+**

Ensure you have Python installed:

    python --version

### **2. Run the setup script**

This installs all requirements and starts the project:

    python setup.py

The setup script will:

-   Print credits
-   Install all dependencies from `requirements.txt`
-   Launch `main.py`

NOTES :

To install voicevox you need `docker` (https://www.docker.com/)
And run `docker pull voicevox/voicevox_engine:cpu-latest` for CPU
or `docker pull voicevox/voicevox_engine:nvidia-latest` for GPU in your terminal


------------------------------------------------------------------------

## 🎤 Usage

After launching:

### **Step 1 --- VoiceVox?**

You will be asked:

    Would you like to run voicevox? (y/n)

Choose **y** if you want built-in VoiceVox TTS running locally.

------------------------------------------------------------------------

### **Step 2 --- Select Mode**

    Select mode:
    1. Text Mode
    2. Voice Mode

------------------------------------------------------------------------

## 📚 Detailed Behavior

### **Text Mode**

    You: hello
    AI is processing...
    AI: Konbanwa!

Behind the scenes:

1.  AI generates reply\
2.  Command handler detects any embedded commands\
3.  Reply is translated to Japanese\
4.  TTS audio is generated\
5.  Audio is played automatically\
6.  Temporary output files are auto-deleted

------------------------------------------------------------------------

### **Voice Mode**

-   Hold **Left Shift** to record\
-   Release to transcribe\
-   AI responds via TTS\
-   Commands are executed

Failsafe: - If TTS file is still "fresh", assistant won't start a new
recording\
- Prevents overlapping voice playback

------------------------------------------------------------------------

## 🧠 Translation Engine

The project uses:

    GoogleTranslator(source='auto', target='ja')

Every response is:

1.  AI →\
2.  Cleaned & command-filtered →\
3.  Translated to Japanese →\
4.  Spoken aloud via VoiceVox

------------------------------------------------------------------------

## 🔍 Smart Executable Searching

The `get_path_exe()` function:

-   Searches disk for executables\
-   For multiple results → AI chooses the correct one\
-   Special Roblox logic:
    -   Auto-detects version folders
    -   Picks correct Player/Studio .exe\
-   AI fallback constructs a real Windows 11 path using your actual
    username

Example AI prompt used:

    Give me the EXACT file path for discord.exe on Windows 11.
    Current username is Hillorius.
    Replace ANY placeholders with the actual username.

------------------------------------------------------------------------

## 🛠 Requirements

Common dependencies:

-   `pyaudio`
-   `googletrans` / `deep-translator`
-   `keyboard`
-   `colorama`
-   `winsound`
-   `wave`
-   `openai` / your AI backend
-   VoiceVox CLI

All installed by:

    python setup.py

------------------------------------------------------------------------

## 🧩 Notes

-   `input.wav` and `out.wav` are reused, auto-cleaned after playback.
-   Supports both fast console usage & full voice assistant mode.
-   Does **not** require internet for TTS if VoiceVox is installed.

------------------------------------------------------------------------

## Credits

Made by **Hillorius**\

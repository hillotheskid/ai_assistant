import os
import shutil
import glob
import platform
import subprocess
import re
from ai import ai

def search_executable(name):
    path = shutil.which(name)
    if path:
        return path
    
    path = shutil.which(f"{name}.exe")
    if path:
        return path
    
    roots = [
        os.environ.get('ProgramFiles', ''),
        os.environ.get('ProgramFiles(x86)', ''),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs')
    ]
    
    found_paths = []
    
    for root in filter(None, roots):
        if not os.path.exists(root):
            continue
            
        patterns = [
            f"**/{name}",
            f"**/{name}.exe", 
            f"**/*{name}*.exe"  
        ]
        
        for pattern in patterns:
            matches = glob.glob(os.path.join(root, pattern), recursive=True)
            found_paths.extend(matches)
    
    return found_paths if found_paths else None

def get_path_exe(app_name):
    """
    Combined approach: search filesystem first, then ask AI for guidance
    """
    print(f"Searching for {app_name}...")
    
    # First, try our automated search
    local_results = search_executable(app_name)
    
    if local_results:
        print(f"Found locally: {local_results}")
        # If we found multiple, ask AI which is correct
        if len(local_results) > 1:
            paths_str = "\n".join(local_results)
            ai_response = ai(
                f"I found these {app_name} executable paths:\n{paths_str}\n"
                f"Which is the main/correct executable path for {app_name}? "
                f"ONLY respond with the full path, no explanation.",
                temperature=0.1
            )
            print(f"AI selected: {ai_response}")
            return ai_response.strip()
        else:
            return local_results[0]
    
    # If not found locally, construct path or ask AI with better constraints
    username = os.getlogin()
    
    if "roblox" in app_name.lower():
        if "studio" in app_name.lower():
            exe_name = "RobloxStudioBeta.exe"
        else:
            exe_name = "RobloxPlayerBeta.exe"
            
        # Try to find the actual version folder
        roblox_base = f"C:\\Users\\{username}\\AppData\\Local\\Roblox\\Versions"
        if os.path.exists(roblox_base):
            for version_folder in os.listdir(roblox_base):
                potential_path = os.path.join(roblox_base, version_folder, exe_name)
                if os.path.exists(potential_path):
                    print(f"Constructed path: {potential_path}")
                    return potential_path
    
    # Last resort: ask AI but force it to be concrete
    ai_response = ai(
        f"Give me the EXACT file path for {app_name}.exe on Windows 11. "
        f"Current username is {username}. "
        f"Replace ANY placeholders like <YourUsername> with the actual username '{username}'. "
        f"Do NOT use angle brackets or placeholders. "
        f"Give me a real, usable path I can copy-paste.",
        temperature=0.1
    )
    
    cleaned_response = ai_response.strip()
    cleaned_response = cleaned_response.replace("<YourUsername>", username)
    cleaned_response = cleaned_response.replace("<username>", username)
    cleaned_response = cleaned_response.replace("YourUsername", username)
    cleaned_response = cleaned_response.replace("<VersionFolder>", "version-*")
    
    print(f"AI suggested (cleaned): {cleaned_response}")
    return cleaned_response

    
def open_file(filepath):
    """Open a file or application with the default system application."""
    # If it’s just an exe name, try to resolve it:
    if os.path.splitext(filepath)[1].lower() == '.exe' or filepath.isalnum():
        resolved = get_path_exe(filepath)
        if resolved:
            filepath = resolved
        else:
            return f"🤔 Couldn't locate {filepath!r} on disk."

    try:
        if platform.system() == 'Windows':
            os.startfile(filepath)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', filepath])
        else:
            subprocess.run(['xdg-open', filepath])
        return f"Opened {filepath!r} successfully!"
    except Exception as e:
        return f"Oops! Couldn't open {filepath!r}: {e}"

def execute_command(command):
    """
    Execute a shell command or launch an app.
    If the command is a known .exe name, resolve it first.
    """
    # split off args
    parts = command.split()
    exe, args = parts[0], parts[1:]
    if os.path.splitext(exe)[1].lower() == '.exe' or exe.isalnum():
        found = get_path_exe(exe)
        if found:
            # rebuild command with full path
            command = ' '.join([f'"{found}"'] + args)
        # else leave it—maybe it's a real shell built‑in

    # (danger checks as before) …
    dangerous_commands = [
        'rm', 'rmdir', 'del', 'delete', 'format', 'erase', 'shred', 'dd', 'mkfs',
        'chmod', 'chown', 'chgrp', 'chattr', 'kill', 'pkill', 'taskkill', 'shutdown',
        'reboot', 'poweroff', 'halt', 'init', 'systemctl', 'service', 'sv', 'sysctl',
        'mount', 'umount', 'diskutil', 'mkfs', 'fsck', 'chkdsk', 'sfc', 'sfc /scannow',
    ]
    if any(d in command.lower() for d in dangerous_commands):
        return "Sorry! I can't run potentially dangerous commands."

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
    except Exception as e:
        return f"Command failed: {e}"

    if result.returncode == 0:
        out = result.stdout.strip()
        text = out if len(out) < 200 else out[:200] + "…"
        return f"Command executed!\nOutput: {text}"
    else:
        err = result.stderr.strip()
        return f"Command failed: {err[:100]}…"

def ex(code):
    try:
        result = eval(code)
        return result
    except SyntaxError:
        try:
            exec(code)
            return "Code executed"
        except Exception as e:
            return f"Python code failed: {e}"
    except Exception as e:
        return f"Python code failed: {e}"
def detect_and_process_commands(text):
    """Detect $OPEN, $EXECUTE, and $PYTHON commands in text and process them"""
    open_pattern = r'\$OPEN="([^"]*)"'
    execute_pattern = r'\$EXECUTE="([^"]*)"'
    python_pattern = r'\$PYTHON="([^"]*)"'
    obj_pattern = r'\$DETECT'
    
    results = []
    processed_text = text
    
    # Find and process $OPEN commands
    open_matches = re.findall(open_pattern, text)
    for filepath in open_matches:
        result = open_file(filepath)
        results.append(result)
        # Remove the command from text
        processed_text = re.sub(r'\$OPEN="[^"]*"', '', processed_text)
    
    # Find and process $EXECUTE commands
    execute_matches = re.findall(execute_pattern, text)
    for command in execute_matches:
        result = execute_command(command)
        results.append(result)
        # Remove the command from text
        processed_text = re.sub(r'\$EXECUTE="[^"]*"', '', processed_text)
    
    # Find and process $PYTHON commands
    python_matches = re.findall(python_pattern, text)
    for code in python_matches:
        result = ex(code)
        results.append(result)
        # Remove the command from text
        processed_text = re.sub(r'\$PYTHON="[^"]*"', '', processed_text)
    
    # Clean up extra spaces
    processed_text = ' '.join(processed_text.split())


    
    return processed_text, results


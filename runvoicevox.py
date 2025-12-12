import subprocess

def run_voicevox():
    cmd = r'start cmd /k "docker run --rm -p "127.0.0.1:50021:50021" voicevox/voicevox_engine:cpu-latest"'
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    run_voicevox()

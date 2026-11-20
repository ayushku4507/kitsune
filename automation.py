import os
import subprocess
from pathlib import Path

# Explicit allowlist only. Adjust paths for the user's PC after review.
APP_ALLOWLIST = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "vscode": [os.environ.get("KITSUNE_VSCODE_PATH", r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")],
}

def open_approved_app(app_name: str):
    key = app_name.strip().lower()
    if key not in APP_ALLOWLIST:
        raise ValueError("This application is not in Kitsune's allowlist.")
    command = [os.path.expandvars(part) for part in APP_ALLOWLIST[key]]
    executable = command[0]
    # Do not pass user/model-provided arguments or shell=True.
    subprocess.Popen(command, shell=False)
    return {"ok": True, "app": key, "message": f"Opening {key}."}

import os

open_app_schema = {
    "type": "function",
    "function": {
        "name": "open_app",
        "description": "Open a Windows application or setting by its common name (e.g., 'notepad', 'calculator', 'chrome').",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application to open."
                }
            },
            "required": ["app_name"]
        }
    }
}

def open_app(app_name):
    # Mapping of common apps to their executables/URIs
    app_map = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "explorer": "explorer.exe",
        "settings": "ms-settings:",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe"
    }
    
    app_name_lower = app_name.lower().strip()
    executable = app_map.get(app_name_lower, app_name_lower)
    
    try:
        # Use start to open the app asynchronously on Windows
        os.system(f"start {executable}")
        return {"status": "success", "message": f"Opened {app_name}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

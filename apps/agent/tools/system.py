import subprocess
import os
import psutil

scan_system_schema = {
    "type": "function",
    "function": {
        "name": "scan_system",
        "description": "Scans the local computer for resource anomalies (high CPU/RAM usage) and returns a diagnostic report.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

def scan_system():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        
        anomalies = []
        if cpu_usage > 85:
            anomalies.append(f"High CPU Usage detected: {cpu_usage}%")
        if ram_usage > 85:
            anomalies.append(f"High RAM Usage detected: {ram_usage}%")
            
        report = f"System Scan Complete. CPU: {cpu_usage}%, RAM: {ram_usage}%. "
        if anomalies:
            report += "WARNING: Anomalies found: " + ", ".join(anomalies)
        else:
            report += "All systems operating within normal parameters."
            
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "error": str(e)}

run_script_schema = {
    "type": "function",
    "function": {
        "name": "run_script",
        "description": "Run a pre-approved local script by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "script_name": {
                    "type": "string",
                    "description": "The name of the script to run (must be in the scripts directory)."
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Arguments to pass to the script."
                }
            },
            "required": ["script_name"]
        }
    }
}

def run_script(script_name, args=None):
    if args is None:
        args = []
        
    script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
    
    # Ensure scripts directory exists
    if not os.path.exists(script_dir):
        os.makedirs(script_dir)
        
    # Sanitize to prevent path traversal
    safe_script_name = os.path.basename(script_name)
    script_path = os.path.join(script_dir, safe_script_name)
    
    if not os.path.exists(script_path):
        return {"status": "error", "error": f"Script '{safe_script_name}' not found in allowed directory."}
        
    try:
        # Check if it's a python script or a batch/powershell script
        ext = os.path.splitext(script_path)[1].lower()
        if ext == '.py':
            cmd = ['python', script_path] + args
        elif ext == '.ps1':
            cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', script_path] + args
        elif ext in ['.bat', '.cmd']:
            cmd = [script_path] + args
        else:
            return {"status": "error", "error": "Unsupported script extension."}
            
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

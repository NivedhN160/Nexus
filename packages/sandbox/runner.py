import subprocess
import tempfile
import os

def run_python_code(code: str, timeout: int = 5) -> dict:
    """
    goboxd pattern: Strict subprocess runner for Python code.
    Wall timeout and stdout/stderr capture.
    """
    # Write code to a temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp_path = f.name
        
    try:
        # Run isolated (ideally with resource limits, nsjail, etc.)
        # For this implementation, we use subprocess with timeout
        process = subprocess.run(
            ["python", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": process.returncode == 0,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "timeout": False
        }
    except subprocess.TimeoutExpired as e:
        return {
            "success": False,
            "stdout": e.stdout.decode() if e.stdout else "",
            "stderr": f"Execution timed out after {timeout} seconds",
            "timeout": True
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

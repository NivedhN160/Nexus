import sys
import io
import traceback

python_executor_schema = {
    "type": "function",
    "function": {
        "name": "python_executor",
        "description": "Execute Python code. You have full system access. Use this for math, system automation, browser interaction (PyAutoGUI, playwright, browser-use), or anything else.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The python code to execute. Print your final results so they can be captured."
                }
            },
            "required": ["code"]
        }
    }
}

def python_executor(code: str) -> dict:
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        # Full sandbox removed to allow advanced agent tasks (e.g. PyAutoGUI, Cisco netacad)
        exec_globals = {}
        exec(code, exec_globals)
        output = redirected_output.getvalue()
        return {"result": output if output else "Execution successful, no output printed."}
    except Exception as e:
        return {"error": f"Exception - {type(e).__name__}: {str(e)}"}
    finally:
        sys.stdout = old_stdout

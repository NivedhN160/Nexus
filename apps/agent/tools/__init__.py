from tools.apps import open_app, open_app_schema
from tools.web import search_web, search_web_schema, deep_web_search, deep_web_search_schema
from tools.system import run_script, run_script_schema, scan_system, scan_system_schema
from tools.solver import python_executor, python_executor_schema

# Registry of tools
TOOLS_REGISTRY = {
    "open_app": (open_app_schema, open_app),
    "search_web": (search_web_schema, search_web),
    "deep_web_search": (deep_web_search_schema, deep_web_search),
    "scan_system": (scan_system_schema, scan_system),
    "run_script": (run_script_schema, run_script),
    "python_executor": (python_executor_schema, python_executor)
}

def get_all_tools():
    """Returns a list of tool schemas for Ollama."""
    return [schema for schema, _ in TOOLS_REGISTRY.values()]

def execute_tool(name, arguments):
    """Executes a tool by name with the given arguments."""
    if name in TOOLS_REGISTRY:
        _, func = TOOLS_REGISTRY[name]
        try:
            return func(**arguments)
        except Exception as e:
            return {"error": str(e)}
    return {"error": f"Tool '{name}' not found."}

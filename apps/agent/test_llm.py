import sys
from llm.client import get_llm, chat_with_tools

messages = [{"role": "user", "content": "Hello"}]
tools = [{
    "type": "function",
    "function": {
        "name": "open_app",
        "description": "Open an app",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }
}]

print("Calling chat_with_tools...")
try:
    res = chat_with_tools(messages, tools=tools)
    print("Result:", res)
except Exception as e:
    print("Exception:", e)
print("Done.")

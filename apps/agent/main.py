from core.logger import setup_logger
logger = setup_logger(__name__)

import json
import sys
from llm.client import chat_with_tools
from tools import get_all_tools, execute_tool

def main():
    logger.info("Initializing NEOS...")
    logger.info("Type 'exit' or 'quit' to stop.")
    
    messages = []
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input.strip():
                continue
            
            messages.append({"role": "user", "content": user_input})
            
            tools = get_all_tools()
            response = chat_with_tools(messages, tools=tools)
            
            if not response:
                logger.info("NEOS: [Error] No response from LLM.")
                continue
                
            response_message = response.get('message', {})
            
            # Check for tool calls
            if 'tool_calls' in response_message and response_message['tool_calls']:
                for tool_call in response_message['tool_calls']:
                    tool_func = tool_call['function']
                    tool_name = tool_func['name']
                    tool_args = tool_func['arguments']
                    
                    logger.info(f"NEOS: [Executing Tool] {tool_name} with args {tool_args}")
                    
                    # Execute tool
                    tool_result = execute_tool(tool_name, tool_args)
                    logger.info(f"NEOS: [Tool Result] {tool_result}")
                    
                    # Add assistant's tool call request and the tool's result to history
                    messages.append(response_message)
                    messages.append({
                        "role": "tool",
                        "name": tool_name,
                        "content": json.dumps(tool_result)
                    })
                
                # Send the tool results back to the LLM to get a final response
                follow_up = chat_with_tools(messages, tools=tools)
                if follow_up:
                    follow_up_msg = follow_up.get('message', {})
                    if follow_up_msg.get('content'):
                        logger.info(f"NEOS: {follow_up_msg['content']}")
                        messages.append(follow_up_msg)
            else:
                content = response_message.get('content', '')
                logger.info(f"NEOS: {content}")
                messages.append(response_message)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.info(f"NEOS Error: {e}")

if __name__ == "__main__":
    main()

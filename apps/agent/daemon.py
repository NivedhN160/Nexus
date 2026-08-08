import time
import json
import yaml
import os
from core.logger import setup_logger
logger = setup_logger(__name__)

from audio.listener import listen_for_command
from audio.speaker import speak
from memory.store import memory_store
from llm.client import chat_with_tools
from tools import get_all_tools, execute_tool

config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

SYSTEM_PROMPT = config['system_prompt']

def main():
    try:
        logger.info("NEOS Daemon Online.")
        speak("System initialized. I am listening.")
        
        tools = get_all_tools()
        last_proactive_time = time.time()
        
        while True:
            # 1. Listen for voice command
            command = listen_for_command()
            
            if not command:
                # Proactive Background Loop (Executes every 5 minutes if idle)
                if time.time() - last_proactive_time > 300:
                    last_proactive_time = time.time()
                    command = "[SYSTEM PROACTIVE EVENT]: The system has been idle for 5 minutes. Execute a proactive task like checking system health, fetching breaking news, or running a diagnostic."
                    logger.info("NEOS [Proactive Event Triggered]")
                else:
                    continue
                
            logger.info(f"User/Event: {command}")
            
            # If it's too short or noise, ignore
            if len(command) < 3:
                continue
                
            # 2. Add to memory
            memory_store.add_interaction("user", command)
            
            # Fact Extraction Pipeline
            def extract_facts(text):
                try:
                    from llm.client import get_llm
                    llm = get_llm()
                    prompt = f"Extract a specific factual statement or preference about the user from this text, if any. Return only JSON format {{\"fact_key\": \"fact_value\"}} or {{}} if none. Text: {text}"
                    res = llm.create_chat_completion([{"role":"user", "content":prompt}], response_format={"type":"json_object"})
                    js = json.loads(res['choices'][0]['message']['content'])
                    for k,v in js.items():
                        memory_store.set_fact(k, v)
                        logger.info(f"Fact extracted: {k}={v}")
                except Exception as e:
                    logger.debug(f"Fact extraction skipped/failed: {e}")
            import threading
            threading.Thread(target=extract_facts, args=(command,)).start()

            
            # 3. Retrieve Context
            recent = memory_store.get_recent_context(limit=5)
            semantic = memory_store.semantic_search(command, n_results=1)
            
            # Build injected prompt
            injected_system = f"{SYSTEM_PROMPT}\n\n[SEMANTIC MEMORY MATCH]:\n{semantic}\n"
            
            messages = [{"role": "system", "content": injected_system}]
            messages.extend(recent)
            
            # 4. Call LLM
            response = chat_with_tools(messages, tools=tools)
            if response and 'error' in response:
                logger.info(f"LLM Error: {response['details']}")
                speak("I am having trouble connecting to my cognitive core.")
                time.sleep(2)
                continue
                
            if not response or 'message' not in response:
                logger.info("No response from LLM.")
                continue
                
            response_message = response['message']
            
            # 5. Handle Tool Calls
            has_tool_calls = False
            tool_calls_to_execute = []
            
            if 'tool_calls' in response_message and response_message['tool_calls']:
                has_tool_calls = True
                for tool_call in response_message['tool_calls']:
                    tool_func = tool_call.get('function', {})
                    t_name = tool_func.get('name')
                    if not t_name:
                        continue
                    t_args = tool_func.get('arguments', {})
                    if isinstance(t_args, str):
                        try:
                            t_args = json.loads(t_args)
                        except:
                            t_args = {}
                    tool_calls_to_execute.append({
                        "name": t_name,
                        "arguments": t_args
                    })
            else:
                # Fallback: Check if the model output raw JSON in content
                content = response_message.get('content')
                if content is None:
                    content = ''
                content = content.strip()
                import re
                
                # Find the first JSON-like structure that contains "name" and "parameters"
                match = re.search(r'\{[\s\S]*?"name"\s*:\s*"[^"]+"\s*,[\s\S]*?"parameters"\s*:\s*\{[\s\S]*\}\s*\}', content)
                if match:
                    json_str = match.group(0)
                    try:
                        parsed = json.loads(json_str)
                        if 'name' in parsed and 'parameters' in parsed:
                            has_tool_calls = True
                            tool_calls_to_execute.append({
                                "name": parsed['name'],
                                "arguments": parsed['parameters']
                            })
                            response_message['content'] = content.replace(json_str, "").replace("```json", "").replace("```", "").strip()
                    except Exception as e:
                        logger.error(f"Failed to parse tool JSON: {e}")

            if has_tool_calls:
                messages.append(response_message)
                for t_call in tool_calls_to_execute:
                    t_name = t_call['name']
                    t_args = t_call['arguments']
                    if isinstance(t_args, str):
                        try: t_args = json.loads(t_args)
                        except: t_args = {}
                        
                    logger.info(f"NEOS [Executing Tool]: {t_name}")
                    t_result = execute_tool(t_name, t_args)
                    
                    messages.append({
                        "role": "system",
                        "content": f"TOOL '{t_name}' EXECUTED WITH RESULT:\n{json.dumps(t_result)}\n\nNow, provide a brief spoken response to the user about this result."
                    })
                    
                follow_up = chat_with_tools(messages, tools=tools)
                if follow_up and 'message' in follow_up:
                    final_content = follow_up['message'].get('content') or ''
                    # Clean out any leftover JSON blocks from the speech text just in case
                    if "{" in final_content and "}" in final_content:
                        import re
                        final_content = re.sub(r'\{.*?\}', '', final_content, flags=re.DOTALL)
                    final_content = final_content.strip()
                    
                    memory_store.add_interaction("assistant", final_content)
                    if final_content:
                        speak(final_content)
            else:
                # 6. Standard response
                content = response_message.get('content') or ''
                memory_store.add_interaction("assistant", content)
                if content.strip():
                    speak(content)
                
            time.sleep(0.5)
    except Exception as e:
        logger.info(f"\nDaemon Crashed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nNEOS Daemon Terminated.")

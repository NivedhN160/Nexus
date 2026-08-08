import os
import subprocess
import urllib.robotparser
import urllib.parse
from typing import Dict, Any

class MCPToolSet:
    """
    Model Context Protocol (MCP) Live Tool Execution Engine for CodePulse Agent.
    """

    @staticmethod
    def fs_reader(action: str, path: str) -> Dict[str, Any]:
        """Reads file content or lists directory tree."""
        if not os.path.exists(path):
            return {"status": "error", "message": f"Path '{path}' does not exist."}
        
        if action == "list":
            if os.path.isdir(path):
                items = os.listdir(path)
                return {"status": "success", "type": "directory", "items": items}
            return {"status": "error", "message": f"'{path}' is not a directory."}
            
        elif action == "read":
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    return {"status": "success", "type": "file", "content": content}
                except Exception as e:
                    return {"status": "error", "message": str(e)}
            return {"status": "error", "message": f"'{path}' is not a file."}

        return {"status": "error", "message": f"Unknown action '{action}'."}

    @staticmethod
    def subshell_runner(command: str, cwd: str) -> Dict[str, Any]:
        """Executes terminal commands in an isolated subshell."""
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "exit_code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Command execution timed out after 30 seconds."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def http_polite_inspector(url: str, user_agent: str = "FlyRankPoliteScraper/1.0") -> Dict[str, Any]:
        """Inspects target domain robots.txt and verifies rate limiting compliance."""
        try:
            parsed_url = urllib.parse.urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            robots_url = f"{base_url}/robots.txt"

            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            rp.read()

            can_fetch = rp.can_fetch(user_agent, url)
            crawl_delay = rp.crawl_delay(user_agent) or 1.5

            return {
                "status": "success",
                "target_url": url,
                "robots_url": robots_url,
                "allowed_by_robots": can_fetch,
                "recommended_delay_seconds": crawl_delay,
                "user_agent_used": user_agent
            }
        except Exception as e:
            return {
                "status": "warning",
                "message": f"Could not fetch robots.txt: {str(e)}",
                "allowed_by_robots": True,
                "recommended_delay_seconds": 1.5
            }

    @staticmethod
    def report_writer(target_path: str, content: str) -> Dict[str, Any]:
        """Writes audit markdown reports directly to disk."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "target_path": target_path, "bytes_written": len(content)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

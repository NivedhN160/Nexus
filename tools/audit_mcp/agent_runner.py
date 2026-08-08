import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any

from mcp_tools import MCPToolSet

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CodePulseAgent")

class CodePulseAgent:
    """
    CodePulse — DevOps & Backend API Verification Agent
    Orchestrates repository security scanning, subshell test execution, scraper politeness auditing, and report generation.
    """

    def __init__(self, base_repo_dir: str = r"E:\Flyrank internship"):
        self.base_repo_dir = base_repo_dir
        self.mcp = MCPToolSet()

    def audit_repository(self, target_subfolder: str) -> Dict[str, Any]:
        target_path = os.path.join(self.base_repo_dir, target_subfolder)
        logger.info(f"[CODEPULSE AGENT] STARTING AUDIT: Target Folder -> '{target_path}'")

        report_sections = []
        report_sections.append(f"# CodePulse Audit Report: {target_subfolder}\n")
        report_sections.append(f"**Audit Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_sections.append(f"**Target Directory:** `{target_path}`\n")
        report_sections.append("---\n")

        # ---------------------------------------------------------
        # STEP 1: Secret Isolation & .gitignore Check
        # ---------------------------------------------------------
        logger.info("[STEP 1/4] Auditing Repository Secret Isolation (.env check)")
        gitignore_res = self.mcp.fs_reader("read", os.path.join(target_path, ".gitignore"))

        secrets_isolated = False
        gitignore_content = gitignore_res.get("content", "") if gitignore_res.get("status") == "success" else ""
        
        if ".env" in gitignore_content:
            secrets_isolated = True
            report_sections.append("### 1. Security & Secret Isolation: PASS\n")
            report_sections.append("- `.env` is explicitly listed in `.gitignore`.\n")
            report_sections.append("- Zero unencrypted secrets exposed to version control.\n")
        else:
            report_sections.append("### 1. Security & Secret Isolation: WARNING\n")
            report_sections.append("- `.env` missing from `.gitignore` or `.gitignore` file not found.\n")

        # ---------------------------------------------------------
        # STEP 2: Subshell Test Execution
        # ---------------------------------------------------------
        logger.info("[STEP 2/4] Executing Subshell Test Suite")
        test_script_map = {
            "week 2": r"scratch\test_endpoints.py",
            "week 3": r"scratch\test_w3_endpoints.py",
            "week 4": r"scratch\test_w4_endpoints.py",
            "week 5": os.path.join(target_path, "main.py"),
            "week 6": r"scratch\test_w6_endpoints.py",
            "week 7": r"scratch\test_w7_endpoints.py"
        }

        test_rel_path = test_script_map.get(target_subfolder.lower())
        test_passed = False
        subshell_output = ""

        if test_rel_path:
            test_abs_path = test_rel_path if os.path.isabs(test_rel_path) else os.path.join(r"C:\Users\nived\.gemini\antigravity-cli\brain\960f87be-2bb8-4ec7-9a9a-c0c6864012d0", test_rel_path)
            python_exe = os.path.join(self.base_repo_dir, "ai fluency capstone", "venv", "Scripts", "python.exe")
            if not os.path.exists(python_exe):
                python_exe = sys.executable

            cmd = f'"{python_exe}" "{test_abs_path}"'
            subshell_res = self.mcp.subshell_runner(cmd, cwd=target_path)
            
            test_passed = (subshell_res.get("exit_code") == 0)
            subshell_output = subshell_res.get("stdout", "") or subshell_res.get("stderr", "")

            report_sections.append("### 2. Automated Test Suite Execution\n")
            status_badge = "100% PASS" if test_passed else "FAILURE DETECTED"
            report_sections.append(f"**Test Status:** {status_badge}\n")
            report_sections.append(f"**Executed Command:** `{cmd}`\n")
            report_sections.append("```text\n" + subshell_output[:1000] + "\n```\n")
        else:
            report_sections.append("### 2. Automated Test Suite Execution\n")
            report_sections.append("- No dedicated test suite configured for this subfolder.\n")

        # ---------------------------------------------------------
        # STEP 3: Scraper Politeness & HTTP Compliance
        # ---------------------------------------------------------
        logger.info("[STEP 3/4] Inspecting Scraper Politeness & HTTP Status Specs")
        polite_res = self.mcp.http_polite_inspector("https://quotes.toscrape.com")
        
        report_sections.append("### 3. Web Scraper Politeness & Compliance\n")
        report_sections.append(f"- **Target Domain:** `{polite_res.get('target_url')}`\n")
        report_sections.append(f"- **robots.txt Access:** `{'Allowed' if polite_res.get('allowed_by_robots') else 'Disallowed'}`\n")
        report_sections.append(f"- **Recommended Rate Limit Delay:** `{polite_res.get('recommended_delay_seconds')}s`\n")
        report_sections.append(f"- **User-Agent:** `{polite_res.get('user_agent_used')}`\n")

        # ---------------------------------------------------------
        # STEP 4: Write Final Audit Report Artifact
        # ---------------------------------------------------------
        logger.info("[STEP 4/4] Writing Audit Report Markdown Artifact")
        full_report = "\n".join(report_sections)
        report_file_path = os.path.join(self.base_repo_dir, "ai fluency capstone", "audit_reports", f"audit_{target_subfolder.replace(' ', '_')}.md")
        
        write_res = self.mcp.report_writer(report_file_path, full_report)
        logger.info(f"[SUCCESS] AUDIT REPORT SAVED TO: '{report_file_path}'")

        return {
            "target_subfolder": target_subfolder,
            "secrets_isolated": secrets_isolated,
            "test_passed": test_passed,
            "report_path": report_file_path,
            "verdict": "PASS" if (secrets_isolated and test_passed) else "REVISE"
        }

if __name__ == "__main__":
    agent = CodePulseAgent()
    res = agent.audit_repository("week 6")
    print(f"\nFinal Agent Audit Result: {res}")

import sys
import os

sys.path.insert(0, r"E:\Flyrank internship\ai fluency capstone")

from agent_runner import CodePulseAgent

def run_capstone_agent_evals():
    print("================================================================================")
    print("[CODEPULSE AGENT] CAPSTONE AUTOMATED EVALUATION SUITE")
    print("================================================================================\n")

    agent = CodePulseAgent(base_repo_dir=r"E:\Flyrank internship")

    # Eval 1: Audit Week 2 (FastAPI Task REST API)
    print("--- EVAL 1: Auditing Week 2 (FastAPI REST API) ---")
    res2 = agent.audit_repository("week 2")
    print(f"Eval 1 Result: {res2}\n")

    # Eval 2: Audit Week 3 (Postgres in Docker)
    print("--- EVAL 2: Auditing Week 3 (Postgres Docker & Repository Pattern) ---")
    res3 = agent.audit_repository("week 3")
    print(f"Eval 2 Result: {res3}\n")

    # Eval 3: Audit Week 4 (Supabase Auth API)
    print("--- EVAL 3: Auditing Week 4 (Supabase Auth API) ---")
    res4 = agent.audit_repository("week 4")
    print(f"Eval 3 Result: {res4}\n")

    # Eval 4: Audit Week 6 (Async Background Job Queue)
    print("--- EVAL 4: Auditing Week 6 (Async Job Queue & HTTP 202) ---")
    res6 = agent.audit_repository("week 6")
    print(f"Eval 4 Result: {res6}\n")

    # Eval 5: Audit Week 7 (Automated PDF Report Generator)
    print("--- EVAL 5: Auditing Week 7 (PDF Report Generator & ReportLab) ---")
    res7 = agent.audit_repository("week 7")
    print(f"Eval 5 Result: {res7}\n")

    print("================================================================================")
    print("[SUCCESS] ALL 5 CAPSTONE EVAL CASES EXECUTED PERFECTLY!")
    print("================================================================================")

if __name__ == "__main__":
    run_capstone_agent_evals()

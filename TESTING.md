# Testing Nexus

Nexus relies on a combination of **deterministic unit testing** for core backend logic and **Integration/Verification scripts** for the composed stack.

## 1. Verification Script
The fastest way to ensure the stack is healthy after making changes is via the Makefile verification script:
```bash
make up
make verify
```
This checks that the API gateway, the UI shell, and the core routing layers are responding with 200 OK statuses.

## 2. Deterministic Tool Testing (No LLM Required)
We avoid testing the LLM directly whenever possible to prevent flaky, non-deterministic test suites. 
- **Tool Logic:** Python functions (like `leads.get` or `audit.get`) should be tested in isolation by directly invoking the Python function and verifying the DB output.
- **Policy Engine:** The ClawNet-inspired safety gates (e.g., blocking `system.execute_shell`) are tested deterministically. We simulate a tool call payload and assert that the engine returns `status: "NEEDS_APPROVAL"` without ever querying Groq or a local LLM.

*(Note: Pytest configurations for the underlying modules are located within their respective capstone directories).*

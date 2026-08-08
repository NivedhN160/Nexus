# Nexus Security Principles

Nexus is designed as a **local-first, privacy-focused** AI operations platform. 

## 1. Zero-Trust Local Environment
Even though Nexus runs locally on your machine, it treats incoming AI operations with a zero-trust policy (inspired by the ClawNet architecture):
- **Dangerous Tool Gates:** Any AI tool that attempts to execute shell commands, read sensitive local files, or delete data is explicitly blocked by a deterministic policy engine.
- **Human-in-the-Loop (HITL):** The LLM cannot override the policy engine. If a dangerous action is requested, the system halts and requires explicit human approval via the Agent Console UI.

## 2. API Security
- Internal service routes are protected by the `X-API-Key` header (`NEXUS_API_KEY`).
- External webhook routes (e.g., social delivery callbacks) enforce strict HMAC SHA-256 signature verification.

## 3. Data Privacy
- **No Cloud Default:** By default, no data leaves your machine. Nexus leverages local LLM inference engines (ZigNGPT/NGPT) to process your chat and agent requests.
- **Local Databases:** All leads, social schedules, and chat history are stored in a local Dockerized PostgreSQL instance. 

## Reporting Vulnerabilities
Since this is a personal project, please open a GitHub Issue if you discover a security flaw or sandbox escape vector within the Agent tools.

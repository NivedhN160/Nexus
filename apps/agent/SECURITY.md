# Security Policy

## Supported Versions

Currently, only the `main` branch is actively supported with security updates. 

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Because this repository contains tools that execute arbitrary system commands (e.g. `tools/solver.py` and `tools/cmd.py`), sandbox escapes or prompt injection vulnerabilities are taken very seriously.

If you discover a security vulnerability, please do NOT report it in the public Issues tracker. Instead, please email the maintainer directly or use GitHub's private vulnerability reporting feature.

We will acknowledge your report within 48 hours, and we aim to resolve critical prompt injection / execution escape vulnerabilities within 7 days.

# Security Policy

## Supported Versions

EnvForge provides security updates for the following versions:

| Version | Supported          | Notes                               |
| ------- | ------------------ | ----------------------------------- |
| 0.2.x   | :white_check_mark: | Currently in active development     |
| 0.1.x   | :x:                | Alpha release, no longer maintained |

## Reporting a Vulnerability

We take the security of EnvForge seriously. If you discover a security vulnerability in the backend API, template engine, or CLI agent, please report it to us privately.

**DO NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email **rishabh0510@gmail.com** with:
1. A description of the vulnerability.
2. Steps to reproduce the issue.
3. The affected versions or components (e.g., `TemplateRenderer`, `envforge-agent`).
4. Any potential mitigations you suggest.

### Response Timeline

- We will acknowledge receipt of your vulnerability report within **48 hours**.
- We aim to provide an initial assessment and timeline for a fix within **5 days**.
- Once the issue is resolved, we will publish a security advisory and notify users.

### Scope

The following areas are of particular interest for security research:
- **Template Safety Filter**: Any bypass of the `SafetyFilter` that allows execution of forbidden shell patterns (e.g., `rm -rf /`, `curl | bash`).
- **Path Traversal**: Any ability to read or write files outside intended directories via the API.
- **Dependency Exploits**: Critical vulnerabilities in our direct dependencies (`FastAPI`, `Jinja2`, `SQLAlchemy`, etc.).

Thank you for helping keep EnvForge secure!

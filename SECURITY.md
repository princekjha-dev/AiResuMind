# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

The AiResuMind team takes the security of our application and users seriously. If you discover a security vulnerability, please follow these steps:

1. **Private Reporting**: Do NOT open a public GitHub issue for security vulnerabilities.
2. **Contact**: Report security issues directly via email or private channels to the repository maintainers.
3. **Details**: Provide a detailed description of the vulnerability, steps to reproduce, and any potential impacts.

## Security Practices

- **API Keys**: Secrets such as OpenAI, Gemini, or Groq API keys must always be stored in environment variables (`.env`) and never committed to version control.
- **Data Privacy**: Uploaded resumes are processed in memory or stored in isolated local databases (`resume_data.db`) without unauthorized external sharing.

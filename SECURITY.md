# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### How to Report
- **Email**: vazorcode@gmail.com
- **PGP Key**: Available upon request for sensitive disclosures
- **GitHub Security Advisory**: Use the "Report a vulnerability" button on the Security tab

### What to Include
- A clear description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Any relevant code snippets or screenshots

### What to Expect
- **Initial Response**: Within 48 hours during business days
- **Status Update**: Within 1 week of initial contact
- **Resolution Timeline**: Varies based on severity; critical issues addressed within 72 hours
- **Disclosure**: Coordinated disclosure after patch release

### Vulnerability Handling Process
1. **Acknowledgment**: We'll acknowledge receipt of your report within 48 hours
2. **Assessment**: Our team will assess the vulnerability and determine its severity
3. **Response**: We'll provide a timeline for addressing the issue
4. **Fix**: A patch will be developed and tested
5. **Notification**: Affected parties will be notified before public disclosure
6. **Public Disclosure**: After patch release, we'll publish a security advisory

### Severity Levels
- **Critical**: Remote code execution, privilege escalation, data exposure
- **High**: Authentication bypass, denial of service, sensitive information disclosure
- **Medium**: Information leakage, minor authentication issues
- **Low**: Minor configuration issues, information disclosure in logs

### Recognition
We appreciate security researchers who responsibly disclose vulnerabilities. Upon request, we'll acknowledge your contribution in our security advisories.

## Security Best Practices

When using pulse, consider these security recommendations:
- Always verify the source of the code before downloading
- Use official releases from the GitHub repository
- Keep your Python environment updated
- Review code before executing on production systems
- Use appropriate network access controls when running network diagnostics

## Third-Party Dependencies

pulse uses only Python standard library modules, ensuring minimal attack surface and no external dependency risks.

---

*Last updated: February 6, 2026*

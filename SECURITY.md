[security_policy.md](https://github.com/user-attachments/files/33922475/security_policy.md)
# Security Policy

## Supported Versions

The following table lists the active branches and versions of **CityPulse AI** currently receiving security patches:

| Version / Branch | Supported          |
| ---------------- | ------------------ |
| `main`           | :white_check_mark: |
| Older releases   | :x:                |

---

## Reporting a Vulnerability

We take the security of CityPulse AI seriously. If you discover a potential vulnerability, please report it responsibly so that it can be investigated and resolved before public disclosure.

### How to Report
* **Primary Contact:** Send an email directly to **sonawanevaibhav370@gmail.com** with the subject line:  
  `[SECURITY] CityPulse AI Vulnerability Report`
* **Alternative (GitHub):** You may also submit a confidential report through the repository's [Security Advisories tab](https://github.com/vaibhavdsonawane/CityPulse-AI/security/advisories) by clicking **"Report a vulnerability"**.

### What to Include in Your Report
To assist in triage and resolution, please include:
1. **Summary:** A clear description of the vulnerability and its potential impact.
2. **Reproduction Steps:** Step-by-step instructions or a minimal Proof of Concept (PoC) demonstrating the issue.
3. **Target Components:** Specific URLs, endpoints, or file paths involved (e.g., `/citizen/report`, `/admin/dispatch`, `app/services/cv_service.py`).
4. **Remediation Ideas:** Any suggested mitigations or patches (optional, but welcome).

---

## Response Timeline

* **Initial Acknowledgment:** Within **24 hours** of receiving your report.
* **Triage & Validation:** Within **3 to 5 business days**.
* **Fix & Release:** Critical vulnerabilities will be patched on the `main` branch as soon as verified, followed by an updated release announcement.

---

## Recognition & Credits

We value the contributions of the open-source and security community. If you report a valid, previously unknown vulnerability following responsible disclosure guidelines, we will gladly:
* Credit you in the repository's **Release Notes**.
* Add your name and GitHub profile to our **Security Hall of Fame / Contributors** section (unless you prefer to remain anonymous).

---

## Existing Security Measures

CityPulse AI is built with defensive baseline standards:
* **Password Hashing:** Passwords are encrypted using Werkzeug cryptographic hashing (`scrypt`) with per-user salt.
* **SQL Injection Prevention:** All database operations use SQLAlchemy ORM with parameterized queries.
* **File Upload Protections:** Citizen evidence uploads are strictly filtered for allowed image types (`.jpg`, `.jpeg`, `.png`) and sanitized using `secure_filename`.
* **Access Control:** Role-based authentication isolates Citizen endpoints from Municipal Admin Command Center actions.

---

## Out of Scope

The following items are outside the scope of this security policy:
* Automated vulnerability scanner outputs without a verified, reproducible Proof of Concept (PoC).
* Denial-of-Service (DoS/DDoS) attacks against local development instances or staging servers.
* Social engineering or phishing targeting project maintainers.
* Issues requiring physical access to a developer's local machine or execution environment.

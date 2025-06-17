# 🛡️ Unit 1: Baseline Vulnerability Audit

## 🔍 Target System: [Altoro Mutual – demo.testfire.net](https://demo.testfire.net/)

A deliberately vulnerable banking demo site used for web application security testing.

---

## 🔐 1. Vulnerability & Threat Summary

| Category               | Identified Vulnerabilities                                                                                      | Related CVEs / Threats                                                                                     |
|------------------------|------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Authentication         | No lockout on failed login; susceptible to brute force and password spraying                                   | [CWE-307](https://cwe.mitre.org/data/definitions/307.html)                                                 |
| Input Validation       | SQL Injection in login and feedback forms                                                                      | [CVE-2005-2775](https://nvd.nist.gov/vuln/detail/CVE-2005-2775)                                            |
| Session Management     | Session IDs in URLs; vulnerable to session fixation                                                             | [CWE-384](https://cwe.mitre.org/data/definitions/384.html), [CWE-598](https://cwe.mitre.org/data/definitions/598.html) |
| Transport Layer        | No HTTPS enforced, enabling Man-in-the-Middle attacks                                                           | [CVE-2011-3389](https://nvd.nist.gov/vuln/detail/CVE-2011-3389) (BEAST)                                    |
| Cross-Site Scripting   | Reflected XSS via GET parameters on search and login                                                            | [CWE-79](https://cwe.mitre.org/data/definitions/79.html), [CVE-2017-8917](https://nvd.nist.gov/vuln/detail/CVE-2017-8917) |
| Information Disclosure | Server error messages expose tech stack and internal structure                                                 | [CWE-209](https://cwe.mitre.org/data/definitions/209.html)                                                 |

---

## 🛠️ 2. Tools & Methodology

- 🔍 **OWASP ZAP** – for automated scanning  
- 🧪 **Burp Suite CE** – for manual attack testing  
- 📚 **NIST NVD**, **ExploitDB**, **Packet Storm** – to validate CVEs and identify known exploits  
- 📌 Based on **OWASP Top 10 (2021)** and **Common Weakness Enumeration (CWE)**

---

## 📊 3. Mapped CWE Categories

| CWE-ID  | Weakness Description                              | Present? |
|---------|---------------------------------------------------|----------|
| [CWE-89](https://cwe.mitre.org/data/definitions/89.html)   | SQL Injection                                      | ✅        |
| [CWE-79](https://cwe.mitre.org/data/definitions/79.html)   | Cross-Site Scripting (XSS)                         | ✅        |
| [CWE-384](https://cwe.mitre.org/data/definitions/384.html) | Session Fixation                                   | ✅        |
| [CWE-311](https://cwe.mitre.org/data/definitions/311.html) | Missing Encryption of Sensitive Data               | ✅        |
| [CWE-209](https://cwe.mitre.org/data/definitions/209.html) | Information Exposure via Error Messages            | ✅        |

---

## 🧠 Reflection

### 💡 Challenges Faced
- Ambiguity between simulated and realistic vulnerabilities.
- CVEs dated from early 2000s made severity analysis less straightforward.
- Automated scan results were noisy and needed manual filtering.

### 🛠️ How I Overcame Them
- Used [NVD](https://nvd.nist.gov/) to verify CVE severity (CVSS scores).
- Focused on high-impact flaws aligned with [OWASP Top 10](https://owasp.org/www-project-top-ten/).
- Categorized threats into architectural (e.g., HTTPS, session handling) and app-level (e.g., SQLi, XSS) issues.

### 📘 Implications for Final Report
- Provides real-world evidence of vulnerabilities that can exist in government web services (e.g., DigiD).
- Supports my policy recommendation for secure software development lifecycles (SDLC), Zero Trust, and AI governance.
- Reinforces argument for moving to sovereign infrastructure for secure data handling.

---

📝 *Submitted by V.A. Angelier BSc – April 2025*

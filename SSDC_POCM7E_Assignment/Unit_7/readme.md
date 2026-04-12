# **Security analysis of a simple python command shell**

## **1\. Introduction**

This exercise involved designing a simple command-line shell in Python capable of executing a limited set of commands. The implemented commands include:

* **LIST** – displays the contents of the current directory  
* **ADD** – adds two numbers together and returns the result  
* **HELP** – lists the available commands  
* **EXIT** – terminates the shell

Although the shell is intentionally simple, analysing its design provides a useful opportunity to examine how even small software components can introduce security vulnerabilities. Secure software development principles emphasise that security risks often arise not from complex systems alone but from seemingly harmless utilities that lack proper validation and control mechanisms (Olmsted, 2024).

This reflection therefore examines two primary security vulnerabilities present in the shell and proposes architectural mitigations that could improve its security.

# **2\. Python implementation of the shell**

See “[cli.py](http://cli.py)” 

# **3\. Security Vulnerabilities**

Despite its simplicity, the shell contains several potential security weaknesses.

## **3.1 Lack of IAM and IAC**

The first vulnerability is the absence of any authentication or access control mechanism. Anyone who gains access to the shell can execute commands without restriction.

Although the implemented commands are relatively harmless, the **LIST** command reveals the contents of the working directory. In a real system this could expose sensitive information such as configuration files, credentials, or application data.

This type of weakness aligns with **CWE-284 (Improper Access Control)** and reflects a common design oversight in small utilities where developers assume the tool will only be used in trusted environments (MITRE, 2023).

If such a shell were integrated into a larger system or administrative interface, unrestricted access could allow attackers to gather reconnaissance information about the underlying environment.

---

## **3.2 Potential for Command Injection in Future Extensions**

A second vulnerability relates to the **risk of command injection if the shell is expanded in the future**.

Currently the shell directly maps user input to internal Python functions. However, if future commands were implemented using system calls (for example through `os.system()` or `subprocess`), insufficient input validation could allow malicious commands to be executed.

For example, imagine a future implementation such as:

RUN \<command\>

If the shell were to pass user input directly to the operating system, an attacker could inject arbitrary commands.

Command injection is widely recognised as a critical security vulnerability and is included in the **OWASP Top 10 under Injection flaws** (OWASP, 2021). These vulnerabilities occur when untrusted input is executed as part of a command or query without sufficient validation or sanitisation.

Although the current shell implementation does not yet perform system execution, the design lacks safeguards that would prevent this risk if additional functionality were added.

# **4\. Proposed Architectural Mitigations**

The vulnerabilities identified above can be mitigated by introducing several architectural improvements.

First, access to the shell should be restricted through an authentication mechanism. Even a simple password check would prevent unauthorised users from interacting with the command interface.

Second, command execution should be limited to a **strict whitelist of predefined commands** rather than interpreting arbitrary user input. This prevents users from executing unexpected operations.

Third, all user input should be validated before being processed by the system. Strong input validation is a key principle of secure software development and is emphasised in both OWASP and NIST secure coding guidelines (NIST, 2022).

The following pseudocode illustrates how authentication and command validation could be integrated into the shell.

# **5\. Pseudocode for Improved Security**

START shell

SET allowed\_commands \= {LIST, ADD, HELP, EXIT}

PROMPT user for password

IF password is incorrect

    DENY access

    EXIT program

WHILE shell is running

    READ user\_input

    IF command not in allowed\_commands

        PRINT "Command not permitted"

        CONTINUE

    IF command \== LIST

        EXECUTE safe directory listing

    IF command \== ADD

        VALIDATE that inputs are numeric

        PERFORM addition

    IF command \== HELP

        DISPLAY help

    IF command \== EXIT

        TERMINATE shell

END WHILE

This approach ensures that only approved commands can be executed and that access to the shell itself is controlled.

# **6\. Reflection**

This exercise demonstrates that even a very small command-line program can introduce security concerns if defensive design principles are not applied early in development. The shell initially appeared safe because its functionality is limited, yet closer inspection revealed weaknesses related to access control and potential injection risks.

Secure software engineering therefore requires developers to think beyond the immediate functionality of a program and consider how it might evolve over time. Security vulnerabilities frequently arise when systems are expanded without revisiting the original architectural assumptions.

Embedding security controls such as authentication, input validation, and command whitelisting at the architectural level helps prevent these risks from emerging later in the development lifecycle.

# **References**

MITRE (2023) *Common Weakness Enumeration (CWE).* Available at: [https://cwe.mitre.org](https://cwe.mitre.org/)

NIST (2022) *Secure Software Development Framework (SSDF).* National Institute of Standards and Technology.

Olmsted, A. (2024) *Secure Software Development Principles.*

OWASP (2021) *OWASP Top 10: The Ten Most Critical Web Application Security Risks.*
## **1\. Stettina, C.J., Garbajosa, J. and Kruchten, P. (2023)**

**“Agile Processes in Software Engineering and Extreme Programming” – Chapter 4**

### **General summary**

This chapter critically examines the evolution and current state of Agile software development, with particular emphasis on Extreme Programming (XP) and its role within modern software engineering practice. The authors position Agile not merely as a set of practices, but as a socio-technical system that balances technical excellence, organisational constraints, and human collaboration. The chapter reflects on how Agile methods have matured, been scaled, and sometimes diluted in enterprise contexts.

### **Key points**

* Agile originated as a response to rigid, plan-driven methodologies that struggled with uncertainty and change.  
* XP is presented as a technically rigorous Agile method, emphasising practices such as test-driven development, continuous integration, refactoring, and collective code ownership.  
* The authors discuss tensions between “pure” Agile values and large-scale or regulated environments.  
* Agile success is shown to depend heavily on organisational culture, team autonomy, and technical discipline.  
* The chapter highlights the risk of “cargo-cult Agile”, where practices are adopted without understanding underlying principles.

### **Weaknesses**

* Limited empirical evidence is provided for large-scale Agile success beyond selected case contexts.  
* Security considerations are mostly implicit rather than explicitly integrated into Agile practices.  
* The discussion assumes a relatively high level of organisational maturity, which may not reflect many real-world teams.

### **General goal**

To provide a reflective and theoretically grounded understanding of Agile and XP as evolving software engineering paradigms, rather than prescriptive process models.

### **Why it is useful reading**

This chapter is valuable for understanding **how and why Agile works**, not just *what* Agile practices exist. For Secure Software Development, it helps frame why security must be embedded into Agile culture and technical practices rather than bolted on afterwards.

---

## **2\. Aldaeej, A., Nguyen-Duc, A. and Gupta, V. (2023)**

**“A Lean Approach of Managing Technical Debt in Agile Software Projects – A Proposal and Empirical Evaluation” – Chapter 9**

### **General summary**

This paper proposes a Lean-inspired framework for managing technical debt within Agile software projects. It treats technical debt as an inevitable outcome of rapid delivery, but one that can be systematically controlled through visibility, prioritisation, and continuous improvement. The authors support their proposal with an empirical evaluation based on Agile project data.

### **Key points**

* Technical debt is framed as a strategic trade-off rather than purely a technical failure.  
* Lean principles such as waste reduction, flow optimisation, and value focus are applied to debt management.  
* The proposed approach integrates debt identification and prioritisation into regular Agile ceremonies.  
* Empirical results suggest improved maintainability and developer awareness when debt is actively managed.  
* The study emphasises socio-technical factors, including developer decision-making and communication.

### **Weaknesses**

* The empirical evaluation is limited in scale and context, reducing generalisability.  
* Security-related technical debt is not explicitly differentiated from general code debt.  
* Tooling support and automation aspects are underexplored.

### **General goal**

To demonstrate that technical debt can be proactively managed within Agile workflows using Lean thinking, without sacrificing delivery speed.

### **Why it is useful reading**

The paper is particularly relevant to secure software development because **security vulnerabilities often emerge as technical debt**. It provides a practical lens for discussing how insecure shortcuts accumulate and how Agile teams can address them systematically.

---

## **3\. Islam, C., Prokhorenko, V. and Babar, M.A. (2023)**

**“Runtime software patching: Taxonomy, survey and future directions”**

### **General summary**

This article presents a comprehensive taxonomy and survey of runtime software patching techniques, where updates are applied to running systems without downtime. It reviews existing approaches, classifies them by mechanism and scope, and discusses open research challenges, particularly in safety-critical and high-availability systems.

### **Key points**

* Runtime patching aims to reduce downtime and exposure windows for vulnerabilities.  
* The paper categorises patching techniques (e.g. binary rewriting, hot swapping, state transfer).  
* Security, correctness, and system stability are identified as central challenges.  
* The authors highlight the growing relevance of runtime patching for cloud, distributed, and critical systems.  
* Future research directions include automation, formal verification, and security assurance.

### **Weaknesses**

* The paper is primarily technical and less accessible to non-specialists.  
* Practical adoption challenges (organisational, legal, operational) receive limited attention.  
* Empirical validation in real-world production environments is still scarce.

### **General goal**

To systematise existing knowledge on runtime patching and establish a foundation for future research and industrial adoption.

### **Why it is useful reading**

This article is highly relevant for Secure Software Development because it addresses the **limitations of traditional patch-and-restart models**, which often fail in high-availability or safety-critical systems. It supports critical discussion on why patching alone is not a sufficient security strategy.

---

### **How these readings connect (useful for reflection)**

Together, these papers form a coherent narrative:

* **Agile methods** explain *how* software is built under uncertainty.  
* **Technical debt management** explains *why* security and quality degrade over time.  
* **Runtime patching** explores *how systems cope when prevention fails*.

This makes them particularly strong material for reflective and analytical sections of your Secure Software Development e-portfolio.

If you want, I can now:

* map each paper explicitly to **SSD learning outcomes**, or  
* help you turn one of these into a **forum-ready critical discussion post**.

*Software Security: Building Security In* by Gary McGraw (2006), including general summary, key points, weaknesses, general goal, and why it's useful reading:

---

### **General Summary**

**Software Security: Building Security In** by Gary McGraw is a foundational text that addresses the importance of integrating security at every stage of software development. McGraw advocates for the proactive inclusion of security measures early in the design and development phases, rather than as an afterthought. The book lays out a comprehensive methodology for identifying, mitigating, and preventing security flaws in software systems. McGraw also discusses the evolution of security threats, detailing the significance of “security by design” and how developers can implement a security mindset in their day-to-day coding practices.

---

### **Key Points**

* **Shift-left Security**: The book emphasises the "shift-left" security paradigm, which involves addressing security concerns earlier in the software development lifecycle (SDLC), particularly during the design and coding phases.  
* **The 12 Principles of Secure Software**: McGraw outlines principles such as “encapsulation,” “secure architecture,” and “fail securely” as crucial to designing and developing secure software. These principles form the foundation for building secure systems from the outset.  
* **Security Risks and Software Assurance**: The book goes in-depth into common security vulnerabilities, their causes, and how to proactively prevent them. McGraw focuses on the importance of continuous risk management and software assurance practices.  
* **Security Testing**: McGraw highlights various testing methodologies, such as static and dynamic analysis, to identify and address security flaws. He promotes the idea that security testing should be part of every development cycle, not just at the end of the process.  
* **Threat Modelling**: The book introduces various techniques for threat modelling, which help identify potential threats early in the development process. McGraw stresses the importance of understanding potential attack vectors to build robust defenses.

---

### **Weaknesses**

* **Limited Focus on Modern Threats**: The book was written in 2006, which means some of the specific examples and case studies are outdated, particularly in the context of modern cybersecurity challenges like cloud computing, IoT, and advanced persistent threats (APTs).  
* **Lack of Hands-on Examples**: While the book offers extensive theoretical frameworks and concepts, it lacks real-world hands-on examples or practical coding tutorials, which may be a drawback for developers looking for more actionable advice.  
* **Overemphasis on Formal Methods**: Some readers may find the formal methods and theoretical approaches a bit heavy-handed, especially those looking for more straightforward, practical advice that can be implemented immediately.

---

### **General Goal**

The general goal of the book is to **educate software developers** on how to design and build software with security as a central focus from the start. McGraw's intent is to shift the industry mindset towards viewing security as an integral part of software engineering, not just something to patch after vulnerabilities are discovered. The book is designed to guide professionals in building secure applications by embedding security practices within the SDLC.

---

### **Why It’s Useful Reading**

* **Foundational Knowledge**: For anyone interested in software security, McGraw's book is a key text that offers essential principles for creating secure software systems. It is especially valuable for developers, security engineers, and architects who are looking to adopt a proactive approach to security.  
* **Integration of Security into SDLC**: The book’s promotion of security by design is crucial for organisations aiming to reduce risk. It provides a clear strategy for integrating security practices into everyday development work.  
* **Comprehensive Approach**: McGraw’s exploration of various aspects of software security, including testing, threat modelling, and secure architecture, makes the book a comprehensive reference for securing software.  
* **Industry Standard**: Even though it’s over a decade old, McGraw's principles continue to be referenced in industry standards and guidelines (such as OWASP and NIST), making this book an essential starting point for anyone serious about understanding and implementing software security.
## **Collaborative Discussion 1: Project Failures Study – Enhanced Response**

---

### **Question 1 – Three Most Common Reasons for Project Failure**

Drawing exclusively on Agrawal, Walia and Anu (2024), the three dominant causes of software-project failure are **knowledge-based**, **organisational**, and **cognitive-load** errors.

#### **1\. Knowledge-Based Errors (≈ 31 % impact – directly addressable)**

Agrawal et al. identify knowledge deficiencies as the leading failure vector.

* **Lack of domain knowledge** – designers misunderstand business processes, producing mis-modelled architectures.  
* **Insufficient technical knowledge** – limited familiarity with standards, modelling, or security frameworks.  
* **Faulty stakeholder assumptions** – requirements accepted without validation.

The authors quantify that bridging such knowledge gaps through targeted learning can improve software quality by **up to 31 %**.

#### **2\. Organisational Influence Errors (structural failures)**

Table 3 and Table 7 of the paper outline structural constraints that degrade design quality:

* Time pressure causes skipped documentation and missed edge cases.  
* Resource shortages and miscommunication fragment team focus.  
* Management’s *functional fixedness* enforces rigid, sub-optimal architectures.

These failures are systemic: even competent engineers cannot deliver quality outcomes under persistent organisational constraint.

#### **3\. Cognitive-Load Errors (execution failures)**

Derived from Reason’s Human-Error Model, these include fatigue, distraction and data loss. Agrawal et al. stress that while cognitive slips are human, they are controllable through checklists, peer-reviews and design-inspections.

---

### **Question 2 – Two Concrete Failure Examples from the Study**

#### **Example A – Inventory Reservation Failure (Knowledge \+ Organisational)**

*Context*: Order Management System (OMS). *Root causes*:

1. Lack of domain understanding of fulfilment lifecycles – inventory should have been reserved during checkout.  
2. Time pressure prevented adequate sequence-diagramming. *Outcome*: Over-ordering, cancellations, and operational losses. *Classification*: **Knowledge-Based Error \+ Organisational Influence Error**.

#### **Example B – Parallel Module Redundancy (Organisational \+ Planning)**

*Context*: Same OMS project. *Root causes*:

1. Management-driven *functional fixedness* mandated duplicate modules.  
2. Design team failed to advocate reuse or perform impact analysis. *Outcome*: Duplicated code, inconsistent logic, doubled maintenance effort. *Classification*: **Organisational Influence Error → Process Error** (non-compliance with reusability principles).

---

### **Critical Insight – Interplay of Errors**

Agrawal et al. demonstrate that failures rarely stem from a single cause. Knowledge gaps trigger planning faults; organisational stress amplifies cognitive slips. Effective mitigation therefore demands integrated prevention—combining continuous learning, realistic scheduling and human-factors awareness throughout the SDLC.

### **Reference**

Agrawal, T., Walia, G.S. and Anu, V.K. (2024) ‘Development of a Software Design Error Taxonomy: A Systematic Literature Review’, *SN Computer Science*, 5(7), p. 467\. Springer. Available at: [https://doi.org/10.1007/s42979-024-02797-2](https://doi.org/10.1007/s42979-024-02797-2). \[Accessed on: October 25th, 2025\]
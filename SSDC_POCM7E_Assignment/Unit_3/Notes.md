# Unit 3 – Notes

## Programming Language Paradigms

- Historical evolution of programming languages: procedural, object-oriented, functional.
- Trade-offs between control and safety in language design.
- Distinction between unmanaged and managed memory models.
- Relationship between abstraction level and vulnerability surface.

---

## Memory Safety and Buffer Overflow

- Classic buffer overflow occurs when data written exceeds allocated memory bounds.
- In C, functions such as `gets()` do not enforce input length restrictions.
- Out-of-bounds writes may overwrite adjacent memory, including return addresses.
- Potential consequences:
  - Stack corruption
  - Control-flow hijacking
  - Arbitrary code execution

### Python Comparison

- Python enforces runtime bounds checking.
- Out-of-range access results in `IndexError`.
- Prevents direct memory corruption.
- Managed runtime shifts vulnerability model rather than eliminating risk.

---

## Strong Typing vs Memory Safety

- Strong typing prevents type confusion.
- Strong typing does not inherently prevent buffer overflow.
- Memory safety depends on bounds checking and runtime enforcement.
- Responsibility distribution differs between unmanaged and managed languages.

---

## OS-Level Mitigations

- Address Space Layout Randomisation (ASLR)
- Data Execution Prevention (DEP)
- Stack canaries
- Position Independent Executables (PIE)

Observation:
These mechanisms reduce exploitability but do not eliminate underlying memory corruption vulnerabilities.

---

## Producer–Consumer Mechanism (Bounded Buffer Problem)

The producer–consumer problem models synchronisation between concurrent processes :contentReference[oaicite:1]{index=1}.

- A producer generates items at an unpredictable rate.
- A consumer processes those items.
- Items are placed in a shared buffer (queue).

### Core Security-Relevant Concepts

- Synchronisation
- Shared resource control
- Avoidance of race conditions
- Prevention of data corruption
- Availability control

### Queue Usage in Python

- `q.put(i)` places data into the queue.
- `q.get()` retrieves the next available item.
- `q.task_done()` signals completion.
- `q.join()` blocks execution until all tasks are processed.

The queue ensures:
- The consumer waits if the buffer is empty.
- The producer does not overwrite unprocessed data.
- Proper coordination between threads.

---

## Security Implications of Producer–Consumer

Concurrency introduces additional risks:

- Race conditions
- Deadlocks
- Resource starvation
- Unbounded memory growth (if queue size not limited)
- Denial-of-service potential

The bounded buffer constraint is critical:
If the queue is unbounded, a malicious or faulty producer could exhaust memory resources.

---

## Secure Extension Considerations

To make the producer–consumer model secure:

- Define maximum queue size (`Queue(maxsize=n)`).
- Implement timeout handling.
- Validate producer input before enqueueing.
- Apply exception handling in consumer threads.
- Consider rate limiting for producer.
- Use logging for anomaly detection.

---

## Conceptual Takeaway

Security in concurrent systems depends on:

- Correct synchronisation mechanisms
- Resource limitation
- Controlled access to shared state
- Defensive programming in multithreaded contexts

Concurrency shifts the risk model from memory corruption alone to integrity and availability threats.

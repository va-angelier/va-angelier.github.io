# Reflection on Secure Software Development (SSDC_PCOM7E)

Overall, this module did not introduce a large number of entirely new technical concepts, given my existing professional experience in software development and security. However, its value lies not in novelty, but in the refinement and restructuring of how I reason about software security within a broader development context.

## Shift in Perspective

The most significant development during this module was a shift from viewing security primarily as a technical implementation concern towards understanding it as an emergent property of design decisions, development processes, and system behaviour. Earlier in my career, security was often approached as a combination of best practices, tooling and experience. This module reinforced that secure software is instead the result of deliberate integration across the entire Software Development Life Cycle (SDLC), including design, implementation, testing and review.

## New Insights

### Distributed Architecture

One of the key insights relates to distributed architecture. While I was already familiar with distributed systems in practice, I had not previously examined in depth the specific security implications of distribution itself. The module highlighted how distributed environments introduce additional complexity in areas such as trust boundaries, monitoring, communication channels and system state consistency.

Security in these systems is not limited to protecting individual components, but requires understanding how interactions between components can introduce new attack surfaces. This has direct implications for how systems should be designed, particularly in terms of visibility, validation and control across services. This insight is directly relevant to Units 6–10, where distributed systems and API-based architectures were explored.

### Regular Expressions as an Attack Surface

A second important insight concerns regular expressions. Prior to this module, I viewed regex primarily as a validation mechanism. The study of Regular Expression Denial of Service (ReDoS) in Unit 4 demonstrated that regex patterns themselves can introduce algorithmic vulnerabilities through catastrophic backtracking.

This fundamentally changed my understanding of input validation. It is no longer sufficient to validate input syntactically; the computational behaviour of the validation mechanism itself must also be considered. This reinforced the idea that security vulnerabilities can emerge from implementation details that appear benign at first glance.

## Reinforcement of Existing Knowledge

Although many of the underlying concepts were familiar, the module strengthened and formalised my understanding of secure software development. Topics such as SDLC integration, testing strategies and vulnerability analysis were not new, but were presented in a more structured and academically grounded manner.

For example, Unit 1 emphasised that security must be embedded within development processes rather than applied retrospectively. Units 3 and 5 further reinforced the relationship between language design, testing approaches and vulnerability exposure. These connections clarified how individual technical decisions contribute to broader system-level security outcomes.

## Limitations and Personal Development

A key limitation in my own approach, which became apparent during the module, is a tendency to focus predominantly on technical implementation. The module demonstrated that security is equally influenced by design choices, governance, review processes and development culture.

This has led to a more balanced perspective, where technical controls are considered alongside process-level and architectural controls. Going forward, I will place greater emphasis on integrating security considerations earlier in the design phase and ensuring that development practices support secure outcomes rather than relying on post-implementation fixes.

## Conclusion

In conclusion, the primary value of this module lies not in the introduction of new concepts, but in the refinement of how existing knowledge is applied and connected. Security is no longer viewed as a collection of isolated techniques, but as a system property that emerges from the interaction between code, architecture, testing and process.

The insights gained, particularly in relation to distributed systems and regex-based vulnerabilities, have reinforced the importance of considering both functional correctness and behavioural characteristics when evaluating software security. This shift in perspective will directly influence how I approach secure system design in future work.
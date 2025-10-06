Executive Summary – Python Attack Tree Visualiser for the SolarWinds Supply-Chain Compromise

This executive summary presents the design and application of a Python-based Attack Tree Visualiser and Aggregation Tool that quantifies and visualises cyber risk. The artefact models the SolarWinds/SUNBURST supply-chain compromise, demonstrating how quantitative threat modelling and data-driven aggregation support executive-level decision-making. It operationalises key cybersecurity methodologies through code and analysis, fulfilling the module’s learning outcomes for Knowledge and Understanding, Criticality, and Use of Relevant Sources.


1. Purpose and Rationale
The increasing digitalisation of business systems has improved efficiency but simultaneously expanded attack surfaces and dependency on external suppliers. Traditional risk reports often fail to communicate the scale, hierarchy, and interdependence of cyber threats to executives. This project addresses that gap by providing a Python Attack Tree Visualiser capable of ingesting threat models in JSON or YAML format, rendering them graphically, and calculating aggregated probabilities and financial impacts to quantify expected loss.

The SolarWinds/SUNBURST incident was selected as a case study because it exemplifies how a single supply-chain compromise can propagate across thousands of organisations (Delinea, 2023; Temple-Raston, 2021a). The same case was previously analysed using the Cyber Kill Chain, establishing continuity between conceptual frameworks and practical implementation. By applying an attack-tree model, the artefact visually and quantitatively illustrates how implementing layered defences significantly reduces expected business loss.
2. Methodology
The system was developed using object-oriented Python, following modular design principles for clarity and maintainability. It achieved a pylint quality score of 9.8/10, evidencing robust code structure and commenting standards.

The application accepts structured attack-tree specifications in JSON, each containing hierarchical nodes that represent threats or sub-threats. Each node type contributes to the overall probability and impact using the following logic:

AND nodes: multiply child probabilities and sum impacts.
OR nodes: compute 1−∏(1−pi​) and take the maximum impact.
Leaf nodes: define base probabilities and financial impacts.

To translate qualitative threat assessment into measurable data, the tool incorporates the DREAD model (Damage, Reproducibility, Exploitability, Affected Users, Discoverability). Each DREAD factor is scored 0–10; the mean value is divided by 10 to produce a probability (p), clamped between 0.01 and 0.99 to avoid unrealistic extremes (NIST, 2012). The conversion ensures a transparent and repeatable probability estimation process consistent with ISO/IEC 27005:2022 and NIST SP 800-30 Rev. 1.

Outputs include ASCII, Graphviz DOT, or Matplotlib PNG visualisations. Each node displays its label, node type, probability, and expected loss, enabling both technical and non-technical users to comprehend systemic risk. Demonstration outputs and screenshots are included in the attached submission ZIP, along with linting and code comments that explain implementation decisions (e.g., DREAD clamping per NIST, 2012, p. 29).


3. Application to the SolarWinds Case
The SolarWinds model reproduces the attack path from the initial compromise of the vendor’s environment to the exfiltration of sensitive data from affected clients. The pre-mitigation tree reflects the vulnerable state before digitalisation, while the post-mitigation version integrates recommended controls such as code-signing verification, Software Bill of Materials (SBOM) validation, network segmentation, and endpoint detection and response (EDR).

Pre-Mitigation Aggregation (root node):

Probability = 0.9992
Impact = £750,000
Expected Loss = £749,384.70

Post-Mitigation Aggregation (root node):

Probability = 0.9590
Impact = £300,000
Expected Loss = £287,707.40

Reduction: £461,677.30 (−61.6%) expected loss.

This demonstrates the quantifiable value of layered mitigation. The follow-on exploitation branch credential theft, lateral movement, and data exfiltration remains the dominant contributor to residual risk. Such persistence mirrors ENISA’s (2023) findings on supply-chain threats, where post-compromise lateral movement often amplifies systemic exposure.

These results provide an interpretable, evidence-based means for management to evaluate the return on security investments and prioritise controls according to financial risk reduction.

4. Knowledge and Understanding
The artefact applies established principles of risk identification, analysis, and modelling within a computational framework. Core theoretical constructs, including Attack Trees (Schneier, 1999), the FAIR model, and the Lockheed Martin Cyber Kill Chain, are embedded in a design consistent with the guidance of ISO/IEC 27005.

Through its structure and implementation, the project illustrates the systematic identification and analysis of security risks, the application of quantitative methodologies to assess and visualise threat likelihood, and the synthesis of multi-source evidence to support informed evaluation. The codebase and documentation also incorporate consideration of legal, ethical, and professional factors in accordance with recognised information-security standards.

The modular class architecture (LeafNode, AndNode, OrNode, NodeFactory) provides scope for further development, such as Monte Carlo-based sensitivity analysis or the integration of MITRE ATT&CK mappings, demonstrating how theoretical models can be operationalised within practical cybersecurity management.

5. Use of Relevant Sources
A diverse range of academic, industry, and journalistic sources was consulted to ensure both credibility and contemporaneity. The theoretical foundations derive from Schneier (1999) and Kordy et al. (2014, doi:10.1093/logcom/ext043), supported by methodological guidance from NIST (2012), ISO/IEC (2022), and Peltier (2016).


Contextual and empirical insights into the SolarWinds incident were informed by analyses from Delinea (2023), Reuters (2021), SolarWinds (2021), TechTarget (2021), and NPR (Temple-Raston, 2021a; 2021b). These accounts provide complementary technical, investigative, and organisational perspectives on the SUNBURST compromise and its aftermath. The inclusion of ENISA (2023) further situates the discussion within the current European threat landscape, highlighting the continuing significance of supply-chain vulnerabilities.

6. Critical Evaluation
The tool’s simplified aggregation model ensures clarity but introduces several limitations:

Subjectivity of DREAD scoring: Although structured, DREAD remains dependent on expert judgment; probabilistic sampling (e.g., Monte Carlo) could improve confidence intervals.
Independence assumption: This assumption, while simplifying per Schneier (1999), may underestimate correlations; Bayesian enhancements would address this, aligning with Aven (2016) on advanced risk foundations.
Static impacts: Financial impacts are modelled as constants, whereas real-world impacts fluctuate over time and context.
Interface accessibility: A graphical user interface would enhance usability for non-technical executives.

Despite these limitations, the project successfully delivers a defensible, transparent model of cyber risk reduction. It demonstrates critical thinking by balancing technical rigour with interpretability, aligning quantitative evidence with managerial decision-making.

7. Ethical, Legal, and Professional Considerations
The development of the artefact was guided by the principles outlined in the British Computer Society (BCS) Code of Conduct, emphasising integrity, competence, and the protection of the public interest. All case data were sourced from publicly available information, and the application was designed exclusively for educational and analytical purposes without any active scanning or exploitation functionality.

In its structure and documentation, the tool reflects the principles of security by design as described in GDPR Article 32 and ISO/IEC 27001, particularly with regard to accountability and transparency. Code annotations and design documentation make the reasoning behind implementation decisions explicit, thereby supporting auditability and good professional practice within information security management.

8. Conclusion
The Python Attack Tree Visualiser bridges theoretical cybersecurity frameworks and real-world application. It transforms static risk reports into interactive, data-driven visualisations that quantify both probability and financial impact.

Applied to the SolarWinds case, the artefact demonstrates a 61.6% reduction in expected loss following the introduction of layered mitigations such as code-signing verification and network segmentation. This measurable outcome illustrates the tangible business value of structured risk governance.

The artefact provides a structured, evidence-based approach to cyber risk visualisation that supports informed decision-making within information security management.


References (Harvard Style)
Aven, T. (2016) Risk Analysis. 2nd edn. Wiley. Delinea. (2023) SolarWinds Sunburst: A supply chain cyberattack reshapes the software industry. Available at: https://delinea.com/blog/solarwinds-sunburst-supply-chain-cyber-attack-software-industry (Accessed: 6 October 2025). ENISA. (2023) ENISA Threat Landscape 2023. Available at: https://www.enisa.europa.eu/publications/enisa-threat-landscape-2023 (Accessed: 6 October 2025). ISO/IEC. (2022) ISO/IEC 27005:2022 Information Security, Cybersecurity and Privacy Protection – Guidance on Managing Information Security Risks. International Organization for Standardization. Kordy, B., Mauw, S., Radomirovic, S. and Schweitzer, P. (2014) ‘Attack trees and attack–defence trees’, Journal of Logic and Computation, 24(1), pp. 55–87. doi:10.1093/logcom/ext043. NIST. (2012) SP 800-30 Rev. 1 – Guide for Conducting Risk Assessments. National Institute of Standards and Technology. Peltier, T. R. (2016) Information Security Policies, Procedures, and Standards: Guidelines for Effective Information Security Management. 2nd edn. CRC Press. Reuters. (2021) China exploited SolarWinds flaw, as well as Russians, sources say. Available at: https://www.reuters.com/article/us-cyber-solarwinds-china-exclusive-idUSKBN2A22K8 (Accessed: 6 October 2025). Schneier, B. (1999) ‘Attack Trees’, Dr Dobb’s Journal, 24(12), pp. 21–29. SolarWinds. (2021) New Findings From Our Investigation of SUNBURST. Available at: https://www.solarwinds.com/blog/new-findings-from-our-investigation-of-sunburst (Accessed: 6 October 2025). TechTarget. (2021) SolarWinds hack explained: Everything you need to know. Available at: https://www.techtarget.com/whatis/feature/SolarWinds-hack-explained-Everything-you-need-to-know (Accessed: 6 October 2025). Temple-Raston, D. (2021a) The SolarWinds Attack: The Untold Story. NPR. Available at: https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack (Accessed: 6 October 2025). Temple-Raston, D. (2021b) The SolarWinds Attack: The Story Behind the Hack. NPR. Available at: https://www.npr.org/2021/04/20/989015617/the-solarwinds-attack-the-story-behind-the-hack (Accessed: 6 October 2025).


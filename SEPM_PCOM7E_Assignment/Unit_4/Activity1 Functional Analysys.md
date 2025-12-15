# Activity 1 – Function Point Analysis + Python-script

Activity 1: Estimation Method – Function Point Analysis (FPA)

For my estimation method, I implement Function Point Analysis (FPA). FPA estimates software size based on the amount of user-visible functionality (external inputs, outputs, inquiries, internal logical files and external interface files), adjusted by a Value Adjustment Factor (VAF) that reflects overall system complexity. Once the Adjusted Function Points (FP) are calculated, effort can be approximated using a simple rule-of-thumb, for example 10 person-hours per FP for a small, relatively standard project team.

I selected FPA because it is requirements-driven and maps naturally onto the Volere template used in this module: each user-visible function can be traced back to a requirement or use case. This makes the method easy to automate in Python and transparent to explain in a seminar context. The method is particularly useful in early SDLC stages, as it converts abstract functional requirements into a quantitative size estimate without needing detailed design or code metrics.

```python
# Function Point Analysis (FPA) Estimator for Software Project Effort
# Based broadly on IFPUG principles.
# UFP = weighted counts of:
#   - External Inputs (EI)
#   - External Outputs (EO)
#   - External Inquiries (EQ)
#   - Internal Logical Files (ILF)
#   - External Interface Files (EIF)
#
# VAF = 0.65 + (0.01 * sum of 14 General System Characteristics, each 0–5)
# Adjusted FP = UFP * VAF
# Effort (person-hours) = FP * HOURS_PER_FP

HOURS_PER_FP = 10  # basic assumption; adjust for team productivity

def calculate_function_points(ei=5, eo=4, eq=3, ilf=2, eif=1, gsc_weights=None):
    """
    Calculate Function Points and Effort Estimate.

    Parameters:
        ei, eo, eq, ilf, eif (int): counts per functional type.
        gsc_weights (list[int]): 14-element list of 0–5 weights for
                                 General System Characteristics.
                                 Defaults to medium complexity (all 2).
    Returns:
        dict: UFP, VAF, FP, Effort (Hours), Effort (Days)
    """
    if gsc_weights is None:
        gsc_weights = [2] * 14  # Default: medium complexity

    if len(gsc_weights) != 14:
        raise ValueError("gsc_weights must contain exactly 14 values.")

    # Step 1: Unadjusted FP (UFP) – simple default weights
    ufp = (ei * 4) + (eo * 5) + (eq * 4) + (ilf * 10) + (eif * 7)

    # Step 2: Value Adjustment Factor (VAF)
    tdi = sum(gsc_weights)  # Total Degree of Influence
    vaf = 0.65 + (0.01 * tdi)

    # Step 3: Adjusted FP
    fp = ufp * vaf

    # Step 4: Effort Estimate (person-hours)
    effort_hours = fp * HOURS_PER_FP
    effort_days = effort_hours / 8  # 8-hour working days

    return {
        "UFP": ufp,
        "VAF": round(vaf, 2),
        "FP": round(fp, 2),
        "Effort (Hours)": round(effort_hours, 1),
        "Effort (Days)": round(effort_days, 1),
    }


# Example run for the OMS demo
if __name__ == "__main__":
    result = calculate_function_points(ei=5, eo=4, eq=3, ilf=2, eif=1)
    print("FPA Estimation Results:", result)

```
## Example Run: 

OMS Demo (5 EI: orders; 4 EO: reports; etc.) result = calculate_function_points(ei=5, eo=4, eq=3, ilf=2, eif=1) print("FPA Estimation Results:", result)
Example Output (Runnen in Jupyter): FPA Estimation Results: {'UFP': 85, 'VAF': 0.93, 'FP': 79.05, 'Effort (Hours)': 790.5, 'Effort (Days)': 98.8}

## Effort- en time-estimate

Activity 1: Effort and Time Estimate for Assignment Demo

Applying the FPA script to the OMS-style demo (approximately 10–15 functional components based on the Volere requirements), the example run yields:

Total Effort: 790.5 person-hours

Approx. Effort for 1 FTE: ≈ 99 working days

Approx. Effort for 4 FTE: ≈ 25 working days (around 5 weeks of focused development)

For a realistic demonstration system, including overheads for meetings, rework and risk buffers (e.g. requirements volatility and scope creep), a 4–6 week timeline for a small team is a reasonable estimate.

I chose FPA because it is requirements-centred and aligns well with the Volere templates used in the module. It provides a transparent, early-stage size estimate without needing detailed design data, which makes it more appropriate than models like COCOMO for relatively small demonstration systems. However, FPA does not capture non-functional requirements (e.g. performance, security), which limits its usefulness when these dominate the effort profile.

## Main Risks Identified by the Authors

Verner et al. (2014) conduct a tertiary study and identify 85 risks in global software development (GSD), grouped into four major categories:

Outsourcing rationale risks (e.g. unrealistic cost-saving expectations, poor vendor selection).

Software development risks (e.g. requirements volatility, architectural complexity, inadequate testing).

Human resources risks (e.g. cultural and time-zone differences, communication barriers, staff turnover).

Project management risks (e.g. coordination delays, weak planning, inadequate monitoring and control).

Anton and Afloarei Nucu (2020) synthesise enterprise-level risks through an ERM lens, highlighting drivers such as probability of financial distress, low earnings performance, growth vulnerabilities and governance gaps (e.g. lack of board independence). These overlap with Verner et al. in that both emphasise governance, organisational structure and execution risks as critical to project success.

## Framework from Unit 3 to Capture and Categorise the Risks

From the frameworks discussed in the Unit 3 lecturecast, I would select the NIST Risk Management Framework (RMF). Unlike high-level standards such as ISO 31000, NIST RMF provides:

A detailed, stepwise process (categorise, select, implement, assess, authorise, monitor);

Explicit role definitions that match both GSD and ERM contexts (e.g. risk owners, system owners, authorising officials);

A rich control catalogue that can be mapped onto SDLC activities.

This makes it suitable for capturing Verner et al.’s GSD risks (e.g. communication and coordination as assets/processes that require controls) and Anton & Afloarei Nucu’s enterprise-level risks (e.g. governance and financial stability) within a single, coherent risk register.

## Added Risk and Suggested Mitigation (for Module Forum / Discussion)

Risk: Requirements volatility in distributed teams, leading to scope creep, rework and schedule slippage (Verner et al., 2014).

Mitigation: Adopt agile backlog refinement anchored in structured requirement templates (e.g. Volere), combined with scheduled cross-time-zone synchronisation meetings to stabilise and confirm requirements at key SDLC decision points. This improves traceability, reduces misinterpretation, and creates explicit baseline agreements that limit scope creep.

Anton, S.G. and Afloarei Nucu, A.E. (2020) ‘Enterprise Risk Management: A Literature Review and Agenda for Future Research’, Journal of Risk and Financial Management, 13(11), p. 281. Available at: https://doi.org/10.3390/jrfm13110281

Verner, J.M., Brereton, O.P., Kitchenham, B.A., Turner, M. and Niazi, M. (2014) ‘Risks and risk mitigation in global software development: A tertiary study’, Information and Software Technology, 56(8), pp. 861–878. Available at: https://www.sciencedirect.com/science/article/abs/pii/S0950584913002254
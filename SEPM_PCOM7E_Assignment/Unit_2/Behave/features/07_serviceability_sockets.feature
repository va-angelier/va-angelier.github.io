# Ensure field service without rework (sockets vs. soldered)
# Acceptance criteria:
#   - Socketed ROMs/ICs enable field replacement and reduce downtime (Appendix: Serviceability notes).

Feature: Sockets vs. soldered serviceability
  As EDC
  I want field-replaceable components
  So that service can be performed without specialist rework

  Scenario: Field ROM replacement on socketed boards
    Given ROMs are socketed (not soldered)
    When a new OS ROM pair is installed
    Then the system shall boot the new firmware without rework or reflow
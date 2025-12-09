# Preserve access to legacy software via emulator
# Acceptance criteria:
#   - Emulator requires ≥128KB and HB extensions; performance must be faithful (Appendix: Compatibility section).

Feature: Backward compatibility (emulator constraints)
  As EDC
  I want existing users to run legacy titles
  So that upgrade friction is reduced

  Scenario: Legacy title runs at original speed under emulator
    Given at least 128KB RAM
    And HB extensions are present in ROM or RAM
    When a supported legacy title is launched from the emulator disk
    Then gameplay speed shall match the original platform within ±5%


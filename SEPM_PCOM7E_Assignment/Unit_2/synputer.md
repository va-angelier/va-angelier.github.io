# File: features/01_rom_boot_priorities.feature
# Purpose: Verify boot order, fallback, and logging resilience
# Acceptance rationale (for e-portfolio):
# - Boot order must be configurable and honoured (Appendix §3.1.6).
# - If no bootable media exists, ROM BASIC is the defined fallback (Appendix §3.1.6–3.1.7).
# - OS must not crash when target log media is absent; redirect/suppress safely (Appendix §3.1.7).

Feature: ROM, boot priorities and fallback
  As EDC
  I want predictable boot priorities and safe fallback
  So that systems are field-supportable

  Scenario: Boot order A → B → ROM is honoured
    Given boot order is configured as A then B then ROM
    And there is no boot sector in drive A
    And a valid boot sector is present in drive B
    When the system powers on
    Then the OS shall boot from drive B
    And it shall not fall back to ROM BASIC

  Scenario: ROM BASIC fallback when no bootable media
    Given no boot sector is present in drive A or drive B
    When the system powers on
    Then the machine shall start ROM BASIC
    And the HB prompt ">" shall be shown

  Scenario: HB/OS continues when B is missing by redirecting logs
    Given HB/OS is configured to log to a RAM disk
    And drive B has no writable media
    When an error is emitted
    Then the OS shall not crash
    And the log entry shall be written to the RAM disk


# File: features/02_memory_capability.feature
# Purpose: Enforce minimum RAM and behaviour per memory matrix
# Acceptance rationale:
# - ≥512KB required for multitasking under the target OS (Appendix §3.1.8).
# - ≥1MB enables RAM-disk usage under HB/OS per matrix (Appendix §3.1.8).

Feature: Memory capability per matrix
  As EDC
  I want defined behaviour at 512KB and 1MB
  So that OS features perform reliably

  Scenario: 512KB enables multi-session under MccOS
    Given installed RAM is 512KB
    When two shell sessions are opened
    Then both sessions shall remain responsive without swap failures

  Scenario: 1MB provides RAM disk under HB/OS
    Given installed RAM is 1MB
    When HB/OS initialises
    Then a RAM disk of at least 400KB shall be mountable


# File: features/03_industry_os_gui.feature
# Purpose: Prove industry-standard OS support and GUI prerequisites
# Acceptance rationale:
# - Industry-standard OS boot from removable media (Appendix §3.1.6).
# - X‑Windows requires HiRes display, ≥512KB, and SCSI HDD (Appendix §5.3 / §3.1.8).
# - GEM under 68KDOS v2 leverages ROM pair and existing storage (Appendix §5.3).

Feature: Industry standard OS and GUI prerequisites
  As EDC
  I want the platform to run mainstream OS/GUI stacks
  So that users have a modern WIMP interface

  Scenario: Boots an industry-standard OS from removable media
    Given a Synputer with no BASIC auto-boot configured
    And an industry-standard OS boot disk is inserted in drive A
    When the system powers on
    Then the system shall boot into the OS from drive A
    And the OS shell shall be available to the user

  Scenario: X-Windows requires HiRes display and ≥512KB with SCSI HDD
    Given a HiRes display configuration is enabled
    And at least 512KB RAM
    And an external SCSI hard drive is attached
    When MccOS with X-Windows is installed
    Then the window manager shall start to a usable desktop

  Scenario: GEM under 68KDOS v2 uses ROM pair and existing storage
    Given 68KDOS v2 ROMs are installed (core and GEM libraries)
    When GEM desktop is launched
    Then it shall operate using the existing removable storage devices


# File: features/04_expansion_upgrade.feature
# Purpose: Validate upgrade path via Pro Expansion board
# Acceptance rationale:
# - CPU is at least 68000-class and field-upgradeable (Appendix §5.3).
# - SCSI storage enumerates via expansion I/O (Appendix §5.3 / I/O section).

Feature: Expansion and upgrade path (Pro Expansion board)
  As EDC
  I want a clear performance and longevity upgrade path
  So that the platform remains viable in service

  Scenario: System ships with ≥68000-class CPU
    Given a production unit
    When CPU information is queried
    Then the CPU shall be a Motorola 68000 or better

  Scenario: CPU upgrade via Pro Expansion board
    Given a Pro Expansion board is installed
    And a higher-grade 68k CPU is socketed on the expansion
    When the system boots
    Then POST shall succeed
    And the OS shall recognise the upgraded CPU

  Scenario: SCSI via Centronics-style connector with adapter
    Given a Pro Expansion board with I/O controller socketed
    And a Centronics-to-SCSI adapter cable is attached
    When the OS scans for storage
    Then the SCSI device shall be enumerated and mountable


# File: features/05_ula_io_serial.feature
# Purpose: Confirm ULA autodetection and serial physical-layer compliance
# Acceptance rationale:
# - IOP ULA auto-detects supported IO/INTSND chips (Appendix: ULA section/BOM).
# - Two serial ports available; RS‑422/RS‑485 compliance via SC100 (Appendix §I/O options).

Feature: ULA/IO autodetection and serial/network readiness
  As EDC
  I want robust I/O initialisation and serial standards support
  So that business comms and networking are possible

  Scenario: ULA auto-detects supported IO/INTSND chips
    Given any IO or INTSND chip listed in the hardware BOM is installed
    When the system initialises I/O
    Then the IOP ULA shall identify the chip
    And route signals correctly for standard operation

  Scenario: Two independent serial ports are available
    Given the system is powered on
    When serial ports are enumerated
    Then at least two ports shall be present and operational

  Scenario Outline: Physical-layer compliance for RS-422/RS-485 via SC100
    Given an SC100 is populated replacing the UART
    And a <standard> loopback fixture is connected to serial port 1
    When a 1KB test frame is transmitted
    Then the same frame shall be received without error
    Examples:
      | standard |
      | RS-422   |
      | RS-485   |


# File: features/06_sc150_input.feature
# Purpose: Verify external keyboard/mouse readiness via SC150
# Acceptance rationale:
# - External keyboard connector and international layouts (Appendix: Input).
# - SC150 multiplexes joystick port for dual keyboards/mice (Appendix: SC150 option).

Feature: External keyboards and mice via SC150
  As EDC
  I want flexible input for international markets
  So that users can choose layouts and pointing devices

  Scenario: External keyboard overrides integrated keyboard
    Given an external keyboard is connected at boot via SC150
    When the system initialises input devices
    Then the external keyboard shall be the active input device

  Scenario: Layout selection persists across reboots
    Given the user selects a DE layout in firmware or OS
    When the system reboots
    Then the DE layout shall remain active

  Scenario: Two external keyboards over SC150
    Given SC150 replaces the joystick interface
    And two external keyboards are attached via the SC150 cable
    When the system initialises input devices
    Then both keyboards shall be detected
    And one shall be selectable as the active layout device

  Scenario: Dual-mouse support over SC150 for GUI
    Given SC150 is installed
    And two mice are connected via SC150
    When the GUI session starts
    Then pointer movement and clicks shall operate UI widgets from either mouse




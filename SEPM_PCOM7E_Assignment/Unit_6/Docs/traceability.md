# Purpose: Requirement ↔ Feature ↔ Scenario mapping (for grading & audit)

| Requirement (restated) | Feature file | Scenario(s) |
|---|---|---|
| Configurable boot order; ROM BASIC fallback; safe logging | 01_rom_boot_priorities.feature | Boot order honoured · ROM BASIC fallback · Continue when B missing by redirecting logs |
| ≥512KB for multitasking; ≥1MB enables RAM disk | 02_memory_capability.feature | 512KB multi-session · 1MB RAM disk under HB/OS |
| Boots industry-standard OS from removable media | 03_industry_os_gui.feature | Boots an industry-standard OS from removable media |
| GUI readiness (X‑Windows/GEM); HiRes + SCSI + ≥512KB | 03_industry_os_gui.feature | X‑Windows requires HiRes+SCSI+≥512KB · GEM under 68KDOS v2 |
| ≥68000 CPU and upgrade path via Pro Expansion | 04_expansion_upgrade.feature | Ships with ≥68000 · CPU upgrade via Pro Expansion |
| SCSI storage via expansion I/O | 04_expansion_upgrade.feature | SCSI via Centronics-style adapter enumerates |
| ULA autodetects IO/INTSND; two serial ports | 05_ula_io_serial.feature | ULA autodetect · Two serial ports operational |
| RS‑422/RS‑485 compliance via SC100 | 05_ula_io_serial.feature | Scenario Outline loopback RS‑422/RS‑485 |
| External keyboard; layout persistence | 06_sc150_input.feature | External overrides; Layout persists |
| Dual keyboards/mice via SC150 | 06_sc150_input.feature | Two keyboards · Dual-mouse support |
| Socketed ROMs for field serviceability | 07_serviceability_sockets.feature | Field ROM replacement without reflow |
| Legacy compatibility via emulator (≥128KB, HB ext.) | 08_backward_compatibility.feature | Legacy title runs at original speed |

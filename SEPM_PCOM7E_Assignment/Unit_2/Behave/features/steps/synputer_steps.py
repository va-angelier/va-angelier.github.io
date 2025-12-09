from behave import given, when, then, step
from hamcrest import assert_that, equal_to, is_, contains_string

# -----------------------------
# Utilities
# -----------------------------

def _ensure_hw(context):
    if not hasattr(context, "hw"):
        raise RuntimeError("context.hw not initialised. Provide a harness in environment.py")

# -----------------------------
# Boot order / ROM BASIC / logging
# -----------------------------

@given("boot order is configured as A then B then ROM")
def step_set_boot_order(context):
    _ensure_hw(context)
    context.hw.set_boot_order(["A", "B", "ROM"])  # TODO: implement in harness

@given("there is no boot sector in drive A")
@given("no boot sector is present in drive A or drive B")
def step_no_boot_in_A(context):
    _ensure_hw(context)
    context.hw.set_media("A", bootable=False)

@given("a valid boot sector is present in drive B")
def step_boot_in_B(context):
    _ensure_hw(context)
    context.hw.set_media("B", bootable=True, os_image="GenericOS")

@when("the system powers on")
def step_power_on(context):
    _ensure_hw(context)
    context.hw.power_on()

@then("the OS shall boot from drive B")
def step_assert_boot_B(context):
    _ensure_hw(context)
    assert_that(context.hw.boot_source, equal_to("B"))

@then("it shall not fall back to ROM BASIC")
def step_assert_no_rom_basic(context):
    _ensure_hw(context)
    assert_that(context.hw.is_in_rom_basic(), is_(False))

@then("the machine shall start ROM BASIC")
def step_assert_rom_basic(context):
    _ensure_hw(context)
    assert_that(context.hw.is_in_rom_basic(), is_(True))

@then('the HB prompt ">" shall be shown')
def step_assert_hb_prompt(context):
    _ensure_hw(context)
    assert_that(context.hw.get_screen_text(), contains_string(">"))

@given("HB/OS is configured to log to a RAM disk")
def step_set_ramlog(context):
    _ensure_hw(context)
    context.hw.set_logging(target="ramdisk")

@given("drive B has no writable media")
def step_b_not_writable(context):
    _ensure_hw(context)
    context.hw.set_media("B", present=False)

@when("an error is emitted")
def step_emit_error(context):
    _ensure_hw(context)
    context.hw.emit_test_error("E_TEST")

@then("the OS shall not crash")
def step_assert_no_crash(context):
    _ensure_hw(context)
    assert_that(context.hw.os_alive(), is_(True))

@then("the log entry shall be written to the RAM disk")
def step_assert_ramlog(context):
    _ensure_hw(context)
    assert_that(context.hw.last_log_target(), equal_to("ramdisk"))

# -----------------------------
# Memory capability
# -----------------------------

@given("installed RAM is 512KB")
@given("installed RAM is 1MB")
@given("at least 128KB RAM")
@given("at least 512KB RAM")
def step_set_ram(context):
    _ensure_hw(context)
    # Parse number from step text
    text = context.step_name if hasattr(context, 'step_name') else context.step.sentence
    # Fallback: scan words
    target = None
    for token in str(text).split():
        if token.endswith("KB") or token.endswith("MB"):
            target = token
            break
    if not target:
        raise AssertionError("Could not parse RAM amount from step text: %r" % text)
    context.hw.set_ram(target)

@when("two shell sessions are opened")
def step_two_sessions(context):
    _ensure_hw(context)
    context.hw.open_shell_sessions(2)

@then("both sessions shall remain responsive without swap failures")
def step_sessions_ok(context):
    _ensure_hw(context)
    assert_that(context.hw.sessions_responsive(), is_(True))
    assert_that(context.hw.swap_failures(), equal_to(0))

@when("HB/OS initialises")
@when("the desktop session starts")
@when("the GUI session starts")
@when("the system initialises input devices")
@when("the system initialises I/O")
@when("the OS scans for storage")
@when("MccOS with X-Windows is installed")
@when("GEM desktop is launched")
@when("CPU information is queried")
@when("serial ports are enumerated")
@when("a 1KB test frame is transmitted")
@when("a test file is written and read back")
@when("a filesystem can be created and mounted successfully")
@when("a supported legacy title is launched from the emulator disk")
def step_generic_when(context):
    _ensure_hw(context)
    context.hw.perform_current_action(context.step.name)  # Dispatch by name in harness

@then("a RAM disk of at least 400KB shall be mountable")
def step_ramdisk_ok(context):
    _ensure_hw(context)
    assert_that(context.hw.ramdisk_size_kb() >= 400, is_(True))

# -----------------------------
# OS/GUI prerequisites
# -----------------------------

@given("a Synputer with no BASIC auto-boot configured")
def step_disable_basic_autoboot(context):
    _ensure_hw(context)
    context.hw.set_basic_autoboot(False)

@given("an industry-standard OS boot disk is inserted in drive A")
def step_insert_os_in_A(context):
    _ensure_hw(context)
    context.hw.set_media("A", bootable=True, os_image="GenericOS")

@then("the OS shell shall be available to the user")
@then("the window manager shall start to a usable desktop")
@then("pointer movement and basic clicks shall operate UI widgets")
@then("windows and menus shall render without clipping at the target resolution")
@then("the CPU shall be a Motorola 68000 or better")
@then("POST shall succeed")
@then("the OS shall recognise the upgraded CPU")
@then("the SCSI device shall be enumerated and mountable")
@then("at least two ports shall be present and operational")
@then("the same frame shall be received without error")
@then("both keyboards shall be detected")
@then("one shall be selectable as the active layout device")
@then("gameplay speed shall match the original platform within ±5%")
@then("the external keyboard shall be the active input device")
@then("the DE layout shall remain active")
@then("the system shall boot the new firmware without rework or reflow")
def step_generic_then(context):
    _ensure_hw(context)
    assert_that(context.hw.assert_condition(context.step.name), is_(True))

# -----------------------------
# Display / peripherals preconditions
# -----------------------------

@given("a HiRes display configuration is enabled")
def step_enable_hires(context):
    _ensure_hw(context)
    context.hw.set_display_mode("HiRes")

@given("an external SCSI hard drive is attached")
@given("a Centronics-to-SCSI adapter cable is attached")
@given("a Pro Expansion board with I/O controller socketed")
@given("a Pro Expansion board is installed")
@given("a higher-grade 68k CPU is socketed on the expansion")
@given("SC150 replaces the joystick interface")
@given("SC150 is installed")
@given("two mice are connected via SC150")
@given("two external keyboards are attached via the SC150 cable")
@given("an external keyboard is connected at boot via SC150")
@given("any IO or INTSND chip listed in the hardware BOM is installed")
@given("an SC100 is populated replacing the UART")
@given("a RS-422 loopback fixture is connected to serial port 1")
@given("a RS-485 loopback fixture is connected to serial port 1")
@given("68KDOS v2 ROMs are installed (core and GEM libraries)")
@given("HB extensions are present in ROM or RAM")
@given("a formatted disk is inserted")
@given("an industry-standard 3.5\" floppy drive is installed")
@given("a supported mouse is connected")
@given("the user selects a DE layout in firmware or OS")
@given("the HiRes graphics configuration is enabled")
@given("a supported SCSI host adapter is present")
@given("a SCSI hard disk is attached")
@given("no bootable media in drive A or B")
@given("no bootable media is present in A or B")
@given("no writable media is present in drive B")
@given("an industry-standard OS boot disk is inserted in drive A")
def step_preconditions_passthrough(context):
    _ensure_hw(context)
    context.hw.apply_precondition(context.step.name)
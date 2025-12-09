class DummyHarness:
    def __init__(self):
        self.boot_order = ["A", "B", "ROM"]
        self.media = {"A": {"present": False, "bootable": False},
                      "B": {"present": False, "bootable": False}}
        self._rom_basic = False
        self._screen = ""
        self._os_alive = True
        self._boot_source = None
        self._log_target = None
        self._ram = "512KB"
        self._display = "LoRes"

    # --- Harness operations (very simplified stubs) ---
    def set_boot_order(self, order):
        self.boot_order = order
    def set_media(self, drive, present=True, bootable=False, os_image=None):
        self.media[drive] = {"present": present, "bootable": bootable, "os_image": os_image}
    def power_on(self):
        # Simplified boot logic
        for d in self.boot_order:
            if d in self.media and self.media[d].get("bootable"):
                self._boot_source = d
                self._rom_basic = False
                return
        self._rom_basic = True
        self._screen = ">"
    def is_in_rom_basic(self):
        return self._rom_basic
    @property
    def boot_source(self):
        return self._boot_source
    def get_screen_text(self):
        return self._screen
    def set_logging(self, target):
        self._log_target = target
    def emit_test_error(self, code):
        # If target invalid, keep OS alive
        self._os_alive = True
    def os_alive(self):
        return self._os_alive
    def last_log_target(self):
        return self._log_target
    def set_ram(self, amount):
        self._ram = amount
    def open_shell_sessions(self, n):
        pass
    def sessions_responsive(self):
        return True
    def swap_failures(self):
        return 0
    def ramdisk_size_kb(self):
        return 512
    def set_basic_autoboot(self, enabled):
        pass
    def set_display_mode(self, mode):
        self._display = mode
    # Dispatchers for demo
    def perform_current_action(self, name):
        return True
    def assert_condition(self, name):
        return True
    def apply_precondition(self, name):
        return True


def before_all(context):
    # Replace DummyHarness with your real simulator/hardware abstraction
    context.hw = DummyHarness()

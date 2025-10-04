"""CLI entry point for the humanoid robot package.

Provides an interactive command loop for basic commands such as:
'navigate 5,5', 'pick bottle', 'speak hello', 'power on/off', 'tick', 'exit'.
"""

from __future__ import annotations

import traceback  # used for unexpected error reporting
from typing import Optional

from .robot_system import Robot, CLI


def main() -> None:
    """Run the interactive CLI loop for the robot."""
    robot = Robot("R1")
    cli = CLI()
    print(
        "Humanoid Robot CLI: Type commands (e.g., 'navigate 5,5', "
        "'pick bottle', 'speak hello', 'power on/off', 'tick', 'exit')"
    )
    try:
        while True:
            try:
                cmd_input = input("> ").strip()
            except EOFError:
                break

            if cmd_input == "exit":
                break

            if cmd_input == "power on":
                print("Power on:", robot.power_on())
                continue

            if cmd_input == "power off":
                print("Power off:", robot.power_off())
                continue

            parts = cmd_input.split(" ", 1)
            cmd = {"type": parts[0], "args": parts[1] if len(parts) > 1 else ""}

            cli.enqueue(cmd)
            next_cmd: Optional[dict[str, str]] = cli.read_command()
            if next_cmd:
                print(robot.tick(next_cmd))

    except KeyboardInterrupt:
        print("\nBye.")
    except Exception as exc:  # pylint: disable=broad-exception-caught
        traceback.print_exc()
        print(f"ERROR: Unexpected CLI failure: {exc}")


if __name__ == "__main__":
    main()

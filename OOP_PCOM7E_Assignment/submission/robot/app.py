"""Application entrypoint for the humanoid robot demo."""
from __future__ import annotations

from robot.controller import Robot
from robot.interface.cli import CLI


def main() -> None:
    """Run a simple interactive CLI session."""
    robot = Robot("R1")
    cli = CLI()
    print(
        "Humanoid Robot CLI: Type commands (e.g., 'navigate 5,5', "
        "'pick bottle', 'speak hello', 'power on/off', 'tick', 'exit')"
    )
    try:
        while True:
            cmd_input = input("> ").strip()
            if cmd_input in ("exit", "quit"):
                break
            if cmd_input == "power on":
                print("Power on:", robot.power_on());
                continue
            if cmd_input == "power off":
                print("Power off:", robot.power_off());
                continue

            parts = cmd_input.split(" ", 1)
            cmd = {"type": parts[0], "args": parts[1] if len(parts) > 1 else ""}
            cli.enqueue(cmd)
            next_cmd = cli.read_command()
            if next_cmd:
                print(robot.tick(next_cmd))
    except KeyboardInterrupt:
        print("\nBye.")


if __name__ == "__main__":
    main()

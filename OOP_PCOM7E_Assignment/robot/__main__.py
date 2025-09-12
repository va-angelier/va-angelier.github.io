# robot/__main__.py
from .robot_system import Robot, CLI, EnvObject, Waypoint

def main():
    robot = Robot("R1")
    cli = CLI()
    print("Humanoid Robot CLI: Type commands (e.g., 'navigate 5,5', "
          "'pick bottle', 'speak hello', 'power on/off', 'tick', 'exit')")
    while True:
        cmd_input = input("> ").strip()
        if cmd_input == "exit":
            break
        if cmd_input == "power on":
            print("Power on:", robot.power_on()); continue
        if cmd_input == "power off":
            print("Power off:", robot.power_off()); continue
        parts = cmd_input.split(" ", 1)
        cmd = {"type": parts[0], "args": parts[1] if len(parts) > 1 else ""}
        cli.enqueue(cmd)
        if cmd := cli.read_command():
            print(robot.tick(cmd))

if __name__ == "__main__":
    main()

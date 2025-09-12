from .robot_system import Robot, CLI

def main():
    robot = Robot("R1")
    cli = CLI()
    print("Humanoid Robot CLI: Type commands (e.g., 'navigate 5,5', "
          "'pick bottle', 'speak hello', 'power on/off', 'tick', 'exit')")
    try:
        while True:
            try:
                cmd_input = input("> ").strip()
            except EOFError:
                break
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
    except KeyboardInterrupt:
        print("\nBye.")
    except Exception:
        import traceback; traceback.print_exc()
        print("ERROR: Unexpected CLI failure")

if __name__ == "__main__":
    main()

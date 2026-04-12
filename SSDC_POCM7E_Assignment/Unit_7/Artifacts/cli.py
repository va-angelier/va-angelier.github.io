import os


def show_help():
    """
    Display the list of commands available in the shell.
    """
    print("\nAvailable commands:")
    print("  LIST            - List the contents of the current directory")
    print("  ADD x y         - Add two numbers together")
    print("  HELP            - Show this help message")
    print("  EXIT            - Exit the shell\n")


def list_directory():
    """
    List the files and folders in the current working directory.
    """
    try:
        contents = os.listdir(".")
        if contents:
            print("\nCurrent directory contents:")
            for item in contents:
                print(f" - {item}")
            print()
        else:
            print("\nThe current directory is empty.\n")
    except Exception as e:
        print(f"\nError listing directory: {e}\n")


def add_numbers(parts):
    """
    Add two numbers entered by the user.
    Expected format: ADD number1 number2
    """
    if len(parts) != 3:
        print("\nUsage: ADD <number1> <number2>\n")
        return

    try:
        number1 = float(parts[1])
        number2 = float(parts[2])
        result = number1 + number2
        print(f"\nResult: {result}\n")
    except ValueError:
        print("\nError: both inputs must be valid numbers.\n")


def run_shell():
    """
    Main shell loop.
    Repeatedly asks the user for input until EXIT is entered.
    """
    print("Simple Python Shell")
    print("Type HELP to see available commands.\n")

    while True:
        command = input("shell> ").strip()

        if not command:
            continue

        parts = command.split()
        action = parts[0].upper()

        if action == "LIST":
            list_directory()

        elif action == "ADD":
            add_numbers(parts)

        elif action == "HELP":
            show_help()

        elif action == "EXIT":
            print("\nExiting shell. Goodbye.")
            break

        else:
            print("\nUnknown command. Type HELP for a list of commands.\n")


if __name__ == "__main__":
    run_shell()
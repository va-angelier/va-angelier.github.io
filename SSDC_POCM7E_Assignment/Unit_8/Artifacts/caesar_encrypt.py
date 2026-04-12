from pathlib import Path

def caesar_encrypt(text: str, shift: int = 3) -> str:
    """
    Encrypt text using a Caesar cipher.

    Parameters:
        text (str): The input text to encrypt
        shift (int): Number of positions to shift characters

    Returns:
        str: Encrypted text
    """
    result = []

    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        elif char.islower():
            result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)

    return ''.join(result)


def encrypt_file(input_path: str, output_path: str, shift: int = 3) -> None:
    """
    Read a text file, encrypt its contents, and save to a new file.

    Parameters:
        input_path (str): Path to the input file
        output_path (str): Path to save the encrypted file
        shift (int): Caesar cipher shift value
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    # Read file content
    content = input_file.read_text(encoding='utf-8')

    # Encrypt content
    encrypted_content = caesar_encrypt(content, shift)

    # Write encrypted content
    Path(output_path).write_text(encrypted_content, encoding='utf-8')

    print(f"Encrypted file saved as: {output_path}")


# ---------------------------
# Demonstration section
# ---------------------------

if __name__ == "__main__":
    # Short text demonstration
    user_text = input("Enter text to encrypt: ")
    encrypted = caesar_encrypt(user_text)
    print(f"Encrypted text: {encrypted}")

    # File encryption demonstration
    # (Make sure 'input.txt' exists in your folder)
    try:
        encrypt_file("input.txt", "encrypted_output.txt")
    except FileNotFoundError as e:
        print(e)
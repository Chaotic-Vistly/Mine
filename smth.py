def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # Shift letter within its case range
            shift_base = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            # Keep non-alphabetic characters as they are
            result += char
    return result

# Get inputs
text = input("Enter text to encode: ")
shift = int(input("Enter shift value: "))
print("Encoded text:", caesar_cipher(text, shift))

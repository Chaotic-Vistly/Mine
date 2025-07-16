def guess_password(actual_password):
    for guess in range(1000001):

        guess_str = f"{guess:04d}"
        print(f"Trying password: {guess_str}")
        if guess_str == actual_password:
            print(f"Password found: {guess_str}")
            return guess_str
    print("Password not found!")
    return None

actual_password = "89235"
guessed_password = guess_password(actual_password)

def calculator():
    print("Welcome to my calculator.")
    a = float(input("Enter a number here: "))
    b = float(input("Enter a second number here: "))
    operation = str(input("Input an operation(+,-,*,/)"))
    if operation == "+":
        print(a+b)
    elif operation == "-":
        print(a - b)
    elif operation == "*":
        print(a * b)
    elif operation == "/":
        if b != 0:
            print(a/b)
        else:
            print("Error: Division by zero.")
    else:
        print("Invalid input please insert one of the operations(+,-,*,/)")
calculator()
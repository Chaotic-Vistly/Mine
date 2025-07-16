def fibonacci(n):

    a = [0, 1]
    for i in range(2, n):
        a.append(a[-1] + a[-2])
    return a[:n]

terms = int(input("Enter the number of terms: "))
print("Fibonacci sequence:", fibonacci(terms))

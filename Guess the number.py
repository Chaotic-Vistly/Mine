import random
import time

def guess_the_number():
    print("Guess the number")
    number = random.randint(1,100)
    attempts = 0

    print("I ve picked a number from 1 to 100. Will you be able to guess it?")
    time.sleep(1)

    while True:
        guess = int(input('Guess a number(1-100): '))
        if guess > number:
            print('Lower!')
            attempts = attempts + 1
        elif guess < number:
            print('Higher!')
            attempts = attempts + 1
        elif guess == number:
            print("Congrats you won!")
            time.sleep(1)
            print(f"It took {attempts} attempts.")
            break
        else:
            print("Please input an integer from 1 to 100.")

guess_the_number()
import time


hard = str(input("Input your hardest tasks for the day: "))
mid = str(input("Input your medium tasks for the day: "))
easy = str(input("Input your easiest tasks for the day: "))
answer = str(input("easy or hard ")).lower()
while answer == "easy":

    answer1 =str(input(f"\nAre you done with {easy}? ")).lower()
    if answer1 == "yes":
        print("Good job you may continue with your medium tasks: ")
        time.sleep(1)

        answer2 =str(input(f"\nAre you done with {mid}? ")).lower()
        if answer2 == "yes":
            print("Great job you may continue with your hard tasks: ")
            time.sleep(1)

            answer3 =str(input(f"\nAre you done with {hard}? ")).lower()
            if answer3 == "yes":
                print("Excellent! You have done all your tasks I am proud of you. Until next time!")
                break
            else:
                print("You haven't done your hardest tasks. You have to finish them before continuing.")
        else:
            print("You haven't done your medium tasks. You have to finish them before continuing.")
    else:
        print("You haven't done your easiest tasks. You have to finish them before continuing.")

while answer == hard:

    answer3 = str(input(f"\nAre you done with {hard}? ")).lower()
    if answer3 == "yes":
        print("Good job you may continue with your medium tasks: ")
        time.sleep(1)

        answer2 = str(input(f"\nAre you done with {mid}? ")).lower()
        if answer2 == "yes":
            print("Great job you may continue with your hard tasks: ")
            time.sleep(1)

            answer1 = str(input(f"\nAre you done with {easy}? ")).lower()
            if answer1 == "yes":
                print("Excellent! You have done all your tasks I am proud of you. Until next time!")
                break
            else:
                print("You haven't done your easiest tasks. You have to finish them before continuing.")
        else:
            print("You haven't done your medium tasks. You have to finish them before continuing.")
    else:
        print("You haven't done your hardest tasks. You have to finish them before continuing.")
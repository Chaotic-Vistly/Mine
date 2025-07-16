import random


def monty_hall_game():
    print("Welcome to the Monty Hall Game Show!")
    print("Behind one of the three doors is a car. The other two have goats.")
    print("Your goal is to win the car!")
    print("Doors: 1, 2, 3")

    # Randomly assign the car to one of the three doors
    car_door = random.randint(1, 3)

    # Player makes an initial choice
    player_choice = int(input("Choose a door (1, 2, or 3): "))
    while player_choice not in [1, 2, 3]:
        player_choice = int(input("Invalid choice. Choose a door (1, 2, or 3): "))

    # Host reveals a goat door
    possible_goat_doors = [door for door in [1, 2, 3] if door != car_door and door != player_choice]
    host_reveals = random.choice(possible_goat_doors)
    print(f"The host opens door {host_reveals} and reveals a goat.")

    # Player decides whether to switch
    remaining_door = [door for door in [1, 2, 3] if door != player_choice and door != host_reveals][0]
    switch_choice = input(f"Do you want to switch to door {remaining_door}? (yes or no): ").strip().lower()

    if switch_choice in ["yes", "y"]:
        player_choice = remaining_door

    # Reveal the result
    print(f"You chose door {player_choice}.")
    if player_choice == car_door:
        print("Congratulations! You won the car!")
    else:
        print("You got a goat. Better luck next time!")

    # Option to play again
    play_again = input("Do you want to play again? (yes or no): ").strip().lower()
    if play_again in ["yes", "y"]:
        monty_hall_game()
    else:
        print("Thanks for playing the Monty Hall Game Show!")


# Start the game
monty_hall_game()

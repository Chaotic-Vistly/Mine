import random


quests_list = []
total_xp = 0

print("Your Quests for the day are:")
print("Type 'stop' to finish entering quests.")

while True:
    quest = input("Enter your quest for the day: ")
    if quest.lower() == 'stop':
        break
    quests_list.append(quest)

if quests_list:
    print("\nHere's your list of quests for the day:")
    for i, quest in enumerate(quests_list, start=1):
        print(f"{i}. {quest}")

    print("\nLet's complete your quests!")

    for quest in quests_list:
        answer = input(f"Did you finish '{quest}'? (yes or no): ").strip().lower()
        if answer == 'yes':
            xp = random.randint(5, 20)
            print(f"Great job! You earned {xp} XP for completing '{quest}'.")
            total_xp += xp
        else:
            print(f"Don't forget to complete '{quest}' later!")

    print("\nAll quests are processed.")
    print(f"Congratulations! You earned a total of {total_xp} XP!")
else:
    print("You didn't enter any quests. Try again tomorrow!")


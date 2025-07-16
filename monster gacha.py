from tkinter import *
import random

# Rarity pool with probabilities
rarity_pool = {
    "Common": 0.60,
    "Rare": 0.25,
    "Epic": 0.10,
    "Legendary": 0.04,
    "Mythical": 0.01
}

# Image lists for each rarity
common_images = ["images/basic.png", "images/watermelon.png", "images/punch.png"]
rare_images = ["images/oceanlemon.png", "images/Monsterbutterfly.png"]
epic_images = ["images/ultrablack.png", "images/mango_loco.png", "images/mango.png"]
legendary_images = ["images/blueone.png", "images/purpleguy.png", "images/dreamstrawberry.png"]
mythical_images = ["images/the best.png"]

# Function to randomize and display an image
def click():
    rarity = random.choices(list(rarity_pool.keys()), weights=rarity_pool.values())[0]
    if rarity == "Common":
        chosen_image = random.choice(common_images)
    elif rarity == "Rare":
        chosen_image = random.choice(rare_images)
    elif rarity == "Epic":
        chosen_image = random.choice(epic_images)
    elif rarity == "Legendary":
        chosen_image = random.choice(legendary_images)
    else:
        chosen_image = random.choice(mythical_images)

    new_monster = PhotoImage(file=chosen_image)
    new_monster = new_monster.subsample(int(new_monster.width()/300), int(new_monster.height()/400))  # Resize to 300x300
    image_label.config(image=new_monster)
    image_label.image = new_monster  # Keep reference
    print(f"Rarity: {rarity}, Image: {chosen_image}")

# Main window
window = Tk()
window.config(bg="black")
window.geometry("800x800")
window.title("Monster Randomizer")

# Default image display
monster = PhotoImage(file="images/basic.png")
monster = monster.subsample(int(monster.width()/300), int(monster.height()/400))  # Resize to 300x300
image_label = Label(window, image=monster, bg="black", width=200, height=400)
image_label.pack()

# Spin button placed directly underneath the image
button = Button(window, text='Spin', fg="white", bg="black", command=click)
button.config(font=("Arial", 22, "bold"))
button.config(activebackground="black", activeforeground="blueviolet", compound="bottom")
button.pack()

window.mainloop()

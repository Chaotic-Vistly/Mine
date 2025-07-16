import matplotlib.pyplot as plt
import numpy as np

# Define category names
categories = ["Strength", "Agility", "Wisdom", "Charisma", "Endurance", "Luck", "Dexterity", "Intelligence"]


def draw_chaos_star(values):
    """
    Draws a chaos star shape based on 8 input values and labels the lines.

    Parameters:
        values (list): A list of 8 integers, each between 0 and 8.
    """
    if len(values) != 8 or any(v < 0 or v > 8 for v in values):
        raise ValueError("Input must be a list of 8 integers, each between 0 and 8.")

    # Angles for the 8 categories (45-degree intervals, in radians)
    angles = np.linspace(0, 2 * np.pi, 9)[:-1]

    # Prepare the plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

    # Set the background colors
    fig.patch.set_facecolor('black')  # Background of the entire figure
    ax.set_facecolor('black')  # Background of the polar plot

    # Draw each line and label it
    for angle, length, category in zip(angles, values, categories):
        # Draw the line
        ax.plot([angle, angle], [0, length], color='blueviolet', lw=2)  # Use bright color for visibility

        # Add labels slightly beyond the maximum length
        ax.text(angle, 8.5, category, ha='center', va='center', fontsize=10, color='cyan'and "red")

    # Set limits and remove clutter
    ax.set_ylim(0, 8)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['polar'].set_visible(False)
    ax.grid(False)

    # Adjust the title position
    plt.title("Chaos Star", fontsize=16, color='blueviolet', y=1.1)  # Move title up with `y=1.1`
    plt.show()


def get_user_input():
    """
    Prompts the user to enter values for each category.

    Returns:
        list: A list of 8 integers entered by the user.
    """
    print("Enter values for each category (0 to 8):")
    values = []
    for category in categories:
        while True:
            try:
                value = int(input(f"{category}: "))
                if 0 <= value <= 8:
                    values.append(value)
                    break
                else:
                    print("Value must be between 0 and 8. Try again.")
            except ValueError:
                print("Invalid input. Please enter an integer between 0 and 8.")
    return values


# Main Program
if __name__ == "__main__":
    values = get_user_input()
    draw_chaos_star(values)

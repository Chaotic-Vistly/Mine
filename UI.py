from tkinter import *

a = 0

def click():
    global a
    a += 1
    label.config(text=f"You've killed {a} beings")

    if 10 <= a < 20:
        window.config(bg="#fcb1b1")
    elif 20 <= a < 30:
        window.config(bg="#ff8a8a")
    elif 30 <= a < 40:
        window.config(bg="#fc6d6d")
    elif 40 <= a < 50:
        window.config(bg="#ff5959")
    elif 50 <= a < 60:
        window.config(bg="#ff4040")
    elif 60 <= a < 70:
        window.config(bg="#ff0f0f")
    elif 70 <= a < 80:
        window.config(bg="#ff0000")
    elif 80 <= a < 90:
        window.config(bg="#ba0202")
    elif 90 <= a < 100:
        window.config(bg="#820303")
    elif 100 <= a < 110:
        window.config(bg="#570000")
    elif 110 <= a < 120:
        window.config(bg="#330000")
    elif 120 <= a < 130:
        window.config(bg="#000000")
    elif a == 130:
        button.config(state=DISABLED)
        print("Why?")


window = Tk()
window.config(bg="white")




button = Button(window, text='Click to kill!')
why = PhotoImage(file="white-stick-figure-hi - Copy.png")
button.config(command=click)
button.config(font=("Ink Free", 40, "bold"))
button.config(bg="black", fg="#26ff00")
button.config(activebackground="black", activeforeground="#6a00ff")

photo = PhotoImage(file="d6rlwzf-1baa20b4-4f70-4721-aca9-c2020ab3be67 - Copy.png")
button.config(image=photo, compound="bottom")
button.pack()


label = Label(window, text=a, font=("Monospace", 40, "bold"))
label.config(bg="#403f3d")
label.pack()


window.mainloop()


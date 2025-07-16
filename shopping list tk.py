import tkinter as tk
from tkinter import messagebox

def add_item():
    item = entry.get()
    if item:
        listbox.insert(tk.END, item)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter an item.")

def delete_item():
    selected_items = listbox.curselection()
    if selected_items:
        for index in reversed(selected_items):
            listbox.delete(index)
    else:
        messagebox.showwarning("Selection Error", "Please select an item to delete.")

def clear_list():
    if messagebox.askyesno("Confirmation", "Are you sure you want to clear the entire list?"):
        listbox.delete(0, tk.END)


note = tk.Tk()
note.title("Shopping List")
note.config(bg="#689df2")


entry = tk.Entry(note, width=40)
entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
entry.config(font=("Lato", 12))


add_button = tk.Button(note, text="Add Item", command=add_item, font=("Lato", 15, "bold"))
add_button.grid(row=0, column=2, padx=10)


listbox = tk.Listbox(note, width=60, height=25, selectmode=tk.MULTIPLE)
listbox.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
listbox.config(bg="#81acf0", font=('Lato', 12))

delete_button = tk.Button(note, text="Delete Selected", command=delete_item, font=("Lato", 15, "bold"))
delete_button.grid(row=2, column=0, padx=10, pady=10)


clear_button = tk.Button(note, text="Clear List", command=clear_list, font=("Lato", 15, "bold"))
clear_button.grid(row=2, column=1, padx=10, pady=10)


quit_button = tk.Button(note, text="Quit", command=note.destroy, font=("Lato", 15, "bold"))
quit_button.grid(row=2, column=2, padx=10, pady=10)


note.mainloop()

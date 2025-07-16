import tkinter as tk


class Calculator:
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('360x540')
        self.win.title('Calculator')
        self.win.config(bg="#97d6fc")

        self.expression = ""

        self.create_buttons()

        self.win.mainloop()

    def create_buttons(self):

        for i in range(6):
            self.win.grid_rowconfigure(i, minsize=90)
        for i in range(4):
            self.win.grid_columnconfigure(i, minsize=90)


        self.res = tk.Label(self.win, text='0', font=("Italic", 25, "bold"), bg='blue', fg="gold", anchor="e")
        self.res.grid(row=0, column=0, sticky="ewns", columnspan=4)

        # Buttons
        buttons = [
            ("CE", 1, 0, self.clear), ("C", 1, 1, self.clear), ("+", 1, 2, lambda: self.add_to_expression("+")),
            ("-", 1, 3, lambda: self.add_to("-")),
            ("7", 2, 0, lambda: self.add_to("7")), ("8", 2, 1, lambda: self.add_to("8")),
            ("9", 2, 2, lambda: self.add_to("9")), ("*", 2, 3, lambda: self.add_to("*")),
            ("4", 3, 0, lambda: self.add_to("4")), ("5", 3, 1, lambda: self.add_to("5")),
            ("6", 3, 2, lambda: self.add_to("6")), ("/", 3, 3, lambda: self.add_to("/")),
            ("1", 4, 0, lambda: self.add_to("1")), ("2", 4, 1, lambda: self.add_to("2")),
            ("3", 4, 2, lambda: self.add_to("3")), ("=", 4, 3, self.calculate, 2),
            ("0", 5, 1, lambda: self.add_to("0")), (".", 5, 2, lambda: self.add_to("."))
        ]

        for btn in buttons:
            text, row, col, command = btn[:4]
            rowspan = btn[4] if len(btn) > 4 else 1
            tk.Button(self.win, text=text, bg="#1f7ced", command=command).grid(row=row, column=col, sticky='ewns',
                                                                               rowspan=rowspan)

    def add_to(self, value):
        if self.res["text"] == "0":
            self.res["text"] = value
        else:
            self.res["text"] += value
        self.expression += value

    def clear(self):
        self.expression = ""
        self.res["text"] = "0"

    def calculate(self):
        try:
            result = str(eval(self.expression))
            self.res["text"] = result
            self.expression = result
        except Exception as e:
            self.res["text"] = "Error"
            self.expression = ""



Calculator()

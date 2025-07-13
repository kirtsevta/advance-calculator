import tkinter as tk

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8F8FF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#FFCCCC"
LIGHT_GRAY = "#000000"
LABEL_COLOR = "#265E56"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x600")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_label()

        self.digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 1), '.': (4, 0)
        }

        self.operations = {
            "/": "\u00f7",
            "*": "\u00d7",
            "-": "\u2212",
            "+": "+"
        }

        self.button_frame = self.create_button_frame()
        self.button_frame.rowconfigure(0, weight=1)
        for x in range(1, 6):
            self.button_frame.rowconfigure(x, weight=1)
        for y in range(5):
            self.button_frame.columnconfigure(y, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_square_button()
        self.create_sqrt_button()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()

    def create_display_label(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E,
                               bg=LABEL_COLOR, fg=WHITE, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,
                         bg=LABEL_COLOR, fg=WHITE, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg="black")
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_button_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:15])  # Limit length

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.button_frame, text=str(digit), bg=OFF_WHITE, fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        if self.current_expression != "":
            self.total_expression += self.current_expression + operator
            self.current_expression = ""
            self.update_total_label()
            self.update_label()

    def create_operator_buttons(self):
        i = 1  # Start from row 1, because row 0 has C, x², √x
        for operator, symbol in self.operations.items():
            button = tk.Button(self.button_frame, text=symbol, bg=LIGHT_GRAY, fg=WHITE,
                               font=DIGITS_FONT_STYLE, borderwidth=0,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.button_frame, text="C", bg=LIGHT_GRAY, fg=WHITE,
                           font=DIGITS_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=0, sticky=tk.NSEW)

    def square(self):
        try:
            if self.current_expression:
                self.current_expression = str(eval(f"({self.current_expression})**2"))
            else:
                self.current_expression = "0"
        except:
            self.current_expression = "Error"
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.button_frame, text="x\u00b2", bg=LIGHT_GRAY, fg=WHITE,
                           font=DIGITS_FONT_STYLE, borderwidth=0, command=self.square)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def sqrt(self):
        try:
            if self.current_expression:
                self.current_expression = str(eval(f"({self.current_expression})**0.5"))
            else:
                self.current_expression = "0"
        except:
            self.current_expression = "Error"
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.button_frame, text="\u221ax", bg=LIGHT_GRAY, fg=WHITE,
                           font=DIGITS_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def create_equals_button(self):
        button = tk.Button(self.button_frame, text="=", bg=LIGHT_BLUE, fg=WHITE,
                           font=DIGITS_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=5, column=3, columnspan=2, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except:
            self.current_expression = "Error"
        self.update_label()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()

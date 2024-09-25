import tkinter as tk

# Function to update expression in the text entry
def press(num):
    global expression
    expression += str(num)
    equation.set(expression)

# Function to evaluate the final expression
def equalpress():
    try:
        global expression
        total = str(eval(expression))
        equation.set(total)
        expression = ""
    except:
        equation.set(" error ")
        expression = ""

# Function to clear the text entry
def clear():
    global expression
    expression = ""
    equation.set("")

# Creating the main GUI window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calculator")
    root.geometry("400x600")

    # Global variable to store the expression
    expression = ""

    # StringVar to update the display
    equation = tk.StringVar()

    # Entry widget to display the expression and result
    display = tk.Entry(root, textvariable=equation, font=('arial', 20, 'bold'), bd=20, insertwidth=4, width=14, borderwidth=4)
    display.grid(columnspan=4)

    # Buttons layout
    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
    ]

    # Loop to create buttons and assign actions
    for (text, row, col) in buttons:
        if text == '=':
            tk.Button(root, text=text, padx=20, pady=20, font=('arial', 20, 'bold'),
                      command=equalpress).grid(row=row, column=col)
        else:
            tk.Button(root, text=text, padx=20, pady=20, font=('arial', 20, 'bold'),
                      command=lambda t=text: press(t)).grid(row=row, column=col)

    # Clear button
    tk.Button(root, text='Clear', padx=80, pady=20, font=('arial', 20, 'bold'),
              command=clear).grid(row=5, columnspan=4)

    root.mainloop()

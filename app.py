# -*- coding: utf-8 -*-
from tkinter import Tk, END, Entry, N, E, S, W, Button, Canvas, Frame, Text, Scrollbar
from tkinter import font
from tkinter import Label
from functools import partial
import ast

memory_value = 0
history_widget = None # Global variable to hold the history widget

def get_input(entry, argu, font_obj, base_size):
    entry.insert(END, argu)
    adjust_font_size(entry, font_obj, base_size)

def backspace(entry, font_obj, base_size):
    input_len = len(entry.get())
    if input_len > 0:
        entry.delete(input_len - 1)
    adjust_font_size(entry, font_obj, base_size)

def clear(entry, font_obj, base_size):
    entry.delete(0, END)
    adjust_font_size(entry, font_obj, base_size)

def calc(entry, font_obj, base_size):
    global history_widget
    input_info = entry.get()
    # Replace unicode division sign with Python division operator
    input_info = input_info.replace('÷', '/').replace('×', '*').replace('−', '-').replace('^', '**')
    output = "" # Initialize output
    try:
        # Safely evaluate the expression using ast.literal_eval after parsing with ast.parse
        # This approach is safer than direct eval() for mathematical expressions.
        # We need to be careful as ast.literal_eval has limitations.
        # For this calculator's scope (basic arithmetic), it should be sufficient.
        node = ast.parse(input_info, mode='eval')

        # A custom evaluator for the limited set of operations
        def evaluate_ast(node):
            if isinstance(node, ast.Expression):
                return evaluate_ast(node.body)
            elif isinstance(node, ast.BinOp):
                left = evaluate_ast(node.left)
                right = evaluate_ast(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                elif isinstance(node.op, ast.Sub):
                    return left - right
                elif isinstance(node.op, ast.Mult):
                    return left * right
                elif isinstance(node.op, ast.Div):
                    if right == 0:
                        raise ZeroDivisionError
                    return left / right
                elif isinstance(node.op, ast.Pow):
                    return left ** right
                else:
                    raise ValueError("Unsupported operation")
            elif isinstance(node, ast.UnaryOp):
                operand = evaluate_ast(node.operand)
                if isinstance(node.op, ast.USub):
                    return -operand
                else:
                    raise ValueError("Unsupported unary operation")
            elif isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.Num): # For compatibility with older Python versions
                return node.n
            else:
                raise ValueError("Invalid expression structure")

        output_value = evaluate_ast(node)
        output = str(output_value)

        if history_widget:
            # Enable the widget to insert text
            history_widget.config(state='normal')
            history_widget.insert(END, f"{input_info} = {output}\n")
            # Disable the widget again to prevent direct editing
            history_widget.config(state='disabled')
            history_widget.see(END) # Scroll to the bottom

    except (SyntaxError, ValueError) as e:
        popupmsg(f"Invalid expression: {e}")
        output = ""
    except ZeroDivisionError:
        popupmsg()
        output = ""
    except Exception as e:
        popupmsg(f"An unexpected error occurred: {e}")
        output = ""

    clear(entry, font_obj, base_size)
    entry.insert(END, output)
    adjust_font_size(entry, font_obj, base_size)

def adjust_font_size(entry, font_obj, base_size):
    input_len = len(entry.get())
    if input_len > 10:
        new_size = max(12, base_size - (input_len - 10) * 2)
    else:
        new_size = base_size
    font_obj.configure(size=new_size)

def popupmsg(msg="Cannot divide by 0!\nEnter valid values"):
    popup = Tk()
    popup.resizable(0, 0)
    popup.geometry("200x100")
    popup.configure(bg="#121212")
    popup.title("Alert")
    label = Label(popup, text=msg, fg="#FFFFFF", bg="#121212", font=("Roboto", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", bg="#FF6200", fg="#FFFFFF", font=("Roboto", 10), command=popup.destroy, relief="flat", borderwidth=0)
    B1.pack(pady=10)
    popup.mainloop()

def add_to_memory(entry, font_obj, base_size):
    global memory_value
    try:
        current_value = float(entry.get())
        memory_value += current_value
    except ValueError:
        popupmsg("Invalid number in entry for M+")

def subtract_from_memory(entry, font_obj, base_size):
    global memory_value
    try:
        current_value = float(entry.get())
        memory_value -= current_value
    except ValueError:
        popupmsg("Invalid number in entry for M-")

def retrieve_memory(entry, font_obj, base_size):
    global memory_value
    clear(entry, font_obj, base_size)
    entry.insert(END, str(memory_value))
    adjust_font_size(entry, font_obj, base_size)

def clear_memory():
    global memory_value
    memory_value = 0

def cal():
    global history_widget # Access the global history widget variable
    root = Tk()
    root.title("गणकयन्त्रम्")
    root.resizable(0, 0)
    root.configure(bg="#000000")

    canvas = Canvas(root, width=320, height=600, bg="#000000", highlightthickness=0)
    canvas.grid(row=0, column=0, padx=10, pady=10)

    canvas.create_rectangle(15, 15, 305, 585, fill="#121212", outline="#FFFFFF", width=2, dash=(2, 2))
    canvas.create_oval(15, 15, 35, 35, fill="#121212", outline="#FFFFFF", width=2)
    canvas.create_oval(285, 15, 305, 35, fill="#121212", outline="#FFFFFF", width=2)
    canvas.create_oval(15, 565, 35, 585, fill="#121212", outline="#FFFFFF", width=2)
    canvas.create_oval(285, 565, 305, 585, fill="#121212", outline="#FFFFFF", width=2)

    calc_frame = Frame(root, bg="#121212")
    canvas.create_window(20, 20, window=calc_frame, anchor="nw", width=280, height=560)

    base_font_size = 24
    entry_font = font.Font(family="Roboto", size=base_font_size, weight="bold")
    entry = Entry(calc_frame, justify="right", font=entry_font, bg="#1C2526", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF")
    entry.grid(row=0, column=0, columnspan=4, sticky=N+W+S+E, padx=10, pady=(20, 10), ipady=20)

    # History display
    history_frame = Frame(calc_frame, bg="#1C2526") # Changed history_frame background
    history_frame.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W, padx=10, pady=(0, 10))
    history_frame.grid_rowconfigure(0, weight=1) # Allow history frame to expand vertically
    history_frame.grid_columnconfigure(0, weight=1) # Allow history frame to expand horizontally


    history_widget = Text(history_frame, bg="#1C2526", fg="#FFFFFF", font=("Roboto", 12), bd=0, state='disabled', wrap='word', height=5) # Added height
    history_widget.grid(row=0, column=0, sticky=N+S+E+W) # Use grid for history widget

    history_scrollbar = Scrollbar(history_frame, command=history_widget.yview)
    history_scrollbar.grid(row=0, column=1, sticky=N+S+W) # Use grid for scrollbar
    history_widget['yscrollcommand'] = history_scrollbar.set

    cal_button_bg = "#FF6200"
    num_button_bg = "#333333"
    other_button_bg = "#4A4A4A"
    text_fg = "#FFFFFF"
    button_active_bg = "#666666"

    num_button = partial(Button, calc_frame, fg=text_fg, bg=num_button_bg, font=("Roboto", 16), relief="flat",
                         activebackground=button_active_bg, borderwidth=0, highlightthickness=0)
    cal_button = partial(Button, calc_frame, fg=text_fg, bg=cal_button_bg, font=("Roboto", 16), relief="flat",
                         activebackground=button_active_bg, borderwidth=0, highlightthickness=0)
    other_button = partial(Button, calc_frame, fg=text_fg, bg=other_button_bg, font=("Roboto", 16), relief="flat",
                          activebackground=button_active_bg, borderwidth=0, highlightthickness=0)


    button_mc = other_button(text='MC', command=lambda: clear_memory())
    button_mc.grid(row=2, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_mr = other_button(text='MR', command=lambda: retrieve_memory(entry, entry_font, base_font_size))
    button_mr.grid(row=2, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_m_plus = other_button(text='M+', command=lambda: add_to_memory(entry, entry_font, base_font_size))
    button_m_plus.grid(row=2, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_m_minus = other_button(text='M-', command=lambda: subtract_from_memory(entry, entry_font, base_font_size))
    button_m_minus.grid(row=2, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)

    button_clear = num_button(text='C', command=lambda: clear(entry, entry_font, base_font_size))
    button_clear.grid(row=3, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_backspace = num_button(text='←', command=lambda: backspace(entry, entry_font, base_font_size))
    button_backspace.grid(row=3, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_divide = cal_button(text='÷', command=lambda: get_input(entry, '÷', entry_font, base_font_size))
    button_divide.grid(row=3, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_power = cal_button(text='^', command=lambda: get_input(entry, '^', entry_font, base_font_size))
    button_power.grid(row=3, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)


    button7 = num_button(text='7', command=lambda: get_input(entry, '7', entry_font, base_font_size))
    button7.grid(row=4, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button8 = num_button(text='8', command=lambda: get_input(entry, '8', entry_font, base_font_size))
    button8.grid(row=4, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button9 = num_button(text='9', command=lambda: get_input(entry, '9', entry_font, base_font_size))
    button9.grid(row=4, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button12 = cal_button(text='×', command=lambda: get_input(entry, '×', entry_font, base_font_size))
    button12.grid(row=4, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)

    button4 = num_button(text='4', command=lambda: get_input(entry, '4', entry_font, base_font_size))
    button4.grid(row=5, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button5 = num_button(text='5', command=lambda: get_input(entry, '5', entry_font, base_font_size))
    button5.grid(row=5, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button6 = num_button(text='6', command=lambda: get_input(entry, '6', entry_font, base_font_size))
    button6.grid(row=5, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button11 = cal_button(text='−', command=lambda: get_input(entry, '−', entry_font, base_font_size))
    button11.grid(row=5, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)

    button1 = num_button(text='1', command=lambda: get_input(entry, '1', entry_font, base_font_size))
    button1.grid(row=6, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button2 = num_button(text='2', command=lambda: get_input(entry, '2', entry_font, base_font_size))
    button2.grid(row=6, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button3 = num_button(text='3', command=lambda: get_input(entry, '3', entry_font, base_font_size))
    button3.grid(row=6, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button10 = cal_button(text='+', command=lambda: get_input(entry, '+', entry_font, base_font_size))
    button10.grid(row=6, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)

    button_open_paren = other_button(text='(', command=lambda: get_input(entry, '(', entry_font, base_font_size))
    button_open_paren.grid(row=7, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button0 = num_button(text='0', command=lambda: get_input(entry, '0', entry_font, base_font_size))
    button0.grid(row=7, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10) # Adjusted column
    button_close_paren = other_button(text=')', command=lambda: get_input(entry, ')', entry_font, base_font_size))
    button_close_paren.grid(row=7, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10) # Adjusted column
    button13 = num_button(text='.', command=lambda: get_input(entry, '.', entry_font, base_font_size))
    button13.grid(row=8, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10) # Adjusted row and column
    button17 = cal_button(text='=', command=lambda: calc(entry, entry_font, base_font_size))
    button17.grid(row=8, column=1, columnspan=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10) # Adjusted row, column, and columnspan


    def quit():
        root.quit()
    exit_button = Button(calc_frame, text='Quit', fg='#FFFFFF', bg='#D32F2F', font=("Roboto", 16), relief="flat",
                         command=quit, activebackground=button_active_bg, borderwidth=0)
    exit_button.grid(row=9, column=0, columnspan=4, padx=10, pady=10, sticky=N+S+E+W, ipady=10)


    for i in range(10): # Adjusted for new rows
        calc_frame.grid_rowconfigure(i, weight=1)
    for i in range(4):
        calc_frame.grid_columnconfigure(i, weight=1)

    # Give more weight to the history row
    calc_frame.grid_rowconfigure(1, weight=3)


    root.mainloop()

if __name__ == '__main__':
    cal()# -*- coding: utf-8 -*-
from tkinter import Tk, END, Entry, N, E, S, W, Button, Canvas, Frame, Text, Scrollbar
from tkinter import font
from tkinter import Label
from functools import partial
import ast

memory_value = 0
history_widget = None # Global variable to hold the history widget

def get_input(entry, argu, font_obj, base_size):
    entry.insert(END, argu)
    adjust_font_size(entry, font_obj, base_size)

def backspace(entry, font_obj, base_size):
    input_len = len(entry.get())
    if input_len > 0:
        entry.delete(input_len - 1)
    adjust_font_size(entry, font_obj, base_size)

def clear(entry, font_obj, base_size):
    entry.delete(0, END)
    adjust_font_size(entry, font_obj, base_size)

def calc(entry, font_obj, base_size):
    global history_widget
    input_info = entry.get()
    # Replace unicode division sign with Python division operator
    input_info = input_info.replace('÷', '/').replace('×', '*').replace('−', '-').replace('^', '**')
    output = "" # Initialize output
    try:
        # Safely evaluate the expression using ast.literal_eval after parsing with ast.parse
        # This approach is safer than direct eval() for mathematical expressions.
        # We need to be careful as ast.literal_eval has limitations.
        # For this calculator's scope (basic arithmetic), it should be sufficient.
        node = ast.parse(input_info, mode='eval')

        # A custom evaluator for the limited set of operations
        def evaluate_ast(node):
            if isinstance(node, ast.Expression):
                return evaluate_ast(node.body)
            elif isinstance(node, ast.BinOp):
                left = evaluate_ast(node.left)
                right = evaluate_ast(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                elif isinstance(node.op, ast.Sub):
                    return left - right
                elif isinstance(node.op, ast.Mult):
                    return left * right
                elif isinstance(node.op, ast.Div):
                    if right == 0:
                        raise ZeroDivisionError
                    return left / right
                elif isinstance(node.op, ast.Pow):
                    return left ** right
                else:
                    raise ValueError("Unsupported operation")
            elif isinstance(node, ast.UnaryOp):
                operand = evaluate_ast(node.operand)
                if isinstance(node.op, ast.USub):
                    return -operand
                else:
                    raise ValueError("Unsupported unary operation")
            elif isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.Num): # For compatibility with older Python versions
                return node.n
            else:
                raise ValueError("Invalid expression structure")

        output_value = evaluate_ast(node)
        output = str(output_value)

        if history_widget:
            # Enable the widget to insert text
            history_widget.config(state='normal')
            history_widget.insert(END, f"{input_info} = {output}\n")
            # Disable the widget again to prevent direct editing
            history_widget.config(state='disabled')
            history_widget.see(END) # Scroll to the bottom

    except (SyntaxError, ValueError) as e:
        popupmsg(f"Invalid expression: {e}")
        output = ""
    except ZeroDivisionError:
        popupmsg()
        output = ""
    except Exception as e:
        popupmsg(f"An unexpected error occurred: {e}")
        output = ""

    clear(entry, font_obj, base_size)
    entry.insert(END, output)
    adjust_font_size(entry, font_obj, base_size)

def adjust_font_size(entry, font_obj, base_size):
    input_len = len(entry.get())
    if input_len > 10:
        new_size = max(12, base_size - (input_len - 10) * 2)
    else:
        new_size = base_size
    font_obj.configure(size=new_size)

def popupmsg(msg="Cannot divide by 0!\nEnter valid values"):
    popup = Tk()
    popup.resizable(0, 0)
    popup.geometry("200x100")
    popup.configure(bg="#121212")
    popup.title("Alert")
    label = Label(popup, text=msg, fg="#FFFFFF", bg="#121212", font=("Roboto", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", bg="#FF6200", fg="#FFFFFF", font=("Roboto", 10), command=popup.destroy, relief="flat", borderwidth=0)
    B1.pack(pady=10)
    popup.mainloop()

def add_to_memory(entry, font_obj, base_size):
    global memory_value
    try:
        current_value = float(entry.get())
        memory_value += current_value
    except ValueError:
        popupmsg("Invalid number in entry for M+")

def subtract_from_memory(entry, font_obj, base_size):
    global memory_value
    try:
        current_value = float(entry.get())
        memory_value -= current_value
    except ValueError:
        popupmsg("Invalid number in entry for M-")

def retrieve_memory(entry, font_obj, base_size):
    global memory_value
    clear(entry, font_obj, base_size)
    entry.insert(END, str(memory_value))
    adjust_font_size(entry, font_obj, base_size)

def clear_memory():
    global memory_value
    memory_value = 0

def cal():
    global history_widget # Access the global history widget variable
    root = Tk()
    root.title("गणकयन्त्रम्")
    root.resizable(0, 0)
    root.configure(bg="#000000")

    canvas = Canvas(root, width=320, height=600, bg="#000000", highlightthickness=0)
    canvas.grid(row=0, column=0, padx=10, pady=10)

    canvas.create_rectangle(15, 15, 305, 585, fill="#121212", outline="#FFFFFF", width=2, dash=(2, 2))
    canvas.create_oval(15, 15, 35, 35, fill="#121212", outline="#FFFFFF", width=2)
    canvas.create_oval(285, 15, 305, 35, fill="#121212", outline="#FFFFFF", width=2)
    canvas.create_oval(15, 565, 35, 585, fill="#121212", outline="#FFFFFF", width=2)
    canvas.create_oval(285, 565, 305, 585, fill="#121212", outline="#FFFFFF", width=2)

    calc_frame = Frame(root, bg="#121212")
    canvas.create_window(20, 20, window=calc_frame, anchor="nw", width=280, height=560)

    base_font_size = 24
    entry_font = font.Font(family="Roboto", size=base_font_size, weight="bold")
    entry = Entry(calc_frame, justify="right", font=entry_font, bg="#1C2526", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF")
    entry.grid(row=0, column=0, columnspan=4, sticky=N+W+S+E, padx=10, pady=(20, 10), ipady=20)

    # History display
    history_frame = Frame(calc_frame, bg="#1C2526") # Changed history_frame background
    history_frame.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W, padx=10, pady=(0, 10))
    history_frame.grid_rowconfigure(0, weight=1) # Allow history frame to expand vertically
    history_frame.grid_columnconfigure(0, weight=1) # Allow history frame to expand horizontally


    history_widget = Text(history_frame, bg="#1C2526", fg="#FFFFFF", font=("Roboto", 12), bd=0, state='disabled', wrap='word', height=5) # Added height
    history_widget.grid(row=0, column=0, sticky=N+S+E+W) # Use grid for history widget

    history_scrollbar = Scrollbar(history_frame, command=history_widget.yview)
    history_scrollbar.grid(row=0, column=1, sticky=N+S+W) # Use grid for scrollbar
    history_widget['yscrollcommand'] = history_scrollbar.set

    cal_button_bg = "#FF6200"
    num_button_bg = "#333333"
    other_button_bg = "#4A4A4A"
    text_fg = "#FFFFFF"
    button_active_bg = "#666666"

    num_button = partial(Button, calc_frame, fg=text_fg, bg=num_button_bg, font=("Roboto", 16), relief="flat",
                         activebackground=button_active_bg, borderwidth=0, highlightthickness=0)
    cal_button = partial(Button, calc_frame, fg=text_fg, bg=cal_button_bg, font=("Roboto", 16), relief="flat",
                         activebackground=button_active_bg, borderwidth=0, highlightthickness=0)
    other_button = partial(Button, calc_frame, fg=text_fg, bg=other_button_bg, font=("Roboto", 16), relief="flat",
                          activebackground=button_active_bg, borderwidth=0, highlightthickness=0)


    button_mc = other_button(text='MC', command=lambda: clear_memory())
    button_mc.grid(row=2, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_mr = other_button(text='MR', command=lambda: retrieve_memory(entry, entry_font, base_font_size))
    button_mr.grid(row=2, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_m_plus = other_button(text='M+', command=lambda: add_to_memory(entry, entry_font, base_font_size))
    button_m_plus.grid(row=2, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_m_minus = other_button(text='M-', command=lambda: subtract_from_memory(entry, entry_font, base_font_size))
    button_m_minus.grid(row=2, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)

    button_clear = num_button(text='C', command=lambda: clear(entry, entry_font, base_font_size))
    button_clear.grid(row=3, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_backspace = num_button(text='←', command=lambda: backspace(entry, entry_font, base_font_size))
    button_backspace.grid(row=3, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_divide = cal_button(text='÷', command=lambda: get_input(entry, '÷', entry_font, base_font_size))
    button_divide.grid(row=3, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button_power = cal_button(text='^', command=lambda: get_input(entry, '^', entry_font, base_font_size))
    button_power.grid(row=3, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)


    button7 = num_button(text='7', command=lambda: get_input(entry, '7', entry_font, base_font_size))
    button7.grid(row=4, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button8 = num_button(text='8', command=lambda: get_input(entry, '8', entry_font, base_font_size))
    button8.grid(row=4, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button9 = num_button(text='9', command=lambda: get_input(entry, '9', entry_font, base_font_size))
    button9.grid(row=4, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button12 = cal_button(text='×', command=lambda: get_input(entry, '×', entry_font, base_font_size))
    button12.grid(row=4, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)

    button4 = num_button(text='4', command=lambda: get_input(entry, '4', entry_font, base_font_size))
    button4.grid(row=5, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button5 = num_button(text='5', command=lambda: get_input(entry, '5', entry_font, base_font_size))
    button5.grid(row=5, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button6 = num_button(text='6', command=lambda: get_input(entry, '6', entry_font, base_font_size))
    button6.grid(row=5, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button11 = cal_button(text='−', command=lambda: get_input(entry, '−', entry_font, base_font_size))
    button11.grid(row=5, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)

    button1 = num_button(text='1', command=lambda: get_input(entry, '1', entry_font, base_font_size))
    button1.grid(row=6, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button2 = num_button(text='2', command=lambda: get_input(entry, '2', entry_font, base_font_size))
    button2.grid(row=6, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button3 = num_button(text='3', command=lambda: get_input(entry, '3', entry_font, base_font_size))
    button3.grid(row=6, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button10 = cal_button(text='+', command=lambda: get_input(entry, '+', entry_font, base_font_size))
    button10.grid(row=6, column=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10)

    button_open_paren = other_button(text='(', command=lambda: get_input(entry, '(', entry_font, base_font_size))
    button_open_paren.grid(row=7, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10)
    button0 = num_button(text='0', command=lambda: get_input(entry, '0', entry_font, base_font_size))
    button0.grid(row=7, column=1, padx=5, pady=5, sticky=N+S+E+W, ipady=10) # Adjusted column
    button_close_paren = other_button(text=')', command=lambda: get_input(entry, ')', entry_font, base_font_size))
    button_close_paren.grid(row=7, column=2, padx=5, pady=5, sticky=N+S+E+W, ipady=10) # Adjusted column
    button13 = num_button(text='.', command=lambda: get_input(entry, '.', entry_font, base_font_size))
    button13.grid(row=8, column=0, padx=5, pady=5, sticky=N+S+E+W, ipady=10) # Adjusted row and column
    button17 = cal_button(text='=', command=lambda: calc(entry, entry_font, base_font_size))
    button17.grid(row=8, column=1, columnspan=3, padx=5, pady=5, sticky=N+S+E+W, ipady=10) # Adjusted row, column, and columnspan


    def quit():
        root.quit()
    exit_button = Button(calc_frame, text='Quit', fg='#FFFFFF', bg='#D32F2F', font=("Roboto", 16), relief="flat",
                         command=quit, activebackground=button_active_bg, borderwidth=0)
    exit_button.grid(row=9, column=0, columnspan=4, padx=10, pady=10, sticky=N+S+E+W, ipady=10)


    for i in range(10): # Adjusted for new rows
        calc_frame.grid_rowconfigure(i, weight=1)
    for i in range(4):
        calc_frame.grid_columnconfigure(i, weight=1)

    # Give more weight to the history row
    calc_frame.grid_rowconfigure(1, weight=3)


    root.mainloop()

if __name__ == '__main__':
    cal()

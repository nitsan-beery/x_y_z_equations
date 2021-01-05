import tkinter as tk
from tkinter import ttk
from EquationsSolver import *


def toggle(b):
    if b.config('relief')[-1] == 'sunken':
        b.config(relief="raised")
        return 'off'
    else:
        b.config(relief="sunken")
        return 'on'


class EquationsWindow:
    def __init__(self):
        self.window_main = tk.Tk(className=' Equations Solver')
        self.window_main.resizable(1, 0)

        self.label_name_x = []
        self.entry_x = []
        self.entry_n = []
        self.label_plus = []
        self.label_equal = []
        self.label_empty = []
        self.label_row = []
        self.label_empty_21 = None
        self.label_n = None

        self.frame_1_output = tk.Frame(self.window_main)
        self.frame_1_output.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.frame_2_input = tk.Frame(self.window_main)
        self.frame_2_input.pack(side=tk.TOP, fill=tk.BOTH)
        self.frame_3_buttons = tk.Frame(self.window_main)
        self.frame_3_buttons.pack(side=tk.TOP, fill=tk.BOTH, ipady=6)

        self.label_empty_11 = tk.Label(self.frame_1_output, text='')
        self.label_empty_11.pack(side=tk.LEFT, pady=5, ipady=3)
        self.entry_answer = tk.Entry(self.frame_1_output, text='', bg='#FFFFCC')
        self.entry_answer.pack(side=tk.LEFT, ipady=3, fill='x', expand=True)
        combo_values = []
        for i in range(2, gv.MAX_MATRIX_SIZE+1):
            combo_values.append(f'{i} x {i}')
        self.combo_nxn = ttk.Combobox(self.frame_1_output, values=combo_values, width=4)
        self.combo_nxn.pack(side=tk.RIGHT, ipady=1, padx=5)
        self.combo_nxn.current(gv.MATRIX_SIZE-2)
        self.combo_nxn.bind("<<ComboboxSelected>>", self.change_nxn_event)

        self.set_window_nxn()

        self.label_empty_31 = tk.Label(self.frame_3_buttons, text='')
        self.button_solve = tk.Button(self.frame_3_buttons, text='Solve', width=4, bg='#CCFFCC', command=self.solve)
        self.button_reset = tk.Button(self.frame_3_buttons, text='Reset', width=4, bg='#F9C7C7', command=self.reset)
        self.button_fraction = tk.Button(self.frame_3_buttons, text=gv.show_fraction, width=6, command=self.switch_fraction_type)
        self.button_steps = tk.Button(self.frame_3_buttons, text='show steps', width=8, command=self.switch_show_steps_mode)

        self.label_empty_31.pack(side=tk.TOP)
        self.button_solve.pack(side=tk.LEFT, padx=5)
        self.button_reset.pack(side=tk.RIGHT, padx=5)
        self.button_fraction.pack(side=tk.RIGHT, padx=5)
        self.button_steps.pack(side=tk.RIGHT, padx=5)

        self.window_main.bind('<Key>', self.board_key)

        self.solution = None
        self.reset()
        if gv.show_steps:
            self.button_steps.config(relief="sunken")

    def set_window_nxn(self, n=gv.MATRIX_SIZE):
        self.set_matrix_nxn(n)

        width = 275 + 57 * (gv.MATRIX_SIZE-2)
        height = 200 + 44 * (gv.MATRIX_SIZE-2)
        self.window_main.geometry(f'{width}x{height}')
        
        name_x = get_name_x(n)

        self.label_empty_21 = tk.Label(self.frame_2_input, text='')
        self.label_empty_21.grid(row=1, column=0, padx=25)
        self.label_n = tk.Label(self.frame_2_input, text='n', padx=5)

        for i in range(0, gv.MATRIX_SIZE):
            self.label_name_x[i] = tk.Label(self.frame_2_input, text=name_x[i].capitalize(), padx=5)
            self.label_name_x[i].grid(row=1, column=2*i+1)
        self.label_n.grid(row=1, column=2*gv.MATRIX_SIZE+1)

        for row in range(0, gv.MATRIX_SIZE):
            self.label_empty[row] = tk.Label(self.frame_2_input, text='')
            self.label_empty[row].grid(row=row*2+1, column=0, pady=1)
            self.label_row[row] = tk.Label(self.frame_2_input, text=row+1)
            self.label_row[row].grid(row=2*(row+1), column=0, padx=5, sticky='E')
            for col in range(0, gv.MATRIX_SIZE):
                self.entry_x[row][col] = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_SIZE)
                self.entry_x[row][col].grid(row=2*(row+1), column=2*col+1, padx=5)
                self.label_plus[row][col] = tk.Label(self.frame_2_input, text='+')
                self.label_plus[row][col].grid(row=2*(row+1), column=2*(col+1))
            self.label_equal[row] = tk.Label(self.frame_2_input, text='=')
            self.label_equal[row].grid(row=2*(row+1), column=2*gv.MATRIX_SIZE, padx=5)
            self.entry_n[row] = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_SIZE)
            self.entry_n[row].grid(row=2*(row+1), column=2*gv.MATRIX_SIZE+1, padx=5)

    def set_matrix_nxn(self, n):
        for widget in self.frame_2_input.winfo_children():
            widget.destroy()
        self.label_name_x = []
        self.entry_x = []
        self.entry_n = []
        self.label_plus = []
        self.label_equal = []
        self.label_empty = []
        self.label_row = []
        none_row = []
        for col in range(0, n):
            none_row.append(None)
        for row in range(0, n):
            self.label_name_x.append(None)
            self.entry_x.append(none_row.copy())
            self.entry_n.append(None)
            self.label_plus.append(none_row.copy())
            self.label_equal.append(None)
            self.label_empty.append(None)
            self.label_row.append(None)
        gv.MATRIX_SIZE = n

    # change matrix size if n != 0
    def reset(self, n=0):
        if n > 0:
            self.set_window_nxn(n)
        self.clear_entries()
        self.solution = gv.no_solution
        self.entry_x[0][0].focus_set()
        self.entry_x[0][0].selection_range(0, tk.END)

    def clear_entries(self):
        for row in range(0, gv.MATRIX_SIZE):
            for col in range(0, gv.MATRIX_SIZE):
                self.entry_x[row][col].delete(0, tk.END)
                self.entry_x[row][col].insert(0, 0)
            self.entry_n[row].delete(0, tk.END)
            self.entry_n[row].insert(0, 0)
        self.entry_answer.delete(0, tk.END)

    def change_nxn_event(self, event):
        values = self.combo_nxn['values']
        choice = event.widget.get()
        n = values.index(choice)+2
        if n == gv.MATRIX_SIZE:
            self.entry_x[0][0].focus_set()
            self.entry_x[0][0].selection_range(0, tk.END)
        else:
            self.reset(n)

    def solve(self):
        name_x = get_name_x()
        empty_row = []
        x = []
        for i in range(0, gv.MATRIX_SIZE+1):
            empty_row.append(None)
        for i in range(0, gv.MATRIX_SIZE):
            x.append(empty_row.copy())
        self.entry_answer.delete(0, tk.END)
        for row in range(0, gv.MATRIX_SIZE):
            for col in range(0, gv.MATRIX_SIZE):
                try:
                    x[row][col] = Fraction(self.entry_x[row][col].get())
                except (ValueError, ZeroDivisionError):
                    self.entry_answer.insert(0, f'invalid {name_x[col].capitalize()}[{row+1}]')
                    self.entry_x[row][col].focus_set()
                    self.entry_x[row][col].selection_range(0, tk.END)
                    return
            try:
                x[row][-1] = Fraction(self.entry_n[row].get())
            except (ValueError, ZeroDivisionError):
                self.entry_answer.insert(0, f'invalid n[{row+1}]')
                return

        self.solution = solve_matrix(x, show_steps_improper=False)
        self.entry_answer.insert(0, ' ' + get_solution_string(self.solution))

    def switch_fraction_type(self):
        fraction_type = [gv.fraction_type_improper, gv.fraction_type_proper, gv.fraction_type_float]
        n = fraction_type.index(gv.show_fraction)
        gv.show_fraction = fraction_type[(n+1) % len(fraction_type)]
        self.button_fraction.config(text=gv.show_fraction)
        if self.solution != gv.no_solution:
            self.entry_answer.delete(0, tk.END)
            self.entry_answer.insert(0, ' ' + get_solution_string(self.solution))

    def switch_show_steps_mode(self):
        if toggle(self.button_steps) == "on":
            gv.show_steps = True
        else:
            gv.show_steps = False

    def board_key(self, key):
        if key.keycode == 13:
            self.solve()

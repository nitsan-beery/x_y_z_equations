import tkinter as tk
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
        self.window_main.geometry('320x250')
        self.window_main.resizable(0, 0)

        self.frame_1_output = tk.Frame(self.window_main)
        self.frame_1_output.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.frame_2_input = tk.Frame(self.window_main)
        self.frame_2_input.pack(side=tk.TOP, fill=tk.BOTH)
        self.frame_3_buttons = tk.Frame(self.window_main)
        self.frame_3_buttons.pack(side=tk.TOP, fill=tk.BOTH, ipady=6)

        self.entry_answer = tk.Entry(self.frame_1_output, text='', width=50, bg='#FFFFCC')
        self.entry_answer.grid(row=0, column=0, padx=5, pady=5, ipady=3)

        self.label_empty_21 = tk.Label(self.frame_2_input, text='')
        self.label_x = tk.Label(self.frame_2_input, text='X', padx=5)
        self.label_y = tk.Label(self.frame_2_input, text='Y', padx=5)
        self.label_z = tk.Label(self.frame_2_input, text='Z', padx=5)
        self.label_n = tk.Label(self.frame_2_input, text='n', padx=5)

        self.label_empty_21.grid(row=1, column=0, padx=25)
        self.label_x.grid(row=1, column=1)
        self.label_y.grid(row=1, column=3)
        self.label_z.grid(row=1, column=5)
        self.label_n.grid(row=1, column=7)

        self.label_row1 = tk.Label(self.frame_2_input, text='1')
        self.entry_x00 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_plus01 = tk.Label(self.frame_2_input, text='+')
        self.entry_x01 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_plus02 = tk.Label(self.frame_2_input, text='+')
        self.entry_x02 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_equal0 = tk.Label(self.frame_2_input, text='=')
        self.entry_n0 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)

        self.label_row1.grid(row=2, column=0, padx=5, sticky='E')
        self.entry_x00.grid(row=2, column=1, padx=5)
        self.label_plus01.grid(row=2, column=2)
        self.entry_x01.grid(row=2, column=3, padx=5)
        self.label_plus02.grid(row=2, column=4)
        self.entry_x02.grid(row=2, column=5, padx=5)
        self.label_equal0.grid(row=2, column=6)
        self.entry_n0.grid(row=2, column=7, padx=5)

        self.label_empty_22 = tk.Label(self.frame_2_input, text='')
        self.label_row2 = tk.Label(self.frame_2_input, text='2')
        self.entry_x10 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_plus11 = tk.Label(self.frame_2_input, text='+')
        self.entry_x11 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_plus12 = tk.Label(self.frame_2_input, text='+')
        self.entry_x12 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_equal1 = tk.Label(self.frame_2_input, text='=')
        self.entry_n1 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)

        self.label_empty_22.grid(row=3, column=0, pady=1)
        self.label_row2.grid(row=4, column=0, padx=5, sticky='E')
        self.entry_x10.grid(row=4, column=1, padx=5)
        self.label_plus11.grid(row=4, column=2)
        self.entry_x11.grid(row=4, column=3, padx=5)
        self.label_plus12.grid(row=4, column=4)
        self.entry_x12.grid(row=4, column=5, padx=5)
        self.label_equal1.grid(row=4, column=6)
        self.entry_n1.grid(row=4, column=7, padx=5)

        self.label_empty_23 = tk.Label(self.frame_2_input, text='')
        self.label_row3 = tk.Label(self.frame_2_input, text='3')
        self.entry_x20 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_plus21 = tk.Label(self.frame_2_input, text='+')
        self.entry_x21 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_plus22 = tk.Label(self.frame_2_input, text='+')
        self.entry_x22 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)
        self.label_equal2 = tk.Label(self.frame_2_input, text='=')
        self.entry_n2 = tk.Entry(self.frame_2_input, width=gv.X_ENTRY_ZIZE)

        self.label_empty_23.grid(row=5, column=0, pady=1)
        self.label_row3.grid(row=6, column=0, padx=5, sticky='E')
        self.entry_x20.grid(row=6, column=1, padx=5)
        self.label_plus21.grid(row=6, column=2)
        self.entry_x21.grid(row=6, column=3, padx=5)
        self.label_plus22.grid(row=6, column=4)
        self.entry_x22.grid(row=6, column=5, padx=5)
        self.label_equal2.grid(row=6, column=6)
        self.entry_n2.grid(row=6, column=7, padx=5)

        self.label_empty_31 = tk.Label(self.frame_3_buttons, text='')
        self.button_solve = tk.Button(self.frame_3_buttons, text='Solve', width=4, bg='#CCFFCC', command=self.solve)
        self.button_reset = tk.Button(self.frame_3_buttons, text='Reset', width=4, bg='#F9C7C7', command=self.reset)
        self.button_fraction = tk.Button(self.frame_3_buttons, text='m(n/q)', width=6, command=self.switch_fraction_type)
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
        if gv.show_int_above_1:
            self.button_fraction.config(relief="sunken")

    def reset(self):
        self.entry_x00.delete(0, tk.END)
        self.entry_x00.insert(0, 0)
        self.entry_x01.delete(0, tk.END)
        self.entry_x01.insert(0, 0)
        self.entry_x02.delete(0, tk.END)
        self.entry_x02.insert(0, 0)
        self.entry_x10.delete(0, tk.END)
        self.entry_x10.insert(0, 0)
        self.entry_x11.delete(0, tk.END)
        self.entry_x11.insert(0, 0)
        self.entry_x12.delete(0, tk.END)
        self.entry_x12.insert(0, 0)
        self.entry_x20.delete(0, tk.END)
        self.entry_x20.insert(0, 0)
        self.entry_x21.delete(0, tk.END)
        self.entry_x21.insert(0, 0)
        self.entry_x22.delete(0, tk.END)
        self.entry_x22.insert(0, 0)
        self.entry_n0.delete(0, tk.END)
        self.entry_n0.insert(0, 0)
        self.entry_n1.delete(0, tk.END)
        self.entry_n1.insert(0, 0)
        self.entry_n2.delete(0, tk.END)
        self.entry_n2.insert(0, 0)

        self.solution = gv.no_solution
        self.entry_answer.delete(0, tk.END)
        self.entry_x00.focus_set()
        self.entry_x00.selection_range(0, tk.END)

    def solve(self):
        x = [
            [Rational(self.entry_x00.get()), Rational(self.entry_x01.get()), Rational(self.entry_x02.get()), Rational(self.entry_n0.get())],
            [Rational(self.entry_x10.get()), Rational(self.entry_x11.get()), Rational(self.entry_x12.get()), Rational(self.entry_n1.get())],
            [Rational(self.entry_x20.get()), Rational(self.entry_x21.get()), Rational(self.entry_x22.get()), Rational(self.entry_n2.get())]
            ]
        self.entry_answer.delete(0, tk.END)
        for row in range(0, gv.MATRIX_SIZE):
            if not x[row][0].is_valid():
                self.entry_answer.insert(0, f'invalid x[{row+1}]')
                return
            if not x[row][1].is_valid():
                self.entry_answer.insert(0, f'invalid y[{row+1}]')
                return
            if not x[row][2].is_valid():
                self.entry_answer.insert(0, f'invalid z[{row+1}]')
                return
            if not x[row][-1].is_valid():
                self.entry_answer.insert(0, f'invalid n[{row+1}]')
                return

        self.solution = solve_equations(x)
        self.entry_answer.insert(0, get_solution_string(self.solution))

    def switch_fraction_type(self):
        if toggle(self.button_fraction) == "on":
            gv.show_int_above_1 = True
        else:
            gv.show_int_above_1 = False
        if self.solution != gv.no_solution:
            self.entry_answer.delete(0, tk.END)
            self.entry_answer.insert(0, get_solution_string(self.solution))

    def switch_show_steps_mode(self):
        if toggle(self.button_steps) == "on":
            gv.show_steps = True
        else:
            gv.show_steps = False

    def board_key(self, key):
        if key.keycode == 13:
            self.solve()

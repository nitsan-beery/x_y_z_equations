from EquationsWindow import *
from test import *
import global_vars as gv


def run_gui():
    equation_window = EquationsWindow()
    equation_window.window_main.mainloop()


if __name__ == '__main__':
    if gv.test_mode:
        test_matrix()
    else:
        run_gui()

from EquationsWindow import *
from test import *
import global_vars as gv


def run_gui():
    parent = win32gui.GetForegroundWindow()
    equation_window = EquationsWindow(parent)
    equation_window.window_main.focus_get()
    equation_window.window_main.update()
    x = equation_window.window_main.winfo_x()
    y = equation_window.window_main.winfo_y()
    # cause the mouse cursor be on the form - therefore creating <Enter> event to minimize the cmd window
    win32api.SetCursorPos((x+50, y+50))
    equation_window.window_main.mainloop()


if __name__ == '__main__':
    if gv.test_mode:
        test()
    else:
        run_gui()

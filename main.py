from EquationsWindow import *


def test_operator():
    f = Rational("4")
    f = f ** .5
    print(f)


def test_matrix():
    x = [
        [0, 2, 2, 4],
        [0, 5, 0, 3],
        [0, 0, 0, 0]
    ]
    for row in range(0, gv.MATRIX_SIZE):
        for col in range(0, gv.MATRIX_SIZE + 1):
            x[row][col] = Rational(x[row][col])
    t = solve_equations(x)
    print(t)

    y = [
        [1, 2, 3, 4, -10, 4],
        [0, 3, 5, 2, 1, 13],
        [1, 1, 1, 1, 1, 6],
        [2, 3, 0, 1, 0, 7],
        [0, 0, 0, 0, 1, 2]
    ]
    gv.MATRIX_SIZE = 5
    for row in range(0, gv.MATRIX_SIZE):
        for col in range(0, gv.MATRIX_SIZE + 1):
            y[row][col] = Rational(y[row][col])
    t = solve_equations(y)
    print(t)


def run_gui():
    equation_window = EquationsWindow()
    equation_window.window_main.mainloop()


if __name__ == '__main__':
    #test_operator()
    #test_matrix()
    run_gui()

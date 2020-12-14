import random
from EquationsSolver import *


def test_operator():
    f = Rational(0.25)
    print(f)


def test():
    gv.show_steps = False
    gv.SHOW_INT_ABOVE_1 = False

    #test_matrix()
    #test_big_matrix()
    test_operator()


def test_matrix():
    gv.MATRIX_SIZE = 3
    m = [
        [
            [0, 2, 2, 4],
            [0, 5, 0, 3],
            [0, 0, 0, 0]
        ],
        [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12]
        ],
        [
            [1, 2, 2, 4],
            [0, 5, 4, 3],
            [3, 1, 1, 8]
        ],
        [
            [0, 2, 2, 4],
            [0, 1, 1, 1],
            [0, 0, 0, 0]
        ],
        [
            [-1, 2, 2, 4],
            [0, 1.5, 1, 5],
            [3, 0, -5, -10]
        ],
    ]
    r = [
        [
            [infinite_rational, 0, 0],
            [0, 3/5, 0],
            [0, 0, 7/5],
        ],
        [
            [-2, 0, 1],
            [0, 3, -2],
            [0, 0, infinite_rational],
        ],
        [
            [12/5, 0, 0],
            [0, -1/5, 0],
            [0, 0, 1],
        ],
        [
            [no_solution_rational, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        [
            ['20/3', 0, 0],
            [0, '-2/3', 0],
            [0, 0, 6],
        ],
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
    ]
    for i in range(0, len(m)):
        x = m[i]
        rx = r[i]
        for row in range(0, gv.MATRIX_SIZE):
            for col in range(0, gv.MATRIX_SIZE):
                x[row][col] = Rational(x[row][col])
                rx[row][col] = Rational(rx[row][col])
            x[row][-1] = Rational(x[row][-1])
        t = solve_equations(x)
        result = True
        for j in range(0, len(t)):
            if t[j] != r[i][j]:
                result = False
        print(f'{i+1}: {result} -> {get_solution_string(t)}')


def test_big_matrix():
    n = 3
    gv.MATRIX_SIZE = n
    y = []
    for row in range(0, n):
        c = []
        for col in range(0, n):
            c.append(Rational(random.randint(0, 100)))
            if random.randint(0, 1):
                c[-1] *= -1
        c.append(Rational(random.randint(101, 999)))
        y.append(c)
    if not gv.show_steps:
        print_matrix(y)
    t = solve_equations(y)
    print(get_solution_string(t, spaces=2))


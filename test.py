import random
from EquationsSolver import *


def test_operator():
    f = Rational("4")
    f = f ** .5
    print(f)


def test():
    gv.show_steps = False
    gv.SHOW_INT_ABOVE_1 = False

    test_matrix()
    #test_big_matrix()


def test_matrix():
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
        [gv.infinite, '3/5', '7/5'],
        ['-2 + z', '3 - 2z', gv.infinite],
        ['12/5', '-1/5', '1'],
        [gv.no_solution, gv.no_solution, gv.no_solution],
        ['20/3', '-2/3', '6'],
    ]
    for i in range(0, len(m)):
        x = m[i]
        for row in range(0, gv.MATRIX_SIZE):
            for col in range(0, gv.MATRIX_SIZE + 1):
                x[row][col] = Rational(x[row][col])
        t = solve_equations(x)
        result = True
        for j in range(0, len(t)):
            if t[j] != r[i][j]:
                result = False
        print(f'{i+1}: {result} -> {get_solution_string(t)}')


def test_big_matrix():
    n = 50
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


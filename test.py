import random
from Rational import *
from EquationsSolver import *


def test_operator():
    f = Rational("4")
    f = f ** .5
    print(f)


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
        ]
    ]
    r = [
        [gv.infinite, '3/5', '7/5'],
        ['-2 + z', '3 - 2z', gv.infinite],
        ['12/5', '-1/5', '1'],
        [gv.no_solution, gv.no_solution, gv.no_solution]
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


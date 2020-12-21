from EquationsSolver import *
import random


def test():
    test_fraction_matrix()
    #test_operator()
    #test_n_matricies()
    #test_big_matrix()
    #test_fraction_1()


def test_operator():
    f1 = Rational('2/3')
    f2 = Rational(2/3)
    f3 = f1 == f2
    print(f3)


def test_big_matrix():
    n = 100
    solve_rational = True
    show_solution_rational = True
    gv.MATRIX_SIZE = n
    yd = []
    yr = []
    for row in range(0, n):
        cd = []
        cr = []
        for col in range(0, n):
            rnd = random.randint(0, 100)
            cd.append(rnd)
            cr.append(Rational(rnd))
        rnd = random.randint(100, 200)
        cd.append(rnd)
        cr.append(Rational(rnd))
        yd.append(cd)
        yr.append(cr)
    if not gv.show_steps:
        print_matrix(yr)
    t = solve_equations(yd)
    if show_solution_rational:
        for row in range(0, n):
            for col in range(0, n):
                t[row][col] = Rational(t[row][col])
    print(get_solution_string(t, spaces=2))
    if solve_rational:
        t = solve_equations(yr)
        print(get_solution_string(t, spaces=2))


def test_fraction_matrix():
    n = 15
    gv.MATRIX_SIZE = n
    d = []
    r = []
    for row in range(0, n):
        cd = []
        cr = []
        for col in range(0, n):
            #cd.append((row / (col + 1) ** 2) ** 7 - (row * col - 11) ** 6)
            cd.append((row + col) ** 7 - (row - col - 11) ** 6)
            #cd.append(1/(row+1+col))
            cr.append(None)
        cd.append((row ** 2 - row + 5) * 10000)
        #cd.append(row+1)
        cr.append(None)
        d.append(cd)
        r.append(cr)
    for row in range(0, n):
        for col in range(0, n+1):
            r[row][col] = Rational(d[row][col])
    if not gv.show_steps:
        print_matrix(r)
    td = copy_matrix(n, d)
    tr = copy_matrix(n, r)
    td = solve_equations(td)
    print('double:   ' + get_solution_string(td, spaces=2))
    result_d = check_result(n, d, td)
    print(result_d)
    tr = solve_equations(tr)
    print('fraction: ' + get_solution_string(tr, spaces=2))
    result_r = check_result(n, r, tr)
    print(result_r)


def test_fraction_1():
    gv.show_steps = True
    gv.MAX_DIGITS_TO_SHOW_FRACTION = 12
    n = 2
    m = [
        [57, 67, 167, 1],
        [3, 36, 181, 7/11],
        [1, 2, 3, 4],
        [-1, 3, -4, 7],
    ]
    gv.MATRIX_SIZE = n
    d = []
    r = []
    for row in range(0, n):
        cd = []
        cr = []
        for col in range(0, n+1):
            cd.append(m[row][col])
            cr.append(Rational(m[row][col]))
        d.append(cd)
        r.append(cr)
    td = solve_equations(d)
    tr = solve_equations(r)
    print('double:   ' + get_solution_string(td, spaces=2))
    print('fraction: ' + get_solution_string(tr, spaces=2))


def test_n_matricies():
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
            [20/3, 0, 0],
            [0, -2/3, 0],
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


def check_result(n, x, r):
    result = []
    max_digits = 0
    if type(r[0][0]) is Rational:
        for row in range(n):
            if r[row][row] is infinite_rational:
                r[row][row] = Rational(0)
                for col in range(n):
                    f = r[col][row]
                    if len(str(abs(f.numerator))) > max_digits:
                        max_digits = len(str(abs(f.numerator)))
                    if len(str(abs(f.denominator))) > max_digits:
                        max_digits = len(str(abs(f.denominator)))

    for row in range(0, n):
        if type(r[row][row]) is Rational:
            if len(str(r[row][row].numerator)) > max_digits:
                max_digits = len(str(r[row][row].numerator))
            if len(str(r[row][row].denominator)) > max_digits:
                max_digits = len(str(r[row][row].denominator))
        elif len(str(r[row][row])) > max_digits:
            max_digits = len(str(r[row][row]))
        result_row = r[0][0] * x[row][0]
        for col in range(1, n):
            result_row += r[col][col] * x[row][col]
        result_row -= x[row][-1]
        result.append(f'{abs(result_row)}')
    result.append(f'max {max_digits} digits')
    return result


def copy_matrix(n, origin):
    m = []
    for i in range(n):
        m_row = []
        for j in range(n+1):
            m_row.append(origin[i][j])
        m.append(m_row.copy())
    return m

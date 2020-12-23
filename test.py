from EquationsSolver import *
import random


def test():
    #test_operator()
    test_fraction()
    #test_random()


def test_operator():
    f1 = Rational(1234512345123451234512340)
    f2 = Rational(f'{f1}/4')
    f3 = f2 * 4
    f4 = f1 * f3
    f5 = f4 / f3
    print(f4)


def test_fraction():
    n = 25
    gv.MATRIX_SIZE = n
    dx = []
    rx = []
    for row in range(0, n):
        cd = []
        cr = []
        for col in range(0, n):
            #r = Rational(f'1/{row+1+col}')
            #r = Rational(f'{row}/{(col + 1) ** 2}') ** 7 - (row * col - 11) ** 6
            r = Rational((row + col) ** 7 - (row - col - 11) ** 6)
            d = r.numerator/r.denominator
            cr.append(r)
            cd.append(d)
        #r = Rational(row+1)
        r = Rational((row ** 2 - row + 5) * 10000)
        d = r.numerator/r.denominator
        cr.append(r)
        cd.append(d)

        dx.append(cd)
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(dx, rx)


def test_random():
    n = 10
    gv.MATRIX_SIZE = n
    dx = []
    rx = []
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
        dx.append(cd)
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    td = copy_matrix(dx)
    tr = copy_matrix(rx)
    test_double_vs_random_matrix(td, tr)


def test_double_vs_random_matrix(dx, rx):
    td = copy_matrix(dx)
    tr = copy_matrix(rx)
    td = solve_equations(td)
    print('double:   ' + get_solution_string(td, spaces=2))
    result_d = check_result(dx, td)
    print(result_d)
    tr = solve_equations(tr)
    print('fraction: ' + get_solution_string(tr, spaces=2))
    result_r = check_result(rx, tr)
    print(result_r)


def check_result(x, r):
    n = len(r)
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
            f1 = r[col][col]
            f2 = x[row][col]
            add = f1 * f2
            result_row += r[col][col] * x[row][col]
        result_row -= x[row][-1]
        result.append(f'{abs(result_row)}')
    result.append(f'max {max_digits} digits')
    return result


def copy_matrix(origin):
    n = len(origin)
    m = []
    for i in range(n):
        m_row = []
        for j in range(n+1):
            m_row.append(origin[i][j])
        m.append(m_row.copy())
    return m



from EquationsSolver import *
import random

show_steps = False
round_int = True


def test():
    gv.show_steps = show_steps
    gv.ROUND_INT = round_int
    if round_int:
        gv.MAX_DIGITS_TO_ALLOW_INT = gv.MAX_DIGITS_IN_FLOAT

    #test_operator()
    test_fraction()
    #test_random()


def test_operator():
    digits = 149
    n = 5
    n1 = int(n * 10 ** (digits-len(str(n))))
    n2 = n1 + 12321
    f1 = Rational(n1)
    f2 = Rational(n2)
    f3 = f1 + f2
    f4 = f2 / 10
    f5 = f4 * 5
    f6 = f5 / f4
    print(f2)


def test_fraction():
    n = 30
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n):
            r = Rational(f'1/{row+101+col}')
            #r = Rational(f'{row}/{(col + 1) ** 2}') ** 7 - (row * col - 11) ** 6
            #r = Rational((row + col) ** 30 - (row - col - 11) ** 6)
            cr.append(r)
        r = Rational(row+1)
        #r = Rational((row ** 2 - row + 5) * 10000)
        cr.append(r)
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx)


def test_random():
    n = 5
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n):
            rnd = random.randint(0, 100)
            cr.append(Rational(rnd))
        rnd = random.randint(100, 200)
        cr.append(Rational(rnd))
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx)


def test_double_vs_random_matrix(rx):
    dx = copy_matrix(rx)
    convert_matrix_to_float(dx)
    td = copy_matrix(dx)
    tr = copy_matrix(rx)
    if gv.err is not None:
        if gv.ROUND_INT:
            gv.err += ' -> change ROUND_INT to False'
        print('exception before solving - ' + gv.err)
        gv.err = None
        return
    if gv.is_rational_converted_to_float:
        print('before solving - rational converted to float')
        gv.is_rational_converted_to_float = False
    td = solve_equations(td)
    print('double:\n' + get_solution_string(td, spaces=2))
    result_d = check_result(dx, td)
    dev_d = print_result(result_d)
    tr = solve_equations(tr)
    if gv.err is not None:
        print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('exception while solving - ' + gv.err)
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
        gv.err = None
    max_digits = gv.rational_largest_digits
    print('\nfraction:')
    if gv.is_rational_converted_to_float:
        print('----------------------------------------------')
        print('while solving - rational converted to float')
        print('----------------------------------------------')
        gv.is_rational_converted_to_float = False
    print(get_solution_string(tr, spaces=2))
    result_r = check_result(rx, tr)
    if gv.err is not None:
        print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('exception while solving - ' + gv.err)
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    if gv.is_rational_converted_to_float:
        print('----------------------------------------------')
        print('while checking result - rational converted to float')
        print('----------------------------------------------')
    dev_r = print_result(result_r)
    if dev_r == 0:
        if dev_d == 0:
            str_dev = '0'
        else:
            str_dev = 'inf'
    elif dev_d != 0:
        str_dev = dev_r / dev_d
    print(f'\nr_deviation / d_deviation: {str_dev}\nmax rational digits: {max_digits}')


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
        result_row = x[row][0] * r[0][0]
        for col in range(1, n):
            f1 = x[row][col]
            f2 = r[col][col]
            add = f1 * f2
            result_row += add
        result_row -= x[row][-1]
        result.append(abs(result_row))
    result.append(max_digits)
    return result


def print_result(r):
    dev = r[0]
    dev_vector = f'{r[0]}   '
    for i in range(1, len(r) - 1):
        dev += r[i]
        dev_vector += f'{r[i]}   '
    print('row deviation: ' + dev_vector)
    dev /= len(r)
    print(f'average deviation: {dev}')
    return dev


def copy_matrix(origin):
    n = len(origin)
    m = []
    for i in range(n):
        m_row = []
        for j in range(n+1):
            m_row.append(origin[i][j])
        m.append(m_row.copy())
    return m



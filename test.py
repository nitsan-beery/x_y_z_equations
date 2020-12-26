from EquationsSolver import *
import random

show_steps = False
round_int = False


def test():
    gv.show_steps = show_steps
    gv.ROUND_INT = round_int
    if round_int:
        gv.MAX_DIGITS_TO_ALLOW_INT = gv.MAX_DIGITS_IN_FLOAT

    test_operator()
    #test_fraction()
    #test_random()
    #test_inf_and_no_solution()


def test_operator():
    inf = float('inf')
    s_fail = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n' \
             ' check   check   check   check   check\n' \
             'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    m_no_zero = [(inf, inf), (1, inf), (inf, 1), (1, 1)]
    m_with_zero = [(0, inf), (inf, 0), (0, 1), (1, 0)]
    for pair in m_no_zero:
        f1 = pair[0]
        f2 = pair[1]
        success = test_all_operators(f1, f2)
        if not success:
            print(s_fail)
        f1 = -f1
        success = test_all_operators(f1, f2)
        if not success:
            print(s_fail)
        f1 = -f1
        f2 = -f2
        success = test_all_operators(f1, f2)
        if not success:
            print(s_fail)
        f1 = -f1
        success = test_all_operators(f1, f2)
        if not success:
            print(s_fail)
    for pair in m_with_zero:
        f1 = pair[0]
        f2 = pair[1]
        success = test_all_operators(f1, f2)
        if not success:
            print(s_fail)
        if f1 == 0:
            f2 = -f2
        else:
            f1 = -f1
        success = test_all_operators(f1, f2)
        if not success:
            print(s_fail)
    success = test_all_operators(0, 0)
    if not success:
        print(s_fail)


def test_all_operators(f1, f2):
    r1 = Rational(f1)
    r2 = Rational(f2)
    gt = r1 > r2
    ge = r1 >= r2
    lt = r1 < r2
    le = r1 <= r2
    eq = r1 == r2
    f_plus = f1+f2
    r_plus = r1+r2
    f_minus = f1-f2
    r_minus = r1-r2
    f_mul = f1*f2
    r_mul = r1*r2
    if f2 != 0:
        f_div = f1/f2
    else:
        f_div = float('nan')
    r_div = r1/r2
    t_plus = f_plus == r_plus
    t_minus = f_minus == r_minus
    t_mul = f_mul == r_mul
    t_div = f_div == r_div
    t_eq = eq == (f1 == f2)
    t_gt = gt == (f1 > f2)
    t_ge = ge == (f1 >= f2)
    t_lt = lt == (f1 < f2)
    t_le = le == (f1 <= f2)
    print('')
    print(f'r1: {r1}   r2: {r2}')
    print(f'+   float: {f_plus}   rational: {r_plus}   | {t_plus}')
    print(f'-   float: {f_minus}   rational: {r_minus}   | {t_minus}')
    print(f'*   float: {f_mul}   rational: {r_mul}   | {t_mul}')
    print(f'/   float: {f_div}   rational: {r_div}   | {t_div}')
    print(f'r1 == r2: {eq}   | {t_eq}')
    print(f'r1 > r2: {gt}   | {t_gt}')
    print(f'r1 >= r2: {ge}   | {t_ge}')
    print(f'r1 < r2: {lt}   | {t_lt}')
    print(f'r1 <= r2: {le}   | {t_le}')

    if gv.is_rational_converted_to_float:
        print('rational_converted_to_float')
    print(f'err: {gv.err}')

    return t_plus and t_minus and t_mul and t_div and t_eq and t_gt and t_ge and t_lt and t_le


def test_fraction():
    n = 10
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n):
            r = Rational(f'1/{row+100000001+col}')
            #r = Rational(f'{row}/{(col + 1) ** 2}') ** 7 - (row * col - 11) ** 6
            #r = Rational((row + col) ** 15 - (row - col - 11) ** 6)
            cr.append(r)
        #r = Rational(row+1)
        r = Rational((row ** 2 - row + 5) * 10000)
        cr.append(r)
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx)


def test_random():
    n = 30
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n+1):
            rnd = random.randint(0, 10000)
            cr.append(Rational(rnd))
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx)


def test_inf_and_no_solution():
    n = 2
    gv.MATRIX_SIZE = n
    print('\nTest - no solution')
    rx = [
        [1, 1, 1],
        [1, 1, 2]
    ]
    convert_matrix_to_rational(rx)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx)
    print('\nTest - infinite solution')
    rx = [
        [1, 1, 1],
        [0, 0, 0]
    ]
    convert_matrix_to_rational(rx)
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
#    gv.show_steps = True
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
    dev_r = print_result(result_r)
    r_d_dev = 'inf'
    if dev_r == 0:
        if dev_d == 0:
            r_d_dev = '0'
        else:
            r_d_dev = 'inf'
    elif dev_d is not gv.no_solution and dev_d != 0:
        r_d_dev = float(dev_r / dev_d)
    print(f'\nr_deviation / d_deviation: {r_d_dev}\nmax rational digits: {max_digits}')


def check_result(x, r):
    n = len(r)
    result = []
    max_digits = 0
    if r[0][0] == Rational(gv.invalid_rational):
        return [gv.no_solution]
    for row in range(n):
        if r[row][row] == Rational(gv.inf_rational):
            r[row][row] = 0

    for row in range(0, n):
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
    if dev is gv.no_solution:
        return dev
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


def convert_matrix_to_float(x):
    n = len(x)
    for row in range(n):
        for col in range(n+1):
            if x[row][col].denominator != 0:
                x[row][col] = x[row][col].numerator / x[row][col].denominator


def convert_matrix_to_rational(x):
    n = len(x)
    for row in range(n):
        for col in range(n+1):
            x[row][col] = Rational(x[row][col])


def get_none_matrix(n):
    m = []
    row_m = []
    for col in range(n + 1):
        row_m.append(None)
    for row in range(n):
        m.append(row_m)
    return m

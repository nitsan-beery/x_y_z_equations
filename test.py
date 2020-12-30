from EquationsSolver import *
import random
import time

show_steps = False
round_int = False


def test():
    gv.show_steps = show_steps
    gv.ROUND_INT = round_int
    if round_int:
        gv.MAX_DIGITS_IN_RATIONAL = gv.MAX_DIGITS_IN_FLOAT

    #test_general()
    #test_operator()
    #test_periodic()
    #test_fraction(20, count_down=False)
    test_random(10, count_down=False)
    #test_inf_and_no_solution()


def test_general():
    n = 73040216269692243
    n = 1000000000000002
    r = Rational(f'{n}/{d}')


def test_fraction(n=11, count_down=False):
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n):
            r = Rational(f'1/{row+1000+col}')
            #r = Rational(f'{row}/{(col + 1) ** 2}') ** 7 - (row * col - 11) ** 6
            #r = Rational((row + col) ** 15 - (row - col - 11) ** 6)
            cr.append(r)
        #r = Rational(row+1)
        r = Rational((row ** 2 - row + 5) * 10000)
        cr.append(r)
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    #test_n_vs_n_minus_one_steps(rx)
    test_double_vs_random_matrix(rx, count_down)


def test_random(n=10, count_down=False):
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n+1):
            rnd = random.randint(0, 10000000)
            cr.append(Rational(rnd))
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_random_matrix(rx, count_down)


def test_periodic():
    min_n = 2
    max_n = 1000
    dif = max_n - min_n
    float_count = 0
    for i in range(min_n, max_n):
        f = 3/i
        r = Rational(f)
        if type(r.numerator) is float:
            float_count += 1
            print(f'1/{i}   {r}')
    print(f'\n{dif-float_count}/{dif} = {1-(float_count/(max_n-min_n))}')


def test_operator():
    print_each_result = False
    precision = 10 ** -9
    inf = float('inf')
    big_f = 10 ** (gv.MAX_DIGITS_IN_FLOAT + 10)
    big_i = 10 ** (gv.MAX_DIGITS_IN_RATIONAL + 10)
    gv.ROUND_INT = False
    s_fail = '\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n' \
             '                     fail     fail     fail     fail     fail    fail     fail\n' \
             'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    m_no_zero = [(inf, inf), (3, inf), (inf, 5), (1/53, 3/911), (big_f, 3), (3, big_f), (big_i, 7), (7, big_i)]
    m_with_zero = [(0, inf), (inf, 0), (0, 11), (11, 0)]
    for pair in m_no_zero:
        f1 = pair[0]
        f2 = pair[1]
        try:
            f1 = float(f1)
        except OverflowError:
            f1 = float('inf')
        try:
            f2 = float(f2)
        except OverflowError:
            f2 = float('inf')
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
        f1 = -f1
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
        f1 = -f1
        f2 = -f2
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
        f1 = -f1
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
    for pair in m_with_zero:
        f1 = pair[0]
        f2 = pair[1]
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            test_all_operators(f1, f2, True, precision)
            print(s_fail)
            return
        if f1 == 0:
            f2 = -f2
        else:
            f1 = -f1
        success = test_all_operators(f1, f2, print_each_result, precision)
        if not success:
            print(s_fail)
            test_all_operators(f1, f2, True, precision)
            return
    f1 = 0
    f2 = 0
    success = test_all_operators(f1, f2, print_each_result, precision)
    if not success:
        print(s_fail)
        test_all_operators(f1, f2, True, precision)
        return
    print('\nSUCCESS')


def test_all_operators(f1, f2, show_result=False, precision=0):
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
    try:
        f_div = f1/f2
    except ZeroDivisionError:
        f_div = float('nan')
    r_div = r1/r2
    t_plus = f_plus == float(r_plus) or (str(f_plus).lower() == 'nan' and not r_plus.is_valid()) or abs(f_plus - float(r_plus)) < precision
    t_minus = f_minus == float(r_minus) or (str(f_minus).lower() == 'nan' and not r_minus.is_valid()) or abs(f_minus - float(r_minus)) < precision
    t_mul = f_mul == float(r_mul) or (str(f_mul).lower() == 'nan' and not r_mul.is_valid()) or abs(f_mul - float(r_mul)) < precision
    t_div = (f_div == float(r_div)) or (str(f_div).lower() == 'nan' and not r_div.is_valid()) or abs(f_div - float(r_div)) < precision
    t_eq = eq == (f1 == f2)
    t_gt = gt == (f1 > f2)
    t_ge = ge == (f1 >= f2)
    t_lt = lt == (f1 < f2)
    t_le = le == (f1 <= f2)
    if show_result:
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
        if gv.err is not None:
            print(f'{r1}   {r2}   err: {gv.err}')
            gv.err = None
    if gv.numerator_converted_to_float:
        print(f'{r1}   {r2}   rational_converted_to_float')
        gv.numerator_converted_to_float = False

    return t_plus and t_minus and t_mul and t_div and t_eq and t_gt and t_ge and t_lt and t_le


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


def test_n_vs_n_minus_one_steps(rx):
    gv.MATRIX_SIZE = len(rx)
    r1 = copy_matrix(rx)
    for row in range(len(rx)):
        r1[row][-2] = rx[row][-1]
        r1[row].pop(-1)
    r1.pop(-1)
    gv.MATRIX_SIZE -= 1
    r1 = solve_matrix(r1, True)
    r1_steps = gv.step_by_step_matrix
    gv.step_by_step_matrix = []
    gv.MATRIX_SIZE += 1
    rx = solve_matrix(rx, True)
    rx_steps = gv.step_by_step_matrix
    for i in range(len(r1_steps)):
        m1 = r1_steps[i]
        m2 = rx_steps[i]
        print(f'{i}:')
        print_matrix(m1)
        print_matrix(m2)
        if not is_step_matrices_equal(m1, m2):
            print('fail')
    print('success')


def test_double_vs_random_matrix(rx, count_down=False):
    dx = copy_matrix(rx)
    convert_matrix_to_float(dx)
    td = copy_matrix(dx)
    tr = copy_matrix(rx)
    if gv.err is not None:
        if gv.ROUND_INT:
            gv.err += ' -> change ROUND_INT to False'
        print_exception(gv.err, gv.exception_type_notice)
        gv.err = None
        return
    if gv.numerator_converted_to_float:
        print_exception('before solving - rational converted to float', gv.exception_type_notice)
        gv.is_rational_converted_to_float = False
    start_time = time.perf_counter()
    td = solve_matrix(td)
    end_time = time.perf_counter()
    time_d = end_time - start_time
    print('double:\n' + get_solution_string(td, spaces=2))
    result_d = check_result(dx, td)
    dev_d = print_result(result_d)
    print(f'time: {time_d} sec')
    print('\nfraction:')
    start_time = time.perf_counter()
    tr = solve_matrix(tr, count_down, False)
    end_time = time.perf_counter()
    time_r = end_time - start_time
    if gv.err is not None:
        print_exception(gv.err)
        gv.err = None
    max_digits = gv.rational_largest_digits
    if gv.numerator_converted_to_float:
        print_exception('while solving - rational converted to float', gv.exception_type_notice)
        gv.is_rational_converted_to_float = False
    print(get_solution_string(tr, spaces=2))
    result_r = check_result(rx, tr)
    if gv.err is not None:
        print_exception('while solving - ' + gv.err)
        gv.err = None
    dev_r = print_result(result_r)
    print(f'time: {time_r} sec')
    r_d_dev = 'inf'
    if dev_r == 0:
        if dev_d == 0:
            r_d_dev = '0'
        else:
            r_d_dev = 'inf'
    elif dev_d is not gv.no_solution and dev_d != 0:
        r_d_dev = float(dev_r / dev_d)
    print(f'\nr_deviation / d_deviation: {r_d_dev}')
    print(f'r_time / d_time: {time_r / time_d}')
    print(f'max rational digits: {max_digits}\n')


def print_exception(msg=gv.unknown_exception, ex_type=gv.exception_type_warning):
    line = 'oooooooooooooooooooooooooooooooooo'
    if ex_type == gv.exception_type_warning:
        print('\n')
        line = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    elif ex_type == gv.exception_type_notice:
        line = '---------------------------------------------'
    print(line)
    print(msg)
    print(line)
    if ex_type == gv.exception_type_warning:
        print('\n')


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
    print(f'average deviation: {float(dev)}')
    return dev


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


def is_step_matrices_equal(m1, m2):
    n = len(m1)
    for row in range(n):
        for col in range(n):
            if m1[row][col] != m2[row][col]:
                return False
        if m1[row][-1] != m2[row][-1]:
            return False
    return True


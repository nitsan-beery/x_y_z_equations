from EquationsSolver import *
import random
import time
from fractions import Fraction


def test():
    #test_general()
    #test_operator(print_each_result=True)
    #test_fraction(50)
    #test_random(15)
    #test_inf_and_no_solution()
    test_periodic()


def test_general():
    n = 1.0
    d = 0.0
    r = Fraction(f'{n}/{d}')
    print(r)


def test_fraction(n=11, count_down=False):
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n):
            r = Fraction(f'1/{row+1000+col}')
            #r = Fraction(f'{row}/{(col + 1) ** 2}') ** 7 - (row * col - 11) ** 6
            #r = Fraction((row + col) ** 15 - (row - col - 11) ** 6)
            cr.append(r)
        #r = Fraction(row+1)
        r = Fraction((row ** 2 - row + 5) * 10000)
        cr.append(r)
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    #test_n_vs_n_minus_one_steps(rx)
    test_double_vs_fraction_matrix(rx)


def test_random(n=10, count_down=False):
    gv.MATRIX_SIZE = n
    rx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n+1):
            rnd = random.randint(0, 10000000)
            cr.append(Fraction(rnd))
        rx.append(cr)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_fraction_matrix(rx)


def test_periodic():
    min_n = 2
    max_n = 100
    dif = max_n - min_n
    for n in range(1, 2):
        float_count = 0
        for i in range(min_n, max_n):
            f = n/i
            r = Fraction(f)
            print(r)
            '''
            if type(r.numerator) is float:
                float_count += 1
#                print(f'{n}/{i}   {r}')
        print(f'{n}/x:   {dif-float_count}/{dif} = {1-(float_count/(max_n-min_n))}')
        '''


def test_inf_and_no_solution():
    n = 2
    gv.MATRIX_SIZE = n
    print('\nTest - no solution')
    rx = [
        [1, 1, 1],
        [1, 1, 2]
    ]
    convert_matrix_to_fraction(rx)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_fraction_matrix(rx)
    print('\nTest - infinite solution')
    rx = [
        [1, 1, 1],
        [0, 0, 0]
    ]
    convert_matrix_to_fraction(rx)
    if not gv.show_steps:
        print_matrix(rx)
    test_double_vs_fraction_matrix(rx)


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


def test_double_vs_fraction_matrix(rx):
    dx = copy_matrix(rx)
    convert_matrix_to_float(dx)
    td = copy_matrix(dx)
    tr = copy_matrix(rx)
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
    tr = solve_matrix(tr, get_step_by_step_matrix=False)
    end_time = time.perf_counter()
    time_r = end_time - start_time
    print(get_solution_string(tr, spaces=2))
    result_r = check_result(rx, tr)
    dev_r = print_result(result_r)
    print(f'time: {time_r} sec')
    d_r_dev = 'inf'
    if dev_r == 0:
        if dev_d == 0:
            d_r_dev = '1'
        else:
            d_r_dev = 'inf'
    elif dev_r is gv.no_solution:
        if dev_d is gv.no_solution:
            d_r_dev = '1'
        else:
            d_r_dev = '-inf'
    elif dev_d is not gv.no_solution:
        d_r_dev = float(dev_d / dev_r)
    print(f'\nd_deviation / r_deviation: {d_r_dev}')
    print(f'r_time / d_time: {time_r / time_d}')


def check_result(x, r):
    n = len(r)
    result = []
    max_digits = 0
    if r[0][0] == gv.no_solution:
        return [gv.no_solution]
    for row in range(n):
        if r[row][row] == gv.infinite:
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


def convert_matrix_to_fraction(x):
    n = len(x)
    for row in range(n):
        for col in range(n+1):
            x[row][col] = Fraction(x[row][col].numerator, x[row][col].denominator)


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


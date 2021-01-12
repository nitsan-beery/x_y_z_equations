from EquationsSolver import *
import random
import time
from fractions import Fraction


def test():
    gv.show_fraction = gv.fraction_type_proper

    #test_general()
    #test_operator(print_each_result=True)
    #test_fraction(100, count_down=True)
    test_random(4, count_down=False)
    #test_inf_and_no_solution()
    #test_periodic()


def test_general():
    x = [
        [-17, 43, -92, 21, -80],
        [46, 81, -86, 100, -47],
        [80, 15, -81, 48, -9],
        [-100, 92, 86, -89, 48]
    ]
    convert_matrix_to_fraction(x)
    print_matrix(x)


def test_fraction(n=11, count_down=False):
    gv.MATRIX_SIZE = n
    mx = []
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
        mx.append(cr)
    if not gv.show_steps:
        print_matrix(mx)
    #test_n_vs_n_minus_one_steps(mx)
    test_float_vs_fraction_matrix(mx, count_down)


def test_random(n=10, count_down=False):
    gv.MATRIX_SIZE = n
    mx = []
    for row in range(0, n):
        cr = []
        for col in range(0, n+1):
            rnd = random.randint(-100, 100)
            cr.append(Fraction(rnd))
        mx.append(cr)
    if not gv.show_steps:
        print_matrix(mx)
    test_float_vs_fraction_matrix(mx, count_down)


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
    mx = [
        [1, 1, 1],
        [1, 1, 2]
    ]
    convert_matrix_to_fraction(mx)
    if not gv.show_steps:
        print_matrix(mx)
    test_float_vs_fraction_matrix(mx)
    print('\nTest - infinite solution')
    mx = [
        [1, 1, 1],
        [0, 0, 0]
    ]
    convert_matrix_to_fraction(mx)
    if not gv.show_steps:
        print_matrix(mx)
    test_float_vs_fraction_matrix(mx)


def test_n_vs_n_minus_one_steps(mx):
    gv.MATRIX_SIZE = len(mx)
    r1 = copy_matrix(mx)
    for row in range(len(mx)):
        r1[row][-2] = mx[row][-1]
        r1[row].pop(-1)
    r1.pop(-1)
    gv.MATRIX_SIZE -= 1
    r1 = solve_matrix(r1, True)
    r1_steps = gv.step_by_step_matrix
    gv.step_by_step_matrix = []
    gv.MATRIX_SIZE += 1
    mx = solve_matrix(mx, True)
    mx_steps = gv.step_by_step_matrix
    for i in range(len(r1_steps)):
        m1 = r1_steps[i]
        m2 = mx_steps[i]
        print(f'{i}:')
        print_matrix(m1)
        print_matrix(m2)
        if not is_step_matrices_equal(m1, m2):
            print('fail')
    print('success')


def test_float_vs_fraction_matrix(mx, count_down=False):
    dx = copy_matrix(mx)
    convert_matrix_to_float(dx)
    td = copy_matrix(dx)
    tr = copy_matrix(mx)
    start_time = time.perf_counter()
    td = solve_matrix(td)
    end_time = time.perf_counter()
    time_d = end_time - start_time
    print('float:\n' + get_solution_string(td, spaces=2))
    result_d = check_result(dx, td)
    dev_d = print_result(result_d)
    print(f'time: {time_d} sec')
    print('\nFraction:')
    start_time = time.perf_counter()
    tr = solve_matrix(tr, count_down=count_down, get_step_by_step_matrix=False)
    max_digits = 0
    for row in range(len(tr)):
        if type(tr[row][row]) is Fraction:
            if len(str(tr[row][row].numerator)) > max_digits:
                max_digits = len(str(tr[row][row].numerator))
            if len(str(tr[row][row].denominator)) > max_digits:
                max_digits = len(str(tr[row][row].denominator))
    end_time = time.perf_counter()
    time_r = end_time - start_time
    print(get_solution_string(tr, spaces=2))
    result_r = check_result(mx, tr)
    dev_r = print_result(result_r)
    print(f'time: {time_r} sec')
    f_F_dev = 'inf'
    if dev_r == 0:
        if dev_d == 0:
            f_F_dev = '1'
        else:
            f_F_dev = 'inf'
    elif dev_r is gv.no_solution:
        if dev_d is gv.no_solution:
            f_F_dev = '1'
        else:
            f_F_dev = '-inf'
    elif dev_d is not gv.no_solution:
        f_F_dev = float(dev_d / dev_r)
    print(f'\nfloat deviation / Fraction deviation: {f_F_dev}')
    print(f'Fraction time / float time: {time_r / time_d}')
    print(f'max digits: {max_digits}')


def check_result(x, r):
    n = len(r)
    result = []
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
        # percentage deviation
        ref = x[row][-1]
        if ref == 0:
            ref = 10 ** -gv.PRECISION
        result_row = 100 * result_row / ref
        result.append(abs(result_row))
    return result


def print_result(r):
    dev = r[0]
    if dev is gv.no_solution:
        return dev
    dev_vector = f'{r[0]}   '
    for i in range(1, len(r) - 1):
        dev += r[i]
        dev_vector += f'{r[i]}   '
    print('row deviation (%): ' + dev_vector)
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
            x[row][col] = convert_float_to_fraction(x[row][col])


def convert_float_to_fraction(f):
    if type(f) is not float:
        return Fraction(f)
    n, d = check_periodic(f)
    if d == 1:
        return Fraction(n)
    return Fraction(n, d)


def check_periodic(exp):
    for n in range(1, gv.MAX_N_FOR_PERIODIC_CHECK):
        if exp * n == int(exp * n):
            return int(exp * n), int(n)
    return exp, 1


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


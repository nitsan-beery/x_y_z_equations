import global_vars as gv
from fractions import Fraction


def solve_matrix(x, show_steps_improper=True, count_down=False, get_step_by_step_matrix=False):
    matrix_size = len(x)
    if gv.show_steps:
        print('\n==========================\n')
    if count_down:
        print('count down - ', end='')
    for col in range(0, matrix_size):
        if gv.show_steps:
            print_matrix(x, show_steps_improper)
        ref = col
        if x[ref][ref] == 0:
            r = find_non_zero_row(x, ref)
            # can't find row
            if r < 0:
                continue
            else:
                replace_rows(x, ref, r)
                if gv.show_steps:
                    print_matrix(x, show_steps_improper)
        ref_value = x[ref][ref]
        for c in range(ref, matrix_size + 1):
            x[ref][c] /= ref_value
        for row in range(0, matrix_size):
            if x[row][ref] == 0 or row == ref:
                continue
            row_ratio = x[row][ref]
            for c in range(ref, matrix_size+1):
                dif = x[ref][c] * row_ratio
                x[row][c] -= dif
        if get_step_by_step_matrix:
            tmp_x = copy_matrix(x)
            gv.step_by_step_matrix.append(tmp_x)
        if count_down:
            print(f'{matrix_size - col} ', end='')
    if gv.show_steps:
        print_matrix(x, show_steps_improper)
    if count_down:
        print('')

    # arrange results for each x[i]
    result_array = []
    xi_result_vector = []
    for i in range(0, matrix_size):
        xi_result_vector.append(0)
    for i in range(0, matrix_size):
        result_array.append(xi_result_vector.copy())

    for row in range(0, matrix_size):
        if x[row][row] == 0:
            if x[row][-1] != 0:
                result_array[0][0] = gv.no_solution
                break
            result_array[row][row] = gv.infinite
        else:
            result_array[row][row] = x[row][-1]
            for col in range(0, matrix_size):
                if col == row:
                    continue
                if x[row][col] != 0:
                    result_array[row][col] = -x[row][col]

    return result_array


def find_non_zero_row(x, n):
    matrix_size = len(x)
    for r in range(n + 1, matrix_size):
        if x[r][n] != 0:
            return r
    for r in range(0, n):
        if x[r][n] != 0 and x[r][r] == 0:
            return r
    return -1


def replace_rows(x, m, n):
    matrix_size = len(x)
    for col in range(0, matrix_size+1):
        x[m][col], x[n][col] = x[n][col], x[m][col]


def get_name_x(matrix_size=gv.MATRIX_SIZE):
    name_x = ['x', 'y', 'z']
    if matrix_size > 3:
        name_x = []
        for i in range(0, matrix_size):
            name_x.append(f'x[{i+1}]')
    return name_x


def get_solution_string(result_array, spaces=5):
    matrix_size = len(result_array)
    if result_array[0][0] == gv.no_solution:
        return gv.no_solution
    name_x = get_name_x(matrix_size)
    result = ''
    space = ''
    for i in range(0, spaces):
        space += ' '
    for i in range(0, matrix_size):
        if result_array[i][i] == gv.infinite:
            result_i = gv.infinite
        else:
            result_i = get_fraction_str(result_array[i][i])
            for c in range(0, len(result_array[i])):
                if c == i:
                    continue
                if result_array[i][c] != 0:
                    if result_array[i][c] < 0:
                        sign = '-'
                    else:
                        sign = '+'
                    num_i = abs(result_array[i][c])
                    if num_i == 1:
                        str_num_i = ''
                    else:
                        str_num_i = get_fraction_str(num_i)
                    result_i += f' {sign} {str_num_i}{name_x[c]}'
        result += f'{name_x[i]} = {result_i}' + space
    return result


def get_fraction_str(f):
    if type(f) is not Fraction:
        return f'{f}'
    if gv.show_fraction == gv.fraction_type_float:
        return f'{f.numerator / f.denominator}'
    if gv.show_fraction == gv.fraction_type_proper and abs(f) > 1 and f.denominator != 1:
        return f'{f.numerator//f.denominator}({f.numerator % f.denominator}/{f.denominator})'
    return f'{f}'


def print_matrix(x, f_type_only_improper=True):
    n = len(x)
    tmp_state = gv.show_fraction
    if f_type_only_improper:
        gv.show_fraction = gv.fraction_type_improper
    for row in range(0, n):
        str_row = ''
        for col in range(0, n):
            str_row += get_fraction_str(x[row][col]) + ' '
        str_row += '   ' + get_fraction_str(x[row][-1])
        print(str_row)
    print('--------------------------')
    gv.show_fraction = tmp_state


def copy_matrix(origin):
    n = len(origin)
    m = []
    for i in range(n):
        m_row = []
        for j in range(n+1):
            m_row.append(origin[i][j])
        m.append(m_row.copy())
    return m



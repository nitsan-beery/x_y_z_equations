from Rational import *
import global_vars as gv


def solve_equations(x):
    if gv.show_steps:
        print('\n==========================\n')
    for col in range(0, gv.MATRIX_SIZE):
        if gv.show_steps:
            print_matrix(x)
        ref = col
        if x[ref][ref] == 0:
            r = find_non_zero_row(x, ref)
            # can't find row
            if r < 0:
                continue
            else:
                replace_rows(x, ref, r)
                if gv.show_steps:
                    print_matrix(x)
        ref_value = x[ref][ref]
        for c in range(ref, gv.MATRIX_SIZE + 1):
            x[ref][c] /= ref_value
        for row in range(0, gv.MATRIX_SIZE):
            if x[row][ref] == 0 or row == ref:
                continue
            row_ratio = x[row][ref]
            for c in range(ref, gv.MATRIX_SIZE+1):
                x[row][c] -= x[ref][c] * row_ratio
    if gv.show_steps:
        print_matrix(x)

    # arrange results for each x[i]
    result_array = []
    xi_result_vector = []
    for i in range(0, gv.MATRIX_SIZE):
        xi_result_vector.append(Rational(0))
    for i in range(0, gv.MATRIX_SIZE):
        result_array.append(xi_result_vector.copy())

    for row in range(0, gv.MATRIX_SIZE):
        if x[row][row] == 0:
            if x[row][-1] != 0:
                result_array[0][0] = no_solution_rational
                break
            result_array[row][row] = infinite_rational
        else:
            result_array[row][row] = x[row][-1]
            for col in range(0, gv.MATRIX_SIZE):
                if col == row:
                    continue
                if x[row][col] != 0:
                    result_array[row][col] = -x[row][col]

    return result_array


def find_non_zero_row(x, n):
    for r in range(n + 1, gv.MATRIX_SIZE):
        if x[r][n] != 0:
            return r
    for r in range(0, n):
        if x[r][n] != 0 and x[r][r] == 0:
            return r
    return -1


def replace_rows(x, m, n):
    for col in range(0, gv.MATRIX_SIZE+1):
        x[m][col], x[n][col] = x[n][col], x[m][col]


def get_name_x():
    name_x = ['x', 'y', 'z']
    if gv.MATRIX_SIZE > 3:
        name_x = []
        for i in range(0, gv.MATRIX_SIZE):
            name_x.append(f'x[{i+1}]')
    return name_x


def get_solution_string(result_array, spaces=5):
    if result_array[0][0] == no_solution_rational:
        return gv.no_solution
    name_x = get_name_x()
    result = ''
    space = ''
    for i in range(0, spaces):
        space += ' '
    for i in range(0, gv.MATRIX_SIZE):
        result_i = ''
        if result_array[i][i] == infinite_rational:
            result_i = gv.infinite
        else:
            result_i = f'{result_array[i][i]}'
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
                        str_num_i = str(num_i)
                    result_i += f' {sign} {str_num_i}{name_x[c]}'
        result += f'{name_x[i]} = {result_i}' + space
    return result


def print_matrix(x):
    tmp_state = gv.SHOW_INT_ABOVE_1
    gv.SHOW_INT_ABOVE_1 = False
    for row in range(0, gv.MATRIX_SIZE):
        str_row = ''
        for col in range(0, gv.MATRIX_SIZE):
            str_row += f'{x[row][col]} '
        str_row += f'   {x[row][-1]}'
        print(str_row)
    print('--------------------------')
    gv.SHOW_INT_ABOVE_1 = tmp_state

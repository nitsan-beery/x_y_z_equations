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

    # arrange result by order (x y z)
    str_result_array = []
    no_solution_str_array = []
    name_x = get_name_x()
    for i in range(0, gv.MATRIX_SIZE):
        str_result_array.append('')
        no_solution_str_array.append(gv.no_solution)
    for row in range(0, gv.MATRIX_SIZE):
        if x[row][row] == 0:
            if x[row][-1] != 0:
                return no_solution_str_array
            str_result_array[row] = gv.infinite
        else:
            str_result_array[row] = f'{x[row][-1]}'
            for col in range(row+1, gv.MATRIX_SIZE):
                if x[row][col] != 0:
                    sign = '- '
                    if x[row][col] < 0:
                        sign = '+ '
                    str_result_array[row] += f' {sign}'
                    if abs(x[row][col]) != 1:
                        str_result_array[row] += f'{abs(x[row][col])}'
                    str_result_array[row] += name_x[col]

    return str_result_array


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


def get_solution_string(str_result_array, spaces=5):
    if str_result_array[0] == gv.no_solution:
        return gv.no_solution
    name_x = get_name_x()
    result = ''
    space = ''
    for i in range(0, spaces):
        space += ' '
    for i in range(0, gv.MATRIX_SIZE):
        result += f'{name_x[i]} = {str_result_array[i]}' + space
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

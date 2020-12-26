
test_mode = True
debug_mode = False

show_int_above_1 = True
show_steps = False

ROUND_INT = False
MATRIX_SIZE = 2
MAX_MATRIX_SIZE = 9
MAX_DIGITS_TO_SHOW_FRACTION = 5
PRECISION = 5
MAX_DIGITS_IN_FLOAT = 17
if ROUND_INT:
    MAX_DIGITS_TO_ALLOW_INT = MAX_DIGITS_IN_FLOAT
else:
    MAX_DIGITS_TO_ALLOW_INT = 300
MAX_N_FOR_PERIODIC_CHECK = 97

X_ENTRY_SIZE = 5

no_solution = 'No Solution'
infinite = 'infinite'
inf_rational = '1/0'
invalid_rational = '0/0'

err = None
# for testing
rational_largest_digits = 0
is_rational_converted_to_float = False


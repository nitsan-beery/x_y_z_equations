
test_mode = True
debug_mode = False

show_int_above_1 = False
show_steps = False

ROUND_INT = False
MATRIX_SIZE = 2
MAX_MATRIX_SIZE = 9
MAX_DIGITS_TO_SHOW_FRACTION = 50
PRECISION = 5
MAX_DIGITS_IN_FLOAT = 17
MAX_DIGITS_TO_ALLOW_INT = 308
if ROUND_INT:
    MAX_DIGITS_IN_RATIONAL = MAX_DIGITS_IN_FLOAT
else:
    MAX_DIGITS_IN_RATIONAL = MAX_DIGITS_TO_ALLOW_INT
MAX_N_FOR_PERIODIC_CHECK = 1000

X_ENTRY_SIZE = 5

no_solution = 'No Solution'
infinite = 'infinite'
inf_rational = '1/0'
invalid_rational = '0/0'
unknown_exception = 'unknown exception'
exception_type_notice = 0
exception_type_warning = 1

err = None
# for testing
rational_largest_digits = 0
numerator_converted_to_float = False
step_by_step_matrix = []


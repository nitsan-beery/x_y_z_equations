import global_vars as gv
import math


class Rational:
    def __init__(self, exp=None, check_float=True):
        n, d = get_n_d_from_exp(exp, check_float)
        self.numerator = n
        self.denominator = d
        if exp is not None:
            if exp != gv.invalid_rational and not self.is_valid():
                gv.err = 'invalid rational'
            elif exp != gv.inf_rational and self.is_inf():
                gv.err = 'inf rational'
            elif type(n) is int:
                self.reduce()

    def reduce(self):
        if type(self.numerator) is float or type(self.denominator) is float:
            self.numerator = float(self)
            self.denominator = 1
            return
        if self.numerator == 0:
            self.denominator = 1
            return

        # for testing
        # -----------------------------------------------------------
        if gv.test_mode:
            if type(self.numerator) is int and len(str(abs(self.numerator))) > gv.rational_largest_digits:
                gv.rational_largest_digits = len(str(abs(self.numerator)))
            if type(self.denominator) is int and len(str(abs(self.denominator))) > gv.rational_largest_digits:
                gv.rational_largest_digits = len(str(abs(self.denominator)))
        # -----------------------------------------------------------

        g = get_gcd(self.numerator, self.denominator)
        if self.is_int_too_large():
            if self.can_convert_n_d_to_float():
                self.numerator = self.numerator / g
                self.denominator = self.denominator / g
                if str(self.numerator).count('e') == 0:
                    self.numerator = int(self.numerator)
                if str(self.denominator).count('e') == 0:
                    self.denominator = int(self.denominator)
                # n or d were ~ 1.ex
                if type(self.numerator) is float or type(self.denominator) is float:
                    gv.numerator_converted_to_float = True
                    self.numerator /= self.denominator
                    self.denominator = 1
            else:
                gv.numerator_converted_to_float = True
                self.numerator = float(self)
                self.denominator = 1
        else:
            if g == 1:
                return
            self.numerator = div_large_number(self.numerator, g)
            self.denominator = div_large_number(self.denominator, g)

    def is_valid(self):
        if self.denominator == 0 and self.numerator == 0:
            return False
        return True

    def is_inf(self):
        if abs(self.numerator) == 1 and self.denominator == 0:
            return True
        return False

    def is_int_too_large(self):
        if type(self.numerator) is int and len(str(abs(self.numerator))) > gv.MAX_DIGITS_IN_RATIONAL:
            return True
        if type(self.denominator) is int and len(str(abs(self.denominator))) > gv.MAX_DIGITS_IN_RATIONAL:
            return True
        return False

    def can_convert_n_d_to_float(self):
        if type(self.numerator) is int and len(str(abs(self.numerator))) > gv.MAX_DIGITS_TO_ALLOW_INT:
            return False
        if type(self.denominator) is int and len(str(abs(self.denominator))) > gv.MAX_DIGITS_TO_ALLOW_INT:
            return False
        return True

    def copy(self):
        f = Rational()
        f.numerator = self.numerator
        f.denominator = self.denominator
        return f

    def __str__(self):
        n = self.numerator
        d = self.denominator
        if not self.is_valid():
            return "NAN"
        if self.is_inf():
            if n > 0:
                return "INF"
            return "-INF"
        if n == 0:
            return "0"
        if d == 1:
            return f"{n}"
        if n != int(n) or d != int(d):
            return f"{n/d}"
        n = int(n)
        d = int(d)
        whole_n = div_large_number(n, d)
        mod_n = abs(n) % abs(d)
        str_num = str(whole_n)
        if whole_n == 0 and n < 0:
            str_num = '-0'
        if gv.MAX_DIGITS_TO_SHOW_FRACTION < len(str(d)):
            # +1 is to avoid 1.32e-5 instead of 0.0000132
            mod_n = mod_n / d + 1
            if mod_n == 1:
                mod_n = str(10 ** (gv.PRECISION+3))[2:]
            str_num += f'.{str(mod_n)[2:gv.PRECISION+2]}'
            return str_num
        if abs(n) > abs(d) and gv.show_int_above_1 and whole_n != 0 and mod_n != 0:
            return f"{whole_n}({mod_n}/{d})"
        return f"{n}/{d}"

    def __eq__(self, other):
        f = Rational(other)
        return self.numerator == f.numerator and self.denominator == f.denominator

    def __ne__(self, other):
        f = Rational(other)
        self.reduce()
        return not(self.numerator == f.numerator and self.denominator == f.denominator)

    def __gt__(self, other):
        f = Rational(other)
        if not self.is_valid() or not f.is_valid():
            return False
        if self.is_inf():
            if f.is_inf():
                if self.numerator > 0 and f.numerator < 0:
                    return True
                return False
            if self.numerator > 0:
                return True
            return False
        if f.is_inf():
            if f.numerator > 0:
                return False
            return True
        return float(self) > float(f)

    def __ge__(self, other):
        f = Rational(other)
        if not self.is_valid() or not f.is_valid():
            return False
        if self.__eq__(other):
            return True
        return self.__gt__(other)

    def __lt__(self, other):
        f = Rational(other)
        if not self.is_valid() or not f.is_valid():
            return False
        return not self.__ge__(other)

    def __le__(self, other):
        f = Rational(other)
        if not self.is_valid() or not f.is_valid():
            return False
        return not self.__gt__(other)

    def __add__(self, other):
        if type(other) is not Rational:
            f = Rational(other)
        else:
            f = other.copy()
        if not f.is_valid() or not self.is_valid():
            return Rational(gv.invalid_rational)
        elif self.is_inf():
            if f == -self:
                return Rational(gv.invalid_rational)
            else:
                return self
        elif f.is_inf():
            return f
        if f.numerator == 0:
            return self
        if self.numerator == 0:
            return f
        len_self_n = math.log(abs(self.numerator), 10) + 1
        len_self_d = math.log(abs(self.denominator), 10) + 1
        len_other_n = math.log(abs(f.numerator), 10) + 1
        len_other_d = math.log(abs(f.denominator), 10) + 1
        if len_self_n + len_other_d > gv.MAX_DIGITS_IN_RATIONAL or len_self_d + len_other_n > gv.MAX_DIGITS_IN_RATIONAL \
                or len_self_d + len_other_d > gv.MAX_DIGITS_IN_RATIONAL \
                or int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
            f.numerator = float(self) + float(f)
            f.denominator = 1
            gv.numerator_converted_to_float = True
            if f.numerator == 0:
                # convert 0.0 to int
                f.numerator = 0
        else:
            f.numerator, f.denominator = self.numerator * f.denominator + f.numerator * self.denominator, self.denominator * f.denominator
            f.reduce()
        return f

    def __sub__(self, other):
        if type(other) is not Rational:
            f = Rational(other)
        else:
            f = other.copy()
        if not f.is_valid() or not self.is_valid():
            return Rational(gv.invalid_rational)
        elif self.is_inf():
            if f == self:
                return Rational(gv.invalid_rational)
            else:
                return self
        elif f.is_inf():
            return -f
        if f.numerator == 0:
            return self
        if self.numerator == 0:
            return -f
        len_self_n = math.log(abs(self.numerator), 10) + 1
        len_self_d = math.log(abs(self.denominator), 10) + 1
        len_other_n = math.log(abs(f.numerator), 10) + 1
        len_other_d = math.log(abs(f.denominator), 10) + 1
        if len_self_n + len_other_d > gv.MAX_DIGITS_IN_RATIONAL or len_self_d + len_other_n > gv.MAX_DIGITS_IN_RATIONAL \
                or len_self_d + len_other_d > gv.MAX_DIGITS_IN_RATIONAL \
                or int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
            f.numerator = float(self) - float(f)
            f.denominator = 1
            gv.numerator_converted_to_float = True
        else:
            f.numerator, f.denominator = self.numerator * f.denominator - f.numerator * self.denominator, self.denominator * f.denominator
            f.reduce()
        return f

    def __mul__(self, other):
        if type(other) is not Rational:
            f = Rational(other)
        else:
            f = other.copy()
        if not f.is_valid() or not self.is_valid():
            return Rational(gv.invalid_rational)
        elif self.is_inf():
            if f == 0:
                return Rational(gv.invalid_rational)
            else:
                if (f > 0 and self > 0) or (f < 0 and self < 0):
                    return Rational(gv.inf_rational)
                return -Rational(gv.inf_rational)
        elif f.is_inf():
            if self == 0:
                return Rational(gv.invalid_rational)
            else:
                if (f > 0 and self > 0) or (f < 0 and self < 0):
                    return Rational(gv.inf_rational)
                return -Rational(gv.inf_rational)
        if self.numerator == 0 or f.numerator == 0:
            return Rational(0)
        len_self_n = math.log(abs(self.numerator), 10) + 1
        len_self_d = math.log(abs(self.denominator), 10) + 1
        len_other_n = math.log(abs(f.numerator), 10) + 1
        len_other_d = math.log(abs(f.denominator), 10) + 1
        if len_self_n + len_other_n > gv.MAX_DIGITS_IN_RATIONAL or len_self_d + len_other_d > gv.MAX_DIGITS_IN_RATIONAL \
                or int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
            f.numerator = float(self) * float(f)
            f.denominator = 1
            gv.numerator_converted_to_float = True
        else:
            f.numerator, f.denominator = self.numerator * f.numerator, self.denominator * f.denominator
            f.reduce()
        return f

    def __truediv__(self, other):
        if type(other) is not Rational:
            f = Rational(other)
        else:
            f = other.copy()
        if not f.is_valid() or not self.is_valid() or f.numerator == 0:
            return Rational(gv.invalid_rational)
        elif self.is_inf():
            if f.is_inf():
                return Rational(gv.invalid_rational)
            else:
                if (f > 0 and self > 0) or (f < 0 and self < 0):
                    return Rational(gv.inf_rational)
                return -Rational(gv.inf_rational)
        elif f.is_inf() or self.numerator == 0:
            return Rational(0)
        len_self_n = math.log(abs(self.numerator), 10) + 1
        len_self_d = math.log(abs(self.denominator), 10) + 1
        len_other_n = math.log(abs(f.numerator), 10) + 1
        len_other_d = math.log(abs(f.denominator), 10) + 1
        if len_self_n + len_other_d > gv.MAX_DIGITS_IN_RATIONAL or len_self_d + len_other_n > gv.MAX_DIGITS_IN_RATIONAL \
                or int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
            f.numerator = float(self) / float(f)
            f.denominator = 1
            gv.numerator_converted_to_float = True
        else:
            f.numerator, f.denominator = self.numerator * f.denominator, self.denominator * f.numerator
            f.reduce()
        return f

    def __pow__(self, other):
        if type(other) is not Rational:
            f = Rational(other)
        else:
            f = other.copy()
        n, d = f.numerator, f.denominator
        if d != 0 and self.denominator != 0:
            p = round(self.numerator ** (n/d), gv.PRECISION)
            q = round(self.denominator ** (n/d), gv.PRECISION)
            f = Rational(f'{p}/{q}')
        return f

    def __neg__(self):
        f = Rational()
        f.numerator = -self.numerator
        f.denominator = self.denominator
        return f

    def __abs__(self):
        f = Rational()
        f.numerator = abs(self.numerator)
        f.denominator = abs(self.denominator)
        return f

    def __float__(self):
        if not self.is_valid():
            return float('nan')
        if self.is_inf():
            if self.numerator > 0:
                return float('inf')
            return -float('inf')
        if self.can_convert_n_d_to_float():
            return self.numerator / self.denominator
        sign = -1
        if (self.numerator > 0 and self.denominator > 0) or (self.numerator < 0 and self.denominator < 0):
            sign = 1
        if len(str(self.numerator)) > gv.MAX_DIGITS_TO_ALLOW_INT:
            gv.err = f'too large rational - exceeds {gv.MAX_DIGITS_IN_RATIONAL} digits limit'
            if len(str(self.denominator)) > gv.MAX_DIGITS_TO_ALLOW_INT:
                return float('nan')
            return sign * float('inf')
        # only denominator is too large
        return 0.0


def get_gcd(p, q):
    if q == 0:
        return 1
    if type(p) is not int or type(q) is not int:
        return 1
    d = p % q
    while d:
        p = q
        q = d
        d = p % q
    return int(q)


# exp can be in any format (str, int, float or Rational)
# return numerator, denominator
# if exp is invalid return 0, 0
def get_n_d_from_exp(exp, check_float=True):
    if exp is None:
        return 0, 0
    if type(exp) is Rational:
        return exp.numerator, exp.denominator
    if type(exp) is str:
        slash_count = exp.count("/")
        if slash_count > 1:
            return 0, 0
        elif slash_count == 1:
            slash_pos = exp.find("/")
            if slash_pos == 0 or slash_pos == len(exp)-1:
                return 0, 0
            n = exp[:slash_pos]
            d = exp[slash_pos+1:]
            try:
                n = int(n)
            except ValueError:
                return 0, 0
            try:
                d = int(d)
            except ValueError:
                return 0, 0
            return n, d
        # no slashes
        else:
            try:
                exp = int(exp)
            except ValueError:
                try:
                    exp = float(exp)
                except ValueError:
                    return 0, 0
    # exp is int or float
    return get_n_d_from_float(exp, check_float)


def get_n_d_from_float(exp, check_float=True):
    if str(exp).count('e') > 0:
        return exp, 1
    if exp == float('inf') or exp == float('-inf'):
        if exp > 0:
            return 1, 0
        else:
            return -1, 0
    if str(exp).lower() == 'nan':
        return 0, 0
    if check_float:
        p_n, p_d = check_periodic(exp)
        if p_n > 0:
            if p_d > 0:
                return p_n, p_d
            else:
                return int(exp * p_n), int(p_n)
    return exp, 1


def check_periodic(exp):
    if str(exp).count('e') > 0:
        return 0
    left_part_digits = 5
    left_part_factor = 10 ** left_part_digits
    f = exp * left_part_factor
    if f == int(f):
        return int(f), left_part_factor
    for n in range(2, gv.MAX_N_FOR_PERIODIC_CHECK):
        if exp * n == int(exp * n):
            return n, 0
    if len(str(exp)) < gv.MAX_DIGITS_IN_FLOAT:
        exp_10 = 10 ** len(str(exp))
        return int(exp * exp_10), int(exp_10)
    return exp, 1


# return the int of n/d
def div_large_number(n, d):
    if n != int(n) or d != int(d):
        return int(n/d)
    sign = 1
    if (n < 0 and d > 0) or (n > 0 and d < 0):
        sign = -1
    n = abs(int(n))
    d = abs(int(d))
    if n < d:
        return 0
    if len(str(n)) <= gv.MAX_DIGITS_IN_FLOAT:
        return int(n/d) * sign
    if len(str(d)) > gv.MAX_DIGITS_IN_FLOAT:
        return div_via_denominator(n, d, sign)
    complex_n = len(str(n))
    dif = complex_n - len(str(d))
    complex_d = 2 * math.log(10 ** dif, 2)
    if complex_d < complex_n:
        return div_via_denominator(n, d, sign)
    return div_via_numerator(n, d, sign)


# return the int of n/d
# don't call this function directly. use div_large_number
def div_via_numerator(n, d, sign=1):
    result = 0
    mod_n = 0
    for digit in str(n):
        tmp_num = mod_n * 10 + int(digit)
        result = result * 10 + int(tmp_num / d)
        mod_n = tmp_num % d
    return result * sign


# return the int of n/d
# don't call this function directly. use div_large_number
def div_via_denominator(n, d, sign):
    dif = 10 ** (int(len(str(n)) - len(str(d))) + 1)
    result = 0
    while dif > 0:
        if (result + dif) * d > n:
            if len(str(dif)) < gv.MAX_DIGITS_IN_FLOAT:
                dif = int(dif/2)
            else:
                dif = div_via_numerator(dif, 2)
        else:
            result += dif
    return result * sign



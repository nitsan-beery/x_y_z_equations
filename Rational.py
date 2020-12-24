import global_vars as gv
import math


class Rational:
    def __init__(self, exp=None):
        n, d = get_n_d_from_exp(exp)
        self.numerator = n
        self.denominator = d
        self.reduce()

    def reduce(self):
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
            gv.err = f'too large rational {self.numerator}/{self.denominator} exceeds {gv.MAX_DIGITS_TO_ALLOW_INT} digits limit'
            self.numerator = self.numerator / g
            self.denominator = self.denominator / g
            if str(self.numerator).count('e') == 0:
                self.numerator = int(self.numerator)
            if str(self.denominator).count('e') == 0:
                self.denominator = int(self.denominator)
            if type(self.numerator) is float or type(self.denominator) is float:
                self.numerator /= self.denominator
                self.denominator = 1
        else:
            if g == 1:
                return
            self.numerator = div_large_number(self.numerator, g)
            self.denominator = div_large_number(self.denominator, g)

    def is_valid(self):
        return self.denominator != 0

    def is_int_too_large(self):
        if type(self.numerator) is int and len(str(abs(self.numerator))) > gv.MAX_DIGITS_TO_ALLOW_INT:
            return True
        if type(self.denominator) is int and len(str(abs(self.denominator))) > gv.MAX_DIGITS_TO_ALLOW_INT:
            return True
        return False

    def __str__(self):
        n = self.numerator
        d = self.denominator
        if d == 0:
            return f"{n}/{d}"
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
            str_num += f'.{str(mod_n)[2:gv.PRECISION+2]}'
            return str_num
        if abs(n) > abs(d) and gv.show_int_above_1 and whole_n != 0 and mod_n != 0:
            return f"{whole_n}({mod_n}/{d})"
        return f"{n}/{d}"

    def __eq__(self, other):
        f = Rational(other)
        self.reduce()
        return self.numerator == f.numerator and self.denominator == f.denominator

    def __ne__(self, other):
        f = Rational(other)
        self.reduce()
        return not(self.numerator == f.numerator and self.denominator == f.denominator)

    def __gt__(self, other):
        f = Rational(other)
        if self.denominator == 0 or f.denominator == 0:
            return False
        return self.numerator/self.denominator > f.numerator/f.denominator

    def __ge__(self, other):
        f = Rational(other)
        if self.denominator == 0 or f.denominator == 0:
            return False
        return self.numerator/self.denominator >= f.numerator/f.denominator

    def __lt__(self, other):
        f = Rational(other)
        if self.denominator == 0 or f.denominator == 0:
            return False
        return self.numerator/self.denominator < f.numerator/f.denominator

    def __le__(self, other):
        f = Rational(other)
        if self.denominator == 0 or f.denominator == 0:
            return False
        return self.numerator/self.denominator <= f.numerator/f.denominator

    def __add__(self, other):
        f = Rational(other)
        if f.numerator == 0:
            return self
        if self.numerator == 0:
            return f
        if f.denominator != 0 and self.denominator != 0:
            len_self_n = math.log(abs(self.numerator), 10) + 1
            len_self_d = math.log(abs(self.denominator), 10) + 1
            len_f_n = math.log(abs(f.numerator), 10) + 1
            len_f_d = math.log(abs(f.denominator), 10) + 1
            if len_self_n + len_f_d > gv.MAX_DIGITS_TO_ALLOW_INT or len_self_d + len_f_n > gv.MAX_DIGITS_TO_ALLOW_INT \
                    or len_self_d + len_f_d > gv.MAX_DIGITS_TO_ALLOW_INT \
                    or int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
                f.numerator = (self.numerator/self.denominator) + (f.numerator/f.denominator)
                f.denominator = 1
                gv.is_rational_converted_to_float = True
            else:
                f.numerator, f.denominator = self.numerator * f.denominator + f.numerator * self.denominator, self.denominator * f.denominator
                f.reduce()
        return f

    def __sub__(self, other):
        f = Rational(other)
        if f.numerator == 0:
            return self
        if self.numerator == 0:
            return -f
        if f.denominator != 0 and self.denominator != 0:
            len_self_n = math.log(abs(self.numerator), 10) + 1
            len_self_d = math.log(abs(self.denominator), 10) + 1
            len_f_n = math.log(abs(f.numerator), 10) + 1
            len_f_d = math.log(abs(f.denominator), 10) + 1
            if len_self_n + len_f_d > gv.MAX_DIGITS_TO_ALLOW_INT or len_self_d + len_f_n > gv.MAX_DIGITS_TO_ALLOW_INT \
                    or len_self_d + len_f_d > gv.MAX_DIGITS_TO_ALLOW_INT \
                    or int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
                f.numerator = (self.numerator/self.denominator) - (f.numerator/f.denominator)
                f.denominator = 1
                gv.is_rational_converted_to_float = True
            else:
                f.numerator, f.denominator = self.numerator * f.denominator - f.numerator * self.denominator, self.denominator * f.denominator
                f.reduce()
        return f

    def __mul__(self, other):
        f = Rational(other)
        if f.denominator == 0 or self.denominator == 0:
            return Rational('0/0')
        if self.numerator == 0 or f.numerator == 0:
            return Rational(0)
        len_self_n = math.log(abs(self.numerator), 10) + 1
        len_self_d = math.log(abs(self.denominator), 10) + 1
        len_f_n = math.log(abs(f.numerator), 10) + 1
        len_f_d = math.log(abs(f.denominator), 10) + 1
        if len_self_n + len_f_n > gv.MAX_DIGITS_TO_ALLOW_INT or len_self_d + len_f_d > gv.MAX_DIGITS_TO_ALLOW_INT \
                or int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
            f.numerator = (self.numerator / self.denominator) * (f.numerator / f.denominator)
            f.denominator = 1
            gv.is_rational_converted_to_float = True
        else:
            f.numerator, f.denominator = self.numerator * f.numerator, self.denominator * f.denominator
            f.reduce()
        return f

    def __truediv__(self, other):
        f = Rational(other)
        if f.denominator == 0 or self.denominator == 0 or f.numerator == 0:
            return Rational('0/0')
        if self.numerator == 0:
            return Rational(0)
        len_self_n = math.log(abs(self.numerator), 10) + 1
        len_self_d = math.log(abs(self.denominator), 10) + 1
        len_f_n = math.log(abs(f.numerator), 10) + 1
        len_f_d = math.log(abs(f.denominator), 10) + 1
        if len_self_n + len_f_d > gv.MAX_DIGITS_TO_ALLOW_INT or len_self_d + len_f_n > gv.MAX_DIGITS_TO_ALLOW_INT \
                or int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
            f.numerator = (self.numerator / self.denominator) / (f.numerator / f.denominator)
            f.denominator = 1
            gv.is_rational_converted_to_float = True
        else:
            f.numerator, f.denominator = self.numerator * f.denominator, self.denominator * f.numerator
            f.reduce()
        return f

    def __pow__(self, other):
        f = Rational(other)
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


def get_gcd(p, q):
    if q == 0:
        return 1
    if int(p) != p or int(q) != q:
    #if type(p) is not int or type(q) is not int:
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
def get_n_d_from_exp(exp):
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
    return get_n_d_from_float(exp)


def get_n_d_from_float(exp):
    if str(exp).count('e') > 0:
        return exp, 1
    '''
    if str(exp).count('+') > 0:
        return exp, 1
    else:
        pos = str(exp).find('e-')
        exp_10 = int(str(exp)[pos+2:])
        exp_10 += pos-2
        exp_10 = 10 ** exp_10
        exp = int(exp * exp_10)
        return exp, exp_10
    '''
    if exp == int(exp):
    #if type(exp) is int:
        return int(exp), 1
    f_exp = exp
    exp = str(exp)
    sign = 1
    if exp[0] == '-':
        sign = -1
    p = exp.find(".")
    if p == 0 or (p == 1 and sign == -1):
        i = 0
    else:
        i = int(exp[:p])
    str_r = exp[p + 1:]
    r = int(str_r)
    if len(exp) < gv.MAX_DIGITS_IN_FLOAT:
        p = len(str_r)
        d = 10 ** p
        n = d * i + sign * r
        g = get_gcd(n, d)
        return int(n / g), int(d / g)
    periodic = check_periodic(f_exp)
    if periodic > 0:
        return int(f_exp * periodic), int(periodic)
    else:
        return f_exp, 1


def check_periodic(f):
    for n in range(2, gv.MAX_N_FOR_PERIODIC_CHECK):
        if f * n == int(n * f):
            return n
    return 0


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


infinite_rational = Rational('1/0')
no_solution_rational = Rational('0/0')

import global_vars as gv


class Rational:
    def __init__(self, exp=None):
        n, d = get_n_d_from_exp(exp)
        self.numerator = n
        self.denominator = d
        self.reduce()

    def reduce(self):
        g = get_gcd(self.numerator, self.denominator)
        if g == 1:
            return
        if len(str(g)) > gv.MAX_DIGITS_IN_FLOAT:
            self.numerator = div_large_denominator(self.numerator, g)
            self.denominator = div_large_denominator(self.denominator, g)
            #print(f"Too big GCD {g} - {len(str(g))} digits")
        else:
            self.numerator = div_large_number(self.numerator, g)
            self.denominator = div_large_number(self.denominator, g)

    def is_valid(self):
        return self.denominator != 0

    def __str__(self):
        n = self.numerator
        d = self.denominator
        if len(str(d)) > gv.MAX_DIGITS_IN_FLOAT:
            whole_n = div_large_denominator(n, d)
        else:
            whole_n = div_large_number(n, d)
        mod_n = n % d
        if n < 0:
            mod_n = d - mod_n
        if d == 0:
            return f"{n}/{d}"
        if n == 0:
            return "0"
        elif d == 1:
            return f"{n}"
        str_num = str(whole_n)
        if whole_n == 0 and n < 0:
            str_num = '-0'
        if gv.MAX_DIGITS_TO_SHOW_FRACTION < len(str(d)) < gv.MAX_DIGITS_IN_FLOAT:
            # +1 is to avoid 1.32e-5 instead of 0.0000132
            mod_n = mod_n / d + 1
            str_num += f'.{str(mod_n)[2:gv.FLOAT_SHOW_DIGITS+2]}...'
            return str_num
        if abs(n) > d and gv.show_int_above_1 and whole_n != 0:
            return f"{whole_n}({mod_n}/{d})"
        return f"{n}/{d}"

    def __eq__(self, other):
        if type(other) == Rational:
            f = other
        else:
            f = Rational(other)
        self.reduce()

        f.reduce()
        return self.numerator == f.numerator and self.denominator == f.denominator

    def __ne__(self, other):
        if type(other) == Rational:
            f = other
        else:
            f = Rational(other)
        self.reduce()
        f.reduce()
        return not(self.numerator == f.numerator and self.denominator == f.denominator)

    def __gt__(self, other):
        if type(other) == Rational:
            f = other
        else:
            f = Rational(other)
        if self.denominator == 0 or f.denominator == 0:
            return False
        return self.numerator/self.denominator > f.numerator/f.denominator

    def __ge__(self, other):
        if type(other) == Rational:
            f = other
        else:
            f = Rational(other)
        if self.denominator == 0 or f.denominator == 0:
            return False
        return self.numerator/self.denominator >= f.numerator/f.denominator

    def __lt__(self, other):
        if type(other) == Rational:
            f = other
        else:
            f = Rational(other)
        if self.denominator == 0 or f.denominator == 0:
            return False
        return self.numerator/self.denominator < f.numerator/f.denominator

    def __le__(self, other):
        if type(other) == Rational:
            f = other
        else:
            f = Rational(other)
        if self.denominator == 0 or f.denominator == 0:
            return False
        return self.numerator/self.denominator <= f.numerator/f.denominator

    def __add__(self, other):
        f = Rational(other)
        if f.denominator != 0 and self.denominator != 0:
            f.numerator, f.denominator = self.numerator * f.denominator + f.numerator * self.denominator, self.denominator * f.denominator
            f.reduce()
        return f

    def __sub__(self, other):
        f = Rational(other)
        if f.denominator != 0 and self.denominator != 0:
            f.numerator, f.denominator = self.numerator * f.denominator - f.numerator * self.denominator, self.denominator * f.denominator
            f.reduce()
        return f

    def __mul__(self, other):
        f = Rational(other)
        if f.denominator == 0 or self.denominator == 0:
            return Rational('0/0')
        if int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
            f.numerator = self.numerator * f.numerator / (self.denominator * f.denominator)
            f.denominator = 1
            return f
        f.numerator, f.denominator = self.numerator * f.numerator, self.denominator * f.denominator
        f.reduce()
        return f

    def __truediv__(self, other):
        f = Rational(other)
        if f.denominator == 0 or self.denominator == 0 or f.numerator == 0:
            return Rational('0/0')
        if int(f.numerator) != f.numerator or int(self.numerator) != self.numerator:
            f.numerator = self.numerator * f.denominator / (self.denominator * f.numerator)
            f.denominator = 1
            return f
        f.numerator, f.denominator = self.numerator * f.denominator, self.denominator * f.numerator
        f.reduce()
        return f

    def __pow__(self, other):
        f = Rational(other)
        n, d = f.numerator, f.denominator
        if d != 0 and self.denominator != 0:
            p = round(self.numerator ** (n/d), gv.PRECISION)
            q = round(self.denominator ** (n/d), gv.PRECISION)
            f = Rational(f'{p/q}')
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
    if q == 0 or int(p) != p or int(q) != q:
        return 1
    d = p % q
    while d:
        p = q
        q = d
        d = p % q
    return q


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
    # exp is float
    if str(exp).count('e+') > 0:
        return exp, 1
    if str(exp).count('e-') > 0:
        pos = str(exp).find('e-')
        exp_10 = int(str(exp)[pos+2:])
        exp_10 += pos-2
        if exp_10 < gv.MAX_DIGITS_IN_FLOAT-1:
            exp_10 = 10 ** exp_10
            exp = int(exp * exp_10)
            return exp, exp_10
        return exp, 1
    if exp == int(exp):
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
    if len(str_r) < gv.MAX_DIGITS_IN_FLOAT-1:
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


# return int(n/m)
def div_large_number(n, d):
    big_n = 0
    sign = 1
    if n < 0:
        sign = -1
    n = abs(n)
    while len(str(n)) > gv.MAX_DIGITS_IN_FLOAT:
        chunk = int(str(n)[:gv.MAX_DIGITS_IN_FLOAT])
        r = int(str(n)[gv.MAX_DIGITS_IN_FLOAT:])
        exp_10 = len(str(n)) - len(str(chunk))
        exp_10 = 10 ** exp_10
        big_n += int(chunk / d) * exp_10
        mod_n = chunk % d
        n = mod_n * exp_10 + r
    big_n += int(n / d)
    return big_n * sign


# return the int of n/d
def div_large_denominator(n, d):
    sign = 1
    if (n < 0 and d > 0) or (n > 0 and d < 0):
        sign = -1
    n = abs(n)
    d = abs(d)
    if n < d:
        return 0
    dif = 10 ** (int(len(str(n)) - len(str(d))) + 1)
    result = 0
    while dif > 0:
        if (result + dif) * d > n:
            dif = div_large_number(dif, 2)
        else:
            result += dif
    return result * sign


infinite_rational = Rational('1/0')
no_solution_rational = Rational('0/0')

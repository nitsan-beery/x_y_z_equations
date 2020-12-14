import global_vars as gv


class Rational:
    def __init__(self, exp=None):
        n, d = get_n_d_from_exp(exp)
        self.numerator = n
        self.denominator = d

    def reduce(self):
        g = get_gcd(self.numerator, self.denominator)
        self.numerator /= g
        self.denominator /= g

    def is_valid(self):
        return self.denominator != 0

    def __str__(self):
        n = int(self.numerator)
        d = int(self.denominator)
        if n == 0 and d != 0:
            return "0"
        elif d == 1:
            return f"{n}"
        elif d != 0 and len(str(d)) > gv.MAX_DIGITS_TO_SHOW_FRACTION:
            if int((10 ** gv.FLOAT_SHOW_DIGITS) * n/d) == (10 ** gv.FLOAT_SHOW_DIGITS) * n/d:
                str_num = f"{(n/d)}"
            else:
                f = n/d
                num = int(f)
                part = abs(f - num)
                part = str(part)[2:gv.FLOAT_SHOW_DIGITS + 2]
                str_num = f'{num}.{part}...'
            return str_num
        if d != 0 and abs(n) > d and gv.show_int_above_1:
            return f"{int(n / d)}({abs(n) % d}/{d})"
        return f"{n}/{d}"

    def __eq__(self, other):
        f = Rational(other)
        self.reduce()
        f.reduce()
        return self.numerator == f.numerator and self.denominator == f.denominator

    def __ne__(self, other):
        f = Rational(other)
        self.reduce()
        f.reduce()
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
        f = Rational("0/0")
        n, d = get_n_d_from_exp(other)
        if d != 0 and self.denominator != 0:
            f.numerator = d * self.numerator
            n = n * self.denominator
            f.denominator = d * self.denominator
            f.numerator += n
            f.reduce()
        return f

    def __sub__(self, other):
        f = Rational("0/0")
        n, d = get_n_d_from_exp(other)
        if d != 0 and self.denominator != 0:
            f.numerator = d * self.numerator
            n = n * self.denominator
            f.denominator = d * self.denominator
            f.numerator -= n
            f.reduce()
        return f

    def __mul__(self, other):
        f = Rational("0/0")
        n, d = get_n_d_from_exp(other)
        if d != 0 and self.denominator != 0:
            f.numerator = n * self.numerator
            f.denominator = d * self.denominator
            f.reduce()
        return f

    def __truediv__(self, other):
        f = Rational("0/0")
        n, d = get_n_d_from_exp(other)
        if d != 0 and self.denominator != 0 and n != 0:
            f.numerator = d * self.numerator
            f.denominator = n * self.denominator
            f.reduce()
        return f

    def __pow__(self, other):
        f = Rational("0/0")
        n, d = get_n_d_from_exp(other)
        if d != 0 and self.denominator != 0:
            p = round(self.numerator ** (n/d), 12)
            q = round(self.denominator ** (n/d), 12)
            f = Rational(p/q)
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
            g = get_gcd(n, d)
            return int(n / g), int(d / g)
        # no slashes
        else:
            try:
                exp = float(exp)
            except ValueError:
                return 0, 0
    # exp is float
    if exp == int(exp):
        return int(exp), 1
    if len(str(exp)) > gv.MAX_DIGITS_TO_SHOW_FRACTION:
        periodic = check_periodic(exp)
        if periodic > 0:
            return exp * periodic, periodic
    exp = str(exp)
    sign = 1
    if exp[0] == '-':
        sign = -1
    p = exp.find(".")
    if p == 0 or (p == 1 and sign == -1):
        i = 0
    else:
        i = int(exp[:p])
    r = int(exp[p + 1:])
    if r == 0:
        return i, 1
    p = len(str(r))
    d = 10 ** p
    n = d * i + sign * r
    g = get_gcd(n, d)
    return int(n/g), int(d/g)


def check_periodic(f):
    for n in range(2, gv.MAX_N_FOR_PERIODIC_CHECK):
        if f * n == int(n * f):
            return n
    return 0

infinite_rational = Rational('1/0')
no_solution_rational = Rational('0/0')

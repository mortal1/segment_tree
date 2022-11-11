# Miscellania

class Monoid():
    def op(a, b):
        return

    id = None


def lift(f):
    def new_f(a, b):
        if a is None:
            return b
        elif b is None:
            return a
        else:
            return f(a, b)
    return new_f


def lift_transfer(f):
    def new_f(a, b):
        if a is None:
            return None
        elif b is None:
            return a
        else:
            return f(a, b)
    return new_f



# Operators

def snd(a, b):
    if b is not None:
        return b
    else:
        return a


def sum(a, b):
    return a + b


def mul(a, b):
    return a * b


min


max


def maxn(a, b):
    return sorted(a + b, reverse=True)[:len(b)]


def bounds(a, b):
    amin, amax = a
    bmin, bmax = b
    return min(amin, bmin), max(amax, bmax)


def inorder(a, b):
    amin, amax, aordered = a
    bmin, bmax, bordered = b
    return min(amin, bmin), max(amax, bmax),\
        aordered and bordered and amax <= bmin


ids = {
    snd: None,
    sum: 0,
    mul: 1,
    min: float("INF"),
    max: float("-INF"),
    maxn: [],
    bounds: (float("INF"), float("-INF")),
    inorder: (float("INF"), float("-INF"), True)
}




# transfers

# def add_context(f):
#     def new_f(q, u, istart=None, iend=None):
#         return f(q, u)
#     return new_f


# snd_snd = add_context(snd)
def snd_snd(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def sum_snd(q, u, istart, iend):
    if u is not None:
        return u * (iend - istart)
    else:
        return q


def sum_sum(q, u, istart, iend):
    return q + u * (iend - istart)


# sum_mul = add_context(mul)
def sum_mul(q, u, istart=None, iend=None):
    return q * u


def mul_snd(q, u, istart, iend):
    if u is not None:
        return u ** (iend - istart)
    else:
        return q


def mul_mul(q, u, istart, iend):
    return q * u ** (iend - istart)


# min_snd = add_context(snd)
def min_snd(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


# min_sum = add_context(sum)
def min_sum(q, u, istart=None, iend=None):
    return q + u


# if u >= 0
# min_mul = add_context(mul)
def min_mul(q, u, istart=None, iend=None):
    return q * u


# min_max = add_context(max)
def min_max(q, u, istart=None, iend=None):
    return max(q, u)


# min_min = add_context(min)
def min_min(q, u, istart=None, iend=None):
    return min(q, u)


# max_snd = add_context(snd)
def max_snd(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


# max_sum = add_context(sum)
def max_sum(q, u, istart=None, iend=None):
    return q + u


# if u >= 0
# max_mul = add_context(mul)
def max_mul(q, u, istart=None, iend=None):
    return q * u


# max_max = add_context(max)
def max_max(q, u, istart=None, iend=None):
    return max(q, u)


# max_min = add_context(min)
def max_min(q, u, istart=None, iend=None):
    return min(q, u)


def maxn_snd(q, u, istart=None, iend=None):
    if u is not None:
        return [u]
    else:
        return q


def maxn_sum(q, u, istart=None, iend=None):
    return [v + u for v in q]


# if u >= 0
def maxn_mul(q, u, istart=None, iend=None):
    return [v * u for v in q]


def bounds_snd(q, u, istart=None, iend=None):
    if u is not None:
        return (u, u)
    else:
        return q


def bounds_sum(q, u, istart=None, iend=None):
    return (q[0] + u, q[1] + u)


def bounds_mul(q, u, istart=None, iend=None):
    if u >= 0:
        return (q[0] * u, q[1] * u)
    else:
        return (q[1] * u, q[0] * u)



transfers = {
    (snd, snd): snd_snd,
    (sum, snd): sum_snd,
    (mul, snd): mul_snd,
    (min, snd): min_snd,
    (max, snd): max_snd,
    (maxn, snd): maxn_snd,
    (bounds, snd): bounds_snd,
    (sum, sum): sum_sum,
    (min, sum): min_sum,
    (max, sum): max_sum,
    (maxn, sum): maxn_sum,
    (bounds, sum): bounds_sum,
    (sum, mul): sum_mul,
    (min, mul): min_mul,
    (max, mul): max_mul,
    (maxn, mul): maxn_mul,
    (bounds, mul): bounds_mul,
    (min, max): max_max,
    (max, max): max_max,
    (min, min): max_min,
    (max, min): max_min,
}

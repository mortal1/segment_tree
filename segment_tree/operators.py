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


# Operators

def snd(a, b):
    if b is not None:
        return b
    else:
        return a


snd_id = None


def add(a, b):
    return a + b


add_id = 0


def mul(a, b):
    return a * b


mul_id = 1


min = min

min_id = float("INF")

max = max

max_id = float("-INF")


def max2(a, b):
    return (max(a[0], b[0]), max([min(a[0], b[0]), a[1], b[1]]))


max2_id = (max_id, max_id)


def bounds(a, b):
    return (min(a[0], b[0]), max(a[1], b[1]))


bounds_id = (min_id, max_id)


# transfers

def snd_snd(u, q, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def snd_add(u, q, istart, iend):
    if u is not None:
        return u * (iend - istart)
    else:
        return q


def add_add(u, q, istart, iend):
    return q + u * (iend - istart)


def mul_add(u, q, istart=None, iend=None):
    return q * u


def snd_mul(u, q, istart, iend):
    if u is not None:
        return u ** (iend - istart)
    else:
        return q


def snd_min(u, q, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def add_min(u, q, istart=None, iend=None):
    return q + u


# if u >= 0
def mul_min(u, q, istart=None, iend=None):
    return q * u


def snd_max(u, q, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def add_max(u, q, istart=None, iend=None):
    return q + u


# if u >= 0
def mul_max(u, q, istart=None, iend=None):
    return q * u


def snd_max2(u, q, istart=None, iend=None):
    if u is not None:
        return (u, max_id)
    else:
        return q


def add_max2(u, q, istart=None, iend=None):
    return (q[0] + u, q[1] + u)


# if u >= 0
def mul_max2(u, q, istart=None, iend=None):
    return (q[0] * u, q[1] * u)


def snd_bounds(u, q, istart=None, iend=None):
    if u is not None:
        return (u, u)
    else:
        return q


def add_bounds(u, q, istart=None, iend=None):
    return (q[0] + u, q[1] + u)


def mul_bounds(u, q, istart=None, iend=None):
    if u >= 0:
        return (q[0] * u, q[1] * u)
    else:
        return (q[1] * u, q[0] * u)


default_ids = {
    snd: snd_id,
    add: add_id,
    mul: mul_id,
    min: min_id,
    max: max_id,
    max2: max2_id,
    bounds: bounds_id,
}

default_transfers = {
    (snd, snd): snd_snd,
    (snd, add): snd_add,
    (add, add): add_add,
    (mul, add): mul_add,
    (snd, mul): snd_mul,
    (snd, min): snd_min,
    (add, min): add_min,
    (mul, min): mul_min,
    (snd, max): snd_max,
    (add, max): add_max,
    (mul, max): mul_max,
    (snd, max2): snd_max2,
    (add, max2): add_max2,
    (mul, max2): mul_max2,
    (snd, bounds): snd_bounds,
    (add, bounds): add_bounds,
    (mul, bounds): mul_bounds,
}

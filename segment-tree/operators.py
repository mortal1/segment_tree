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


def snd_max(u, q, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def add_add(u, q, istart, iend):
    return q + u * (iend - istart)


def add_min(u, q, istart=None, iend=None):
    return q + u


def add_max(u, q, istart=None, iend=None):
    return q + u


def mul_add(u, q, istart=None, iend=None):
    return q * u


# if u >= 0
def mul_min(u, q, istart=None, iend=None):
    return q * u


# if u >= 0
def mul_max(u, q, istart=None, iend=None):
    return q * u


default_ids = {
    snd: snd_id,
    add: add_id,
    mul: mul_id,
    min: min_id,
    max: max_id,
}

default_transfers = {
    (snd, snd): snd_snd,
    (snd, add): snd_add,
    (snd, mul): snd_mul,
    (snd, min): snd_min,
    (snd, max): snd_max,
    (add, add): add_add,
    (add, min): add_min,
    (add, max): add_max,
    (mul, add): mul_add,
    (mul, min): mul_min,
    (mul, max): mul_max,
}

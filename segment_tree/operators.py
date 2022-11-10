# Higher order functions

class Monoid():
    def op(a, b):
        return

    id = None


def lift_alternative(f):
    def new_f(a, b):
        if a is None:
            return b
        elif b is None:
            return a
        else:
            return f(a, b)
    return new_f

def lift_transfer(f):
    def new_f(q, u):
        if q is None:
            return None
        elif u is None:
            return q
        else:
            return f(u, q)
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


min

min_id = float("INF")

max

max_id = float("-INF")


def maxn(a, b):
    return sorted(set(a + b), reverse=True)[:len(b)]


maxn_id = []


def bounds(a, b):
    amin, amax = a
    bmin, bmax = b
    return min(amin, bmin), max(amax, bmax)


bounds_id = (min_id, max_id)


def inorder(a, b):
    amin, amax, aordered = a
    bmin, bmax, bordered = b
    return min(amin, bmin), max(amax, bmax),\
        aordered and bordered and amax < bmin

inorder_id = (min_id, max_id, True)

# transfers

def snd_snd(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def snd_add(q, u, istart, iend):
    if u is not None:
        return u * (iend - istart)
    else:
        return q


def add_add(q, u, istart, iend):
    return q + u * (iend - istart)


def mul_add(q, u, istart=None, iend=None):
    return q * u


def snd_mul(q, u, istart, iend):
    if u is not None:
        return u ** (iend - istart)
    else:
        return q


def snd_min(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def add_min(q, u, istart=None, iend=None):
    return q + u


# if u >= 0
def mul_min(q, u, istart=None, iend=None):
    return q * u


def snd_max(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def add_max(q, u, istart=None, iend=None):
    return q + u


# if u >= 0
def mul_max(q, u, istart=None, iend=None):
    return q * u


def snd_maxn(q, u, istart=None, iend=None):
    if u is not None:
        return [u]
    else:
        return q


def add_maxn(q, u, istart=None, iend=None):
    return [v + u for v in q]


# if u >= 0
def mul_maxn(q, u, istart=None, iend=None):
    return [v * u for v in q]


def snd_bounds(q, u, istart=None, iend=None):
    if u is not None:
        return (u, u)
    else:
        return q


def add_bounds(q, u, istart=None, iend=None):
    return (q[0] + u, q[1] + u)


def mul_bounds(q, u, istart=None, iend=None):
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
    maxn: maxn_id,
    bounds: bounds_id,
    inorder: inorder_id
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
    (snd, maxn): snd_maxn,
    (add, maxn): add_maxn,
    (mul, maxn): mul_maxn,
    (snd, bounds): snd_bounds,
    (add, bounds): add_bounds,
    (mul, bounds): mul_bounds,
}

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

mID = {
    snd: snd_id,
    add: add_id,
    mul: mul_id,
    min: min_id,
    max: max_id,
}

# transfers

def snd_snd(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def add_snd(q, u, istart, iend):
    if u is not None:
        return u * (iend - istart)
    else:
        return q


def mul_snd(q, u, istart, iend):
    if u is not None:
        return u ** (iend - istart)
    else:
        return q


def min_snd(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q


def max_snd(q, u, istart=None, iend=None):
    if u is not None:
        return u
    else:
        return q

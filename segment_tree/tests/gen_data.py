from dataclasses import dataclass
from typing import List, Any


@dataclass
class Inputs:
    n: int
    m: int
    arr: List[int]
    queries: List[List[Any]]


def validate(inputs):
    valid = True

    def check(cond):
        global valid
        valid = valid and cond

    check(len(inputs[0]) == 2)
    n, m = inputs[0]
    check(len(inputs[1]) == n)
    check(len(inputs[2:]) == m)
    return valid



def save(inputs, filename):
    text = '\n'.join(' '.join(str(x) for x in line) for line in inputs)
    with open(filename, 'w') as f:
        f.write(text)

# init_large = [
#     [100000, 100000],
#     [i for i in range(1, 100001)],
#     [['Q', i, i] for i in range(1, 100001)]
# ]

# save(init_large, 'init_large.in')


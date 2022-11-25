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

def test_query_zero(n):
    print(n, 1)
    print(' '.join(list(range(5, n+5)))) 
    print('Q 0 1')

def test_query_n(n):
    print(n, 1)
    print(' '.join(list(range(5, n+5)))) 
    print(f'Q {n-1} {n}')

def test_query_units(n):
    print(n, n-1)
    print(' '.join(list(range(5, n+5))))
    for i in range(n-1):
        print(f'Q {i} {i+1}')   

def test_query_full(n):
    print(n, 1)
    print(' '.join(list(range(5, n+5))))
    print(f'Q {0} {n}')   

# fails on naive brute forces
def test_query_fulln(n):
    print(n, n)
    print(' '.join(list(range(5, n+5))))
    for i in range(n):
        print(f'Q {0} {n}')   


def test_query_right_triangle(n):
    print(n, n-1)
    print(' '.join(list(range(5, n+5))))
    for i in range(n-1):
        print(f'Q {i} {n}')   

def test_query_left_triangle(n):
    print(n, n-1)
    print(' '.join(list(range(5, n+5))))
    for i in range(1, n):
        print(f'Q {0} {i}')   

# fails on non-logn range trees
def test_query_speed(n):
    print(n, n)
    print(' '.join(list(range(5, n+5))))
    for i in range(n):
        print(f'Q {i//2} {(n+i)//2}')   




def test_update_zero(n):
    print(n, 2)
    print(' '.join(list(range(5, n+5)))) 
    print('u 0 1 10')
    print('q 0 1')


def test_update_n(n):
    print(n, 2)
    print(' '.join(list(range(5, n+5)))) 
    print(f'u {n-1} {n} 10')
    print(f'q {n-1} {n}')

def test_update_units(n):
    n //= 2
    print(n, 2*n-2)
    print(' '.join(list(range(5, n+5))))
    for i in range(n-1):
        print(f'u {i} {i+1} {i}')   
        print(f'q {i} {i+1}')   

def test_update_full(n):
    print(n, 2)
    print(' '.join(list(range(5, n+5))))
    print(f'u {0} {n} 10')   
    print(f'q {0} {n}')   

def test_update_right_triangle(n):
    n = n // 2
    print(n, n-1)
    print(' '.join(list(range(5, n+5))))
    for i in range(n-1):
        print(f'U {i} {n}')   
        print(f'Q {i} {n}')   

def test_update_left_triangle(n):
    n = n // 2
    print(n, n-1)
    print(' '.join(list(range(5, n+5))))
    for i in range(1, n):
        print(f'Q {0} {i}')   


# fails on naive brute forces
def test_update_fulln(n):
    n //= 2 
    print(n, 2*n)
    print(' '.join(list(range(5, n+5))))
    for i in range(n):
        print(f'u {0} {n} 10')   
        print(f'q {0} {n}')   

# fails on non-logn range trees
def test_update_speed(n):
    print(n, n)
    print(' '.join(list(range(5, n+5))))
    for i in range(n):
        if i % 2 == 1
        print(f'q {i//2} {(n+i)//2}')   


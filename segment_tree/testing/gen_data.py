from dataclasses import dataclass
from typing import List, Any
import sys, os
from contextlib import redirect_stdout


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



## Test queries on initialised tree
def test_query_zero(n):
    print(n, 1)
    print(' '.join(str(i) for i in range(5, n+5))) 
    print('Q 0 1')

def test_query_n(n):
    print(n, 1)
    print(' '.join(str(i) for i in range(5, n+5))) 
    print(f'Q {n-1} {n}')

def test_query_units(n):
    print(n, n-1)
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(n-1):
        print(f'Q {i} {i+1}')   

def test_query_full(n):
    print(n, 1)
    print(' '.join(str(i) for i in range(5, n+5)))
    print(f'Q {0} {n}')   

# fails on naive brute forces
def test_query_fulln(n):
    print(n, n)
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(n):
        print(f'Q {0} {n}')   


def test_query_right_triangle(n):
    print(n, n-1)
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(n-1):
        print(f'Q {i} {n}')   

def test_query_left_triangle(n):
    print(n, n-1)
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(1, n):
        print(f'Q {0} {i}')   

# fails on non-logn updates and queries
def test_query_speed(n):
    print(n, n)
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(n):
        print(f'Q {i//2} {(n+i)//2}')   


## Test updates

def test_update_zero(n):
    print(n, 2)
    print(' '.join(str(i) for i in range(5, n+5))) 
    print('U 0 1 10')
    print('Q 0 1')


def test_update_n(n):
    print(n, 2)
    print(' '.join(str(i) for i in range(5, n+5))) 
    print(f'U {n-1} {n} 10')
    print(f'Q {n-1} {n}')

def test_update_units(n):
    n //= 2
    print(n, 2*(n-1))
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(n-1):
        print(f'U {i} {i+1} {i}')   
        print(f'Q {i} {i+1}')   

def test_update_full(n):
    print(n, 2)
    print(' '.join(str(i) for i in range(5, n+5)))
    print(f'U {0} {n} 10')   
    print(f'Q {0} {n}') 

# fails on naive brute forces
def test_update_fulln(n):
    print(n, n)
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(n//2):
        print(f'U {0} {n} {i}')   
        print(f'Q {0} {n}')

def test_update_right_triangle(n):
    n = n // 2
    print(n, 2*(n-1))
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(n-1):
        print(f'U {i} {n} {i}')
        print(f'Q {i} {n}')   


def test_update_left_triangle(n):
    n = n // 2
    print(n, 2*(n-1))
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(1, n):
        print(f'U {0} {i} {i}')
        print(f'Q {0} {i}')   

# fails on non-logn updates and queries
def test_update_speed(n):
    print(n, n)
    print(' '.join(str(i) for i in range(5, n+5)))
    for i in range(n):
        if i % 2 == 0:
            print(f'U {i//2} {(n+i)//2} {i}')   
        elif i % 2 == 1:
            print(f'Q {i//2} {(n+i)//2}')   



# Testing interaction between updates and queries

def test_parents_updated(n):
    '''
    Ensures that parents and grandparents are correctly updated.
    '''
    if n < 4:
        print(f"n = {n} is too small", file=sys.stderr)
        return
    print(n, 2)
    print(' '.join(str(i) for i in range(5, n+5)))
    print(f'U 2 3 10')
    print(f'Q 2 4')
    print(f'U 1 2 20')
    print(f'Q 0 4')

def test_children_updated(n):
    '''
    Ensures that children and grandchildren are correctly updated.
    '''
    if n < 4:
        print(f"n = {n} is too small", file=sys.stderr)
        return
    print(n, 2)
    print(' '.join(str(i) for i in range(5, n+5)))
    print(f'U 0 4 10')
    print(f'Q 2 4')
    print(f'U 0 4 20')
    print(f'Q 1 2')


tests = [
test_query_zero, test_query_n, test_query_units, test_query_full, test_query_fulln, test_query_right_triangle, test_query_left_triangle, test_query_speed, test_update_zero, test_update_n, test_update_units,test_update_full, test_update_fulln, test_update_right_triangle, test_update_left_triangle, test_update_speed, test_parents_updated, test_children_updated
]


def make_all(n):
    tc = 0
    for test in tests:
        with open(f'{os.path.dirname(__file__)}/tests/{tc}.in', 'w') as f:
            with redirect_stdout(f):
                test(n)
        tc += 1

if __name__ == '__main__':
    make_all(100000)
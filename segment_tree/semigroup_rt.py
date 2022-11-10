from __future__ import annotations
from math import log2, ceil
from typing import Callable, TypeVar, Union, Iterable
import operators
from operators import default_transfers, lift_alternative, lift_transfer


def lift_left(f):
    def new_f(a, b):
        if b is None:
            return a
        else:
            return f(a, b)
    return new_f


'''
This variation does not require an ids 
_update ranges range over [0, n) not [0, N)

'''
class SemigroupRT():

    Q = TypeVar('Q')
    U = TypeVar('U')

    def __init__(self: SemigroupRT,
                 arr: Union[Iterable[Q], int],
                 update_plus: Callable[[U, U], U] = operators.snd,
                 query_plus: Callable[[Q, Q], Q] = operators.add,
                 transfer_op: Union[Callable[[Q, U, int, int], Q], str]
                 = None
                 ):

        if transfer_op is None and (update_plus, query_plus) in default_transfers:
            transfer_op: Callable[[self.Q, self.U, int, int],
                                  self.Q] = default_transfers[(update_plus, query_plus)]

        self.query_plus = lift_alternative(query_plus)
        self.update_plus = lift_alternative(update_plus)
        self.transfer = transfer_op

        if isinstance(arr, int):
            self.n = arr
            self.N = 2**ceil(log2(self.n))
            self.qarr = [None]*(2*self.N)
            self.uarr = [None]*(2*self.N)

        elif isinstance(arr, Iterable):
            self.n = len(arr)
            self.N = 2**ceil(log2(self.n))
            self.qarr = [None]*self.N + list(arr) + [None]*(self.N-self.n)
            self.uarr = [None]*(2*self.N)

        else:
            raise TypeError

        # evaluating the tree at all the intermediate segments
        for i in range(N-1, 0, -1):
            if self.qarr[i*2+1] is None:
                self.qarr[i] = self.qarr[i*2]
            else:
                self.qarr[i] = self.query_plus(self.qarr[i*2], self.qarr[i*2+1])

    def push(self: SemigroupRT,
             i: int,
             istart: int,
             iend: int
             ):
        if self.uarr[i] == None: return # Speed boost

        self.qarr[i] = self.transfer(self.qarr[i], self.uarr[i], istart, iend)

        if i < self.N:
            self.uarr[i*2] = self.update_plus(self.uarr[i*2], self.uarr[i])
            self.uarr[i*2+1] = self.update_plus(self.uarr[i*2+1], self.uarr[i])

        self.uarr[i] = None

    def update(self: SemigroupRT,
               start: int,
               end: int,
               value: U
               ):
        self._update(start, end, value, 1, 0, self.n)

    def query(self: SemigroupRT,
              start: int,
              end: int,
              ):
        return self._update(start, end, self.update_id, 1, 0, self.N)

    def _update(self: SemigroupRT,
                start: int,
                end: int,
                value: U,
                i: int,
                istart: int,
                iend: int
                ):
        self.push(i, istart, iend)

        # The query/update range is entirely outside of the segment
        if end <= istart or start >= iend:
            return None  # only queries

        # The query/update range entirely contains the segment
        elif start <= istart and end >= iend:
            self.uarr[i] = value  # only updates
            self.push(i, istart, iend)  # only updates

            return self.qarr[i]  # only queries

        # The segment partially overlaps query/update range
        # We query/update both children
        else:
            imid = (istart + iend) // 2
            left = self._update(start, end, value, 2*i, istart, imid)
            right = self._update(start, end, value, 2*i+1, imid, iend)
            self.qarr[i] = self.query_plus(
                self.qarr[i*2], self.qarr[i*2+1])  # only updates

            return self.query_plus(left, right)  # only queries

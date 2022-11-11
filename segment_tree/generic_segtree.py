from __future__ import annotations
from math import log2, ceil
from typing import Callable, TypeVar, Union, Iterable
import operators
from operators import DEFAULT, ids, transfers, lift, lift_transfer

class RangeTree():

    Q = TypeVar('Q')
    U = TypeVar('U')

    def __init__(self: RangeTree,
                 arr: Union[Iterable[Q], int],
                 query_plus: Callable[[Q, Q], Q] = operators.sum,
                 update_plus: Callable[[U, U], U] = operators.snd,
                 query_id: Union[Q, str] = DEFAULT,
                 update_id: Union[U, str] = DEFAULT,
                 transfer_op: Union[Callable[[Q, U, int, int], Q], str]
                 = DEFAULT
                 ):


        lift_required = False


        if update_id is DEFAULT:
            try:
                update_id = ids[update_plus]
            except KeyError:
                update_id = None
                update_plus = lift(update_plus)
                lift_required = True

        if query_id is DEFAULT:
            try:
                query_id = ids[query_plus]
            except KeyError:
                query_id = None
                query_plus = lift(query_plus)
                lift_required = True

        if transfer_op is DEFAULT:
            if (query_plus, update_plus) in transfers:
                transfer_op = transfers[(update_plus, query_plus)]
            else:
                raise ValueError

        if lift_required:
            transfer_op = lift_transfer(transfer_op)

        self.query_plus = query_plus  
        self.update_plus = update_plus
        self.query_id = query_id
        self.update_id = update_id
        self.transfer = transfer_op

        if isinstance(arr, int):
            n = arr
            N = 2**ceil(log2(n))
            self.N = N
            self.qarr = [query_id]*(2*N)
            self.uarr = [update_id]*(2*N)

        elif isinstance(arr, Iterable):
            n = len(arr)
            N = 2**ceil(log2(n))
            self.N = N
            self.qarr = [query_id]*N + list(arr) + [query_id]*(N-n)
            self.uarr = [update_id]*(2*N)

        else:
            raise TypeError

        # initialising the tree at all the intermediate segments
        for i in range(N-1, 0, -1):
            self.qarr[i] = self.query_plus(self.qarr[i*2], self.qarr[i*2+1])


    def push(self: RangeTree,
             i: int,
             istart: int,
             iend: int
             ):
        self.qarr[i] = self.transfer(self.qarr[i], self.uarr[i], istart, iend)

        if i < self.N:
            self.uarr[i*2] = self.update_plus(self.uarr[i*2], self.uarr[i])
            self.uarr[i*2+1] = self.update_plus(self.uarr[i*2+1], self.uarr[i])

        self.uarr[i] = self.update_id


    def update(self: RangeTree,
               start: int,
               end: int,
               value: U
               ):
        self._update(start, end, value, 1, 0, self.N)


    def query(self: RangeTree,
              start: int,
              end: int,
              ):
        return self._update(start, end, self.update_id, 1, 0, self.N)


    def _update(self: RangeTree,
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
            return self.query_id  # only queries

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

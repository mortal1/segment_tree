from __future__ import annotations
from copy import copy, deepcopy
from math import log2, ceil
from typing import Callable, TypeVar, Union, Iterable
import operators
from operators import default_ids, default_transfers


class GenericSegmentTree():

    Q = TypeVar('Q')
    U = TypeVar('U')

    def __init__(self: GenericSegmentTree,
                 arr: Union[Iterable[Q], int],
                 update_add: Callable[[U, U], U] = operators.snd,
                 update_id: Union[U, str] = None,
                 query_add: Callable[[Q, Q], Q] = operators.add,
                 query_id: Union[Q, str] = None,
                 transfer_op: Union[Callable[[Q, U, int, int], Q], str]
                 = None
                 ):

        if update_id is None and update_add in default_ids:
            update_id: self.U = default_ids[update_add]
        if query_id is None and query_add in default_ids:
            query_id: self.Q = default_ids[query_add]
        if transfer_op is None and (update_add, query_add) in default_transfers:
            transfer_op: Callable[[self.Q, self.U, int, int],
                                  self.Q] = default_transfers[(update_add, query_add)]

        self.query_add = query_add
        self.query_id = query_id
        self.update_add = update_add
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

        # evaluating the tree at all the intermediate segments
        for i in range(N-1, 0, -1):
            self.qarr[i] = self.qarr[i*2] + self.qarr[i*2+1]

    def push(self: GenericSegmentTree,
             i: int,
             istart: int,
             iend: int
             ):
        self.qarr[i] = self.transfer(self.qarr[i], self.uarr[i], istart, iend)

        if i < self.N:
            self.uarr[i*2] = self.update_add(self.uarr[i*2], self.uarr[i])
            self.uarr[i*2+1] = self.update_add(self.uarr[i*2+1], self.uarr[i])

        self.uarr[i] = self.update_id

    def update(self: GenericSegmentTree,
               start: int,
               end: int,
               value: U
               ):
        self._update(start, end, value, 1, 0, self.N)

    def query(self: GenericSegmentTree,
              start: int,
              end: int,
              ):
        return self._update(start, end, self.update_id, 1, 0, self.N)

    def _update(self: GenericSegmentTree,
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
            self.qarr[i] = self.query_add(
                self.qarr[i*2], self.qarr[i*2+1])  # only updates

            return self.query_add(left, right)  # only queries

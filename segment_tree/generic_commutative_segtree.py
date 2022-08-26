from __future__ import annotations
from copy import copy, deepcopy
from math import log2, ceil
from typing import Callable, TypeVar, Union, Iterable
import operators
from operators import default_ids, default_transfers


class GenericCommutativeTree():

    Q = TypeVar('Q')
    U = TypeVar('U')

    def __init__(self: GenericCommutativeTree,
                 arr: Union[Iterable[Q], int],
                 update_add: Callable[[U, U], U] = operators.add,
                 update_id: Union[U, str] = 'default',
                 query_add: Callable[[Q, Q], Q] = operators.add,
                 query_id: Union[Q, str] = 'default',
                 transfer_op: Union[Callable[[U, Q, int, int], Q], str]
                 = 'default'
                 ):

        if update_id == 'default':
            update_id: self.Q = default_ids[update_add]
        if query_id == 'default':
            query_id: self.Q = default_ids[query_add]
        if transfer_op == 'default':
            transfer_op: Callable[[self.U, self.Q, int, int],
                                  self.Q] = default_transfers[(update_add, query_add)]

        self.query_add = query_add
        self.query_id = query_id
        self.update_add = update_add
        self.update_id = update_id
        self.transfer = transfer_op

        if isinstance(arr, int):
            k = arr
            n = 2**ceil(log2(k))
            self.n = n
            self.qarr = [query_id]*(2*n)
            self.uarr = [update_id]*(2*n)

        elif isinstance(arr, Iterable):
            k = len(arr)
            n = 2**ceil(log2(k))
            self.n = n
            self.qarr = [query_id]*n + list(arr) + [query_id]*(n-k)
            self.uarr = [update_id]*(2*n)

        else:
            raise TypeError

        # evaluating the tree at all the intermediate segments
        for i in range(n-1, -1, -1):
            self.qarr[i] = self.qarr[i*2] + self.qarr[i*2+1]

    def update(self: GenericCommutativeTree,
               start: int,
               end: int,
               value: U
               ):
        self._update(start, end, value, 1, 0, self.n)

    def query(self: GenericCommutativeTree,
              start: int,
              end: int,
              ):
        return self._update(start, end, self.update_id, 1, 0, self.n)

    def _update(self: GenericCommutativeTree,
                start: int,
                end: int,
                value: U,
                i: int,
                istart: int,
                iend: int
                ):

        if istart >= end or iend <= start:
            return self.query_id  # only queries

        elif istart >= start and iend <= end:
            self.uarr[i] = self.update_add(value, self.uarr[i])  # only updates
            self.qarr[i] = self.transfer(
                value, self.qarr[i], istart, iend)  # only updates

            return self.qarr[i]  # only queries

        else:
            imid = (istart + iend) // 2
            left = self._update(start, end, value, 2*i, istart, imid)
            right = self._update(start, end, value, 2*i+1, imid, iend)
            self.qarr[i] = self.transfer(self.uarr[i],
                                         self.query_add(
                                             self.qarr[i*2], self.qarr[i*2+1]),
                                         istart, iend
                                         )  # only updates

            return self.transfer(self.uarr[i],
                                 self.query_add(left, right),
                                 max(start, istart), min(end, iend)
                                 )  # only queries


'''
NOTES
- In the commutative tree, information is duplicated in each level of the tree - The update is written in uarr[i] and qarr[i] at the same time. The conceptual basis for this is that qarr[i] or any evaluated query at [i] needs to pull from the two children and from uarr[i]. Since it's commutative, the update stays there, so it needs to be reused every time. In a pushing tree, the values need to move around, so the guarantee of no duplicated values is more useful.
'''

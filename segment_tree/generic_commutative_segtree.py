from __future__ import annotations
from typing import Callable, TypeVar, Union, Iterable
import operators
from operators import DEFAULT
from generic_segtree import RangeTree


class CommutativeTree(RangeTree):

    Q = TypeVar('Q')
    U = TypeVar('U')

    
    def __init__(self: CommutativeTree,
                 arr: Union[Iterable[Q], int],
                 query_plus: Callable[[Q, Q], Q] = operators.sum,
                 update_plus: Callable[[U, U], U] = operators.snd,
                 query_id: Union[Q, str] = DEFAULT,
                 update_id: Union[U, str] = DEFAULT,
                 transfer_op: Union[Callable[[Q, U, int, int], Q], str]
                 = DEFAULT
                 ):
        super().__init__(arr, query_plus, update_plus, query_id, update_id, transfer_op)

    def _update(self: CommutativeTree,
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
            self.uarr[i] = self.update_plus(self.uarr[i], value)  # only updates
            self.qarr[i] = self.transfer(
                self.qarr[i], value, istart, iend
                )  # only updates

            return self.qarr[i]  # only queries

        else:
            imid = (istart + iend) // 2
            left = self._update(start, end, value, 2*i, istart, imid)
            right = self._update(start, end, value, 2*i+1, imid, iend)

            self.qarr[i] = self.transfer(
                self.query_plus(self.qarr[i*2], self.qarr[i*2+1]), 
                self.uarr[i], istart, iend
                )  # only updates

            return self.transfer(self.query_plus(left, right),
                self.uarr[i],
                max(start, istart), min(end, iend)
                )  # only queries


'''
NOTES
- In the commutative tree, information is duplicated in each level of the tree - The update is written in uarr[i] and qarr[i] at the same time. The conceptual basis for this is that qarr[i] or any evaluated query at [i] needs to pull from the two children and from uarr[i]. Since it's commutative, the update stays there, so it needs to be reused every time. In a pushing tree, the values need to move around, so the guarantee of no duplicated values is more useful.
'''

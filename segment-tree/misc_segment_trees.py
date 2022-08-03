from copy import copy, deepcopy
from math import log2, floor
from typing import Callable, TypeVar, Union, Iterable
import operators
from operators import default_ids, default_transfers

# incomplete


class StrictBottomUpSetSumSegmentTree():

    def __init__(self, arr):
        self.n = len(arr)
        self.arr = [0]*self.n + deepcopy(arr)
        self.update = [-1]*(self.n*2)

    def query(self, start, end):
        start += self.n
        end += self.n
        sum = 0

        while end > start:
            if start & 1:
                sum += self.arr[start]
                start += 1
            if end & 1:
                sum += self.arr[end-1]
                end -= 1
            start /= 2
            end /= 2

    def update(self, start, end):
        start += self.n
        end += self.n
        sum = 0

        while end > start:
            if start & 1:
                sum += self.arr[start]
                start += 1
            if end & 1:
                sum += self.arr[end-1]
                end -= 1
            start /= 2
            end /= 2


class SetSumSegmentTree():

    def __init__(self, n):
        self.n = int(2**(floor(log2(n-1))+1))
        self.qarr = [0]*(2*self.n)
        self.uarr = [None]*(2*self.n)

    def push(self, i, istart, iend):
        if self.uarr[i] is None:
            return

        self.qarr[i] = self.uarr[i] * (iend-istart)

        if i < self.n:
            self.uarr[i*2] = self.uarr[i]
            self.uarr[i*2+1] = self.uarr[i]

        self.uarr[i] = None

    def update(self, start, end, value):
        return self._update(start, end, value, 1, 0, self.n)

    def query(self, start, end):
        return self._update(start, end, None, 1, 0, self.n)

    def _update(self, start, end, value, i, istart, iend):
        self.push(i, istart, iend)

        if end <= istart or start >= iend:
            return 0

        elif start <= istart and end >= iend:
            if value is not None:
                self.uarr[i] = value
            self.push(i, istart, iend)

            # print(locals(), self.__dict__)
            return self.qarr[i]

        else:
            imid = (istart + iend) // 2
            left = self._update(start, end, value, 2*i, istart, imid)
            right = self._update(start, end, value, 2*i+1, imid, iend)
            if value is not None:
                self.qarr[i] = self.qarr[i*2] + self.qarr[i*2+1]

            # print(locals(), self.__dict__)
            return left + right


class GenericSegmentTree():

    Q = TypeVar('Q')
    U = TypeVar('U')

    def __init__(self: 'GenericSegmentTree',
                 arr: Union[Iterable[Q], int],
                 update_add: Callable[[U, U], U] = operators.snd,
                 update_id: Union[U, str] = 'default',
                 query_add: Callable[[Q, Q], Q] = operators.add,
                 query_id: Union[Q, str] = 'default',
                 transfer_op: Union[Callable[[U, Q, int, int], Q], str]
                 = 'default'
                 ):

        if query_id == 'default':
            query_id = default_ids[query_add]
        if update_id == 'default':
            update_id = default_ids[update_add]
        if transfer_op == 'default':
            transfer_op = default_transfers[(query_add, update_add)]

        self.query_add = query_add
        self.query_id = query_id
        self.update_add = update_add
        self.update_id = update_id
        self.transfer = transfer_op

        if isinstance(arr, int):
            n = int(2**(floor(log2(arr-1))+1))
            self.n = n
            self.qarr = [query_id]*(2*self.n)
            self.uarr = [update_id]*(2*self.n)

        elif isinstance(arr, Iterable):
            n = int(2**(floor(log2(len(arr)-1))+1))
            self.n = n
            self.qarr = [query_id]*n + list(arr) + [query_id]*(n-len(arr))
            self.uarr = [update_id]*(2*n)

        else:
            raise TypeError

    def push(self: 'GenericSegmentTree',
             i: int,
             istart: int,
             iend: int
             ):
        self.qarr[i] = self.transfer(self.uarr[i], self.qarr[i], istart, iend)

        if i < self.n:
            self.uarr[i*2] = self.update_add(self.uarr[i], self.uarr[i*2])
            self.uarr[i*2+1] = self.update_add(self.uarr[i], self.uarr[i*2+1])

        self.uarr[i] = self.update_id

    def update(self: 'GenericSegmentTree',
               start: int,
               end: int,
               value: U
               ):
        self._update(start, end, value, 1, 0, self.n)

    def query(self: 'GenericSegmentTree',
              start: int,
              end: int,
              ):
        return self._update(start, end, self.update_id, 1, 0, self.n)

    def _update(self: 'GenericSegmentTree',
                start: int,
                end: int,
                value: U,
                i: int,
                istart: int,
                iend: int
                ):
        self.push(i, istart, iend)

        if istart >= end or iend <= start:
            return self.query_id  # only queries

        elif istart >= start and iend <= end:
            self.uarr[i] = self.update_add(value, self.uarr[i])  # only updates
            self.push(i, istart, iend)  # only updates

            return self.qarr[i]  # only queries

        else:
            imid = (istart + iend) // 2
            left = self._update(start, end, value, 2*i, istart, imid)
            right = self._update(start, end, value, 2*i+1, imid, iend)
            self.qarr[i] = self.query_add(
                self.qarr[i*2], self.qarr[i*2+1])  # only updates

            return self.query_add(left, right)  # only queries

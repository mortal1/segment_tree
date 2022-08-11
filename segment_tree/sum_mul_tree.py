from __future__ import annotations
from copy import copy, deepcopy
from math import log2, ceil
from typing import Callable, TypeVar, Union, Iterable
import operators
from operators import default_ids, default_transfers


class SumMulTree():

    def __init__(self, arr):

        if isinstance(arr, int):
            k = arr
            n = 2**ceil(log2(k))
            self.n = n
            self.qarr = [0]*n + [1]*k + [0]*(n-k)
            self.uarr = [1]*(2*self.n)

        elif isinstance(arr, Iterable):
            k = len(arr)
            n = 2**ceil(log2(k))
            self.n = n
            self.qarr = [0]*n + list(arr) + [0]*(n-k)
            self.uarr = [1]*(2*n)

        # evaluating the tree at all the intermediate segments
        for i in range(self.n-1, -1, -1):
            self.qarr[i] = self.qarr[i*2] + self.qarr[i*2+1]

    def update(self, start, end, value):
        self._update(start, end, value, 1, 0, self.n)

    def query(self, start, end):
        return self._update(start, end, 1, 1, 0, self.n)


    def _update(self, start, end, value, i, istart, iend):
        if istart >= end or iend <= start:
            return 0  # only queries

        elif istart >= start and iend <= end:
            self.uarr[i] = value * self.uarr[i]  # only updates

            return self.uarr[i] * self.qarr[i]  # only queries

        else:
            imid = (istart + iend) // 2
            left = self._update(start, end, value, 2*i, istart, imid)
            right = self._update(start, end, value, 2*i+1, imid, iend)
            self.qarr[i] = self.uarr[i*2] * self.qarr[i*2] + \
                self.uarr[i*2+1] * self.qarr[i*2+1]  # only updates

            return self.uarr[i] * (left + right)  # only queries

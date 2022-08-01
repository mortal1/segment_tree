from copy import copy, deepcopy
from math import log2, floor

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


    # def _query(self, start, end, i, istart, iend):
    #     self.push(i, istart, iend)
    #     if start <= istart and end >= iend:
    #         return self.qarr[i]

    #     elif end <= istart or start >= iend:
    #         return 0

    #     else:
    #         mid = (istart + iend) // 2
    #         left = self._query(self, start, end, 2*i, istart, mid)
    #         right = self._query(self, start, end, 2*i+1, mid, iend)
    #         return left + right
    


class GenericSetSumSegmentTree():

    u_id = None
    q_id = 0

    def __init__(self, n):
        self.n = int(2**(floor(log2(n-1))+1))
        self.qarr = [0]*(2*self.n)
        self.uarr = [None]*(2*self.n)

    # def mid(start, end):
    #     return (start + end) / 2

    def merge_uu(a, b):
        if a is not None:
            return a
        else:
            return b

    def merge_qq(a, b):
        return a + b

    def merge_uq(u, q, istart, iend):
        if u is not None:
            return u * (iend-istart)
        else:
            return q

    def push(self, i, istart, iend):
        if self.uarr[i] == self.u_id:
            return
        
        self.qarr[i] = self.merge_uq(self.uarr[i], self.qarr[i], istart, iend)

        if i < self.n:
            self.uarr[i*2] = self.merge_uu(self.uarr[i], self.uarr[i*2])
            self.uarr[i*2+1] = self.merge_uu(self.uarr[i], self.uarr[i*2+1])

        self.uarr[i] = self.u_id

    def update(self, start, end, value):
        return self._update(self, start, end, value, None, 1, 0, self.n)

    def query(self, start, end):
        return self._update(self, start, end, None, None, 1, 0, self.n)


    def _update(self, start, end, value, i, istart, iend):
        self.push(i, istart, iend)
        if end <= istart or start >= iend:
            pass

        elif start <= istart and end >= iend:
            self.update_vals[i] = self.merge_uu(value, self.update_vals[i])
            self.push(i, istart, iend)

            
        else:
            mid = self.mid(istart, iend)
            off_value = self.setval(off_value, self.uarr[i])
            left = self._update(self, start, end, value, 2*i, istart, mid)
            right = self._update(self, start, end, value, 2*i+1, mid, iend)
            self.query_vals[i] = \
                self.merge_qq(
                    self.merge_,
                    )
        
        return self.query_vals[i]

    # copied code
#    def _update(self, start, end, value, i, istart, iend):
#         if end <= istart or start >= iend:
#             return 0

#         elif start <= istart and end >= iend:
#             if value is not None:
#                 self.uarr[i] = value
#             self.push(i, istart, iend)

#             print(locals(), self.__dict__)
#             return self.qarr[i]

#         else:
#             self.push(i, istart, iend)

#             mid = (istart + iend) // 2
#             left = self._update(start, end, value, 2*i, istart, mid)
#             right = self._update(start, end, value, 2*i+1, mid, iend)
#             if value is not None:
#                 self.qarr[i] = left + right

#             print(locals(), self.__dict__)
#             return self.qarr[i]

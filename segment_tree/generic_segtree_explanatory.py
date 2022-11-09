from math import log2, ceil

# The default operators used for the segment tree


def snd(a, b):
    # Returns the second value if it exists. Behaves like "set a to b"
    if b is not None:
        return b
    else:
        return a


snd_id = None


def add(a, b):
    return a + b


add_id = 0


def snd_add(q, u, istart, iend):
    # Defines the sum of a segment if it is entirely set to one value
    if u is not None:
        return u * (iend - istart)
    else:
        return q


class GenericSegmentTree():

    def __init__(self,
                 arr,
                 update_add=snd,
                 update_id=snd_id,
                 query_add=add,
                 query_id=add_id,
                 transfer_op=snd_add
                 ):

        self.query_add = query_add  # Adds two query values
        self.query_id = query_id  # The "zero" query value
        self.update_add = update_add  # Adds two update values
        self.update_id = update_id  # The "zero" update value
        self.transfer = transfer_op  # Applies an update to a query range

        # Initialises the range tree with a size of the nearest power of 2
        n = len(arr)
        N = 2**ceil(log2(n))
        self.N = N

        # Array of query values
        self.qarr = [query_id]*N + list(arr) + [query_id]*(N-n)

        # Array of update values
        self.uarr = [update_id]*(2*N)

        # Evaluating the tree at all the intermediate segments
        for i in range(n-1, 0, -1):
            self.qarr[i] = self.qarr[i*2] + self.qarr[i*2+1]

    # Processes an update in the update tree,

    def push(self, i, istart, iend):

        # Transfers it horisontally to the query tree
        self.qarr[i] = self.transfer(self.qarr[i], self.uarr[i], istart, iend)

        # Pushes it down to its two children in the update tree
        if i < self.N:
            self.uarr[i*2] = self.update_add(self.uarr[i*2], self.uarr[i])
            self.uarr[i*2+1] = self.update_add(self.uarr[i*2+1], self.uarr[i])

        # Deletes it
        self.uarr[i] = self.update_id

    def update(self, start, end, value):  # no return
        self._update(start, end, value, 1, 0, self.N)

    def query(self, start, end):  # updates with update_id
        return self._update(start, end, self.update_id, 1, 0, self.N)

    def _update(self, start, end, value, i, istart, iend):
        self.push(i, istart, iend)

        # The query/update range is entirely outside of the segment
        if end <= istart or start >= iend:
            return self.query_id  # only queries

        # The query/update range entirely contains the segment
        elif start <= istart and end >= iend:
            self.uarr[i] = self.update_add(self.uarr[i], value)  # only updates
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

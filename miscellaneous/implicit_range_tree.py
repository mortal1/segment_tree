'''
Implementing a range-sum, range-add, implicit range tree.
This means that it can range over [1,1e9] without storing excess memory

implemented with pushing
'''


from dataclasses import dataclass

@dataclass
class Node():
    def __init__(self, qval=0, uval=0, left=-1, right=-1):
        self.qval = qval
        self.uval = uval
        self.left = left
        self.right = right

N = 8
P = 1
tree = [Node()]


def push(i, istart, iend):
    tree[i].qval = tree[i].qval + tree[i].uval * (iend - istart)

    if i < N:
        if tree[i].left == -1:
            tree[i].left = len(tree)
            tree.append(Node())
            tree[i].right = len(tree)
            tree.append(Node())
 
        tree[tree[i].left].uval += tree[i].uval
        tree[tree[i].right].uval += tree[i].uval

    tree[i].uval = 0


def update(start, end, value, i=1, istart=0, iend=N):
    push(i, istart, iend)

    if end <= istart or start >= iend:
        return

    elif start <= istart and end >= iend:
        tree[i].uval = value
        push(i, istart, iend)

    else:
        imid = (istart + iend) // 2
        update(start, end, value, 2*i, istart, imid)
        update(start, end, value, 2*i+1, imid, iend)

        tree[i].qval = tree[i*2].qval + tree[i*2+1].qval


def query(start, end, i=1, istart=0, iend=N):

    if end <= istart or start >= iend:
        return 0

    elif start <= istart and end >= iend:
        return tree[i].qval

    else:
        imid = (istart + iend) // 2
        left = query(start, end, 2*i, istart, imid)
        right = query(start, end, 2*i+1, imid, iend)

        return left + right
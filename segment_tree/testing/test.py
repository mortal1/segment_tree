from misc_segment_trees import SetSumSegmentTree as ST
import sys, os
from glob import glob
from contextlib import redirect_stdin, redirect_stdout


def runTree(st):
    n, m = (int(i) for i in input().split())
    arr = [int(i) for i in input().split()]
    tree = st(arr)

    for _ in range(m):
        instr, *vals = input().split()
        if instr == 'U':
            s, e, v = map(int, vals)
            tree.update(s, e, v)
        elif instr == 'Q':
            s, e = map(int, vals)
            print(tree.query(s, e))


def produce(st, infolder=None, outfolder=None, tag = ''):
    if infolder is None:
        infolder = f'{os.path.dirname(__file__)}/tests'

    if outfolder is None:
        outfolder = f'{os.path.dirname(__file__)}/tmp'
    
    for file in glob(f'{infolder}/*.in'):
        with open(file) as f:
            with redirect_stdin(f):
                runTree(st)
                pass
    
    return


def main():
    st = ST(10)
    print(st.values)
    return


if __name__ == '__main__':
    main()
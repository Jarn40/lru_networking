'''Accepts two lines (x1,x2) and (x3,x4) on the
x-axis and returns whether they overlap. '''
from __future__ import print_function
import sys


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print('Please call this program providing the right arguments.Example: program.py x1 x2 x3 x4')
        exit()

    LINE_1 = set(range(int(sys.argv[1]), int(sys.argv[2])+1))
    LINE_2 = set(range(int(sys.argv[3]), int(sys.argv[4])+1))

    print(bool(LINE_1.intersection(LINE_2)))

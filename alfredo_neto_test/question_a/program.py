'''Accepts two lines (x1,x2) and (x3,x4) on the
x-axis and returns whether they overlap. '''
from __future__ import print_function
import sys


def has_intersection(x1, x2, x3 ,x4):
    '''function that checks if 2 lines intesects
    :rbool'''
    line_1 = set(range(min(x1, x2), max(x1, x2)+1))
    line_2 = set(range(min(x3, x4), max(x3, x4)+1))
    # print(line_1)
    return bool(line_1.intersection(line_2))



if __name__ == "__main__":

    if len(sys.argv) != 5:
        print('Please call this program providing the right arguments.Example: program.py x1 x2 x3 x4')
        sys.exit()

    print(has_intersection(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])))

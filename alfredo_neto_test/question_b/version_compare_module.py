'''This file serve as a module as well stand alone file with inputs
    I opted to use all statments GREATER, LOWER and EQUAL, instead of sort the Greater one.
'''
from __future__ import print_function
import sys

def version_compare(v_1, v_2):
    '''Actual function for version comparison'''
    v_1, v_2 = float(v_1), float(v_2)
    if v_1 > v_2:
        return f'Version {v_1} is greater than {v_2}'

    if v_1 < v_2:   
        return f'Version {v_1} is lower than {v_2}'

    return f'{v_1} is equal to {v_2}'

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Please call this program providing the right arguments.Example: version_compare.py version1 version2')
        exit()
    print(version_compare(sys.argv[1], sys.argv[2]))
    
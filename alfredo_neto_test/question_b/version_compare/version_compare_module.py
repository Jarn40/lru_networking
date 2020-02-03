'''This file serve as a module as well stand alone file with inputs
    I opted to use all statments GREATER, LOWER and EQUAL, instead of sort the Greater one.
'''
from __future__ import print_function
import sys

def version_compare(v_1, v_2):
    '''Actual function for version comparison'''
    check_v_1, check_v_2 = str(v_1).split('.'), str(v_2).split('.')

    size_1 = len(check_v_1)
    size_2 = len(check_v_2)

    if size_1 > size_2:
        dif = size_1 - size_2
        [check_v_2.append('0') for i in range(dif)]
    else:
        dif = size_2 - size_1
        [check_v_1.append('0') for i in range(dif)]

    for dec in range(len(check_v_1)):
        if check_v_1[dec] > check_v_2[dec]:
            return f'Version {v_1} is greater than {v_2}'
        elif check_v_1[dec] < check_v_2[dec]:
            return f'Version {v_1} is lower than {v_2}'

    return f'{v_1} is equal to {v_2}'

if __name__ == "__main__":
    '''Can be used as a standAlone module if wanted'''
    if len(sys.argv) != 3:
        print('Please call this program providing the right arguments.Example: version_compare.py version1 version2')
        sys.exit()
    print(version_compare(sys.argv[1], sys.argv[2]))

from .__init__ import *


def binaryToHexFunc(max_dig=10, format='string'):
    problem = ''
    for i in range(random.randint(1, max_dig)):
        temp = str(random.randint(0, 1))
        problem += temp

    if format == 'string':
        solution = hex(int(problem, 2))
        return problem, solution
    else:
        return problem, solution


binary_to_hex = Generator("Binary to Hexidecimal", 64, binaryToHexFunc,
                          ["max_dig=10"])

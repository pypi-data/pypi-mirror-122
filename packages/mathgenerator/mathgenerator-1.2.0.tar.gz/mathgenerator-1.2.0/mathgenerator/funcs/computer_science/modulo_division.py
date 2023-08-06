from .__init__ import *


def moduloFunc(maxRes=99, maxModulo=99, format='string'):
    a = random.randint(0, maxModulo)
    b = random.randint(0, min(maxRes, maxModulo))
    c = a % b if b != 0 else 0

    if format == 'string':
        problem = str(a) + "%" + str(b) + "="
        solution = str(c)
        return problem, solution
    else:
        return a, b, c


modulo_division = Generator("Modulo Division", 5, moduloFunc,
                            ["maxRes=99", "maxModulo=99"])

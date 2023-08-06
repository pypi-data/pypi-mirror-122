from .__init__ import *

import math


def euclidianNormFunc(maxEltAmt=20, format='string'):
    vec = [
        random.uniform(0, 1000) for i in range(random.randint(2, maxEltAmt))
    ]
    solution = math.sqrt(sum([i**2 for i in vec]))

    if format == 'string':
        problem = f"Euclidian norm or L2 norm of the vector{vec} is:"
        return problem, solution
    else:
        return vec, solution


eucldian_norm = Generator("Euclidian norm or L2 norm of a vector", 69,
                          euclidianNormFunc, ["maxEltAmt=20"])

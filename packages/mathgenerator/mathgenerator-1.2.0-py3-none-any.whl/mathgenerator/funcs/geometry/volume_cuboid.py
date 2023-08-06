from .__init__ import *


def volumeCuboid(maxSide=20, unit='m', format='string'):
    a = random.randint(1, maxSide)
    b = random.randint(1, maxSide)
    c = random.randint(1, maxSide)
    ans = a * b * c

    if format == 'string':
        problem = f"Volume of cuboid with sides = {a}{unit}, {b}{unit}, {c}{unit} is"
        solution = f"{ans} {unit}^3"
        return problem, solution
    else:
        return a, b, c, ans, unit


volume_cuboid = Generator("Volume of Cuboid", 36, volumeCuboid,
                          ["maxSide=20", "unit='m'"])

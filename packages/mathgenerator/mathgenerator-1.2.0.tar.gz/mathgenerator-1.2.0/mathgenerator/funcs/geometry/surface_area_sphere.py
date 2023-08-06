from .__init__ import *


def surfaceAreaSphere(maxSide=20, unit='m', format='string'):
    r = random.randint(1, maxSide)
    ans = 4 * math.pi * r * r

    if format == 'string':
        problem = f"Surface area of Sphere with radius = {r}{unit} is"
        solution = f"{ans} {unit}^2"
        return problem, solution
    else:
        return r, ans, unit


surface_area_sphere = Generator("Surface Area of Sphere", 60,
                                surfaceAreaSphere, ["maxSide=20", "unit='m'"])

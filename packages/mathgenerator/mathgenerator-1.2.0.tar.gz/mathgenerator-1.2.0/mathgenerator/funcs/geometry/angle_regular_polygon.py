from .__init__ import *


def regularPolygonAngleFunc(minVal=3, maxVal=20, format='string'):
    sideNum = random.randint(minVal, maxVal)
    problem = f"Find the angle of a regular polygon with {sideNum} sides"

    exteriorAngle = round((360 / sideNum), 2)
    solution = 180 - exteriorAngle

    if format == 'string':
        return problem, solution
    else:
        return sideNum, solution


angle_regular_polygon = Generator("Angle of a Regular Polygon", 29,
                                  regularPolygonAngleFunc,
                                  ["minVal=3", "maxVal=20"])

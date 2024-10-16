import math as mt

l1 = 55
l2 = 95
l3 = 120


def get_coordinate(q1, q2):
    y = l1 + mt.sin(q1 * mt.pi / 180) * l2 + mt.sin((q2 * mt.pi / 180) - mt.pi + (q1 * mt.pi / 180)) * l3
    x = l2 * mt.cos(q1 * mt.pi / 180) + l3 * mt.cos((q2 * mt.pi / 180) - mt.pi + (q1 * mt.pi / 180))
    return (x, y)


def get_angles(x, y):
    d = mt.sqrt(x ** 2 + (y - l1) ** 2)
    q1 = mt.atan((y - l1) / x)
    q2 = mt.acos((d ** 2 + l2 ** 2 - l3 ** 2) / (2 * l2 * d))
    q3 = mt.acos((l2 ** 2 + l3 ** 2 - d ** 2) / (2 * l2 * l3))
    result1 = (q1 + q2) * 180 / mt.pi
    result2 = q3 * 180 / mt.pi
    return (result1, result2)


re = (get_coordinate(140, 35))
print(re)
print(get_angles(150, -10))

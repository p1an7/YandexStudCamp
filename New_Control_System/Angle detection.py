import math

def calculate_slope_in_degrees(x1, y1, x2, y2):
    if x1 == x2:
        return 90
    slope = (y2 - y1) / (x2 - x1)
    angle_radians = math.atan(slope)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance



x1, y1 = 1, 2
x2, y2 = 4, 6

angle_degrees = calculate_slope_in_degrees(x1, y1, x2, y2)
print(f"Угол наклона прямой: {angle_degrees} градусов")

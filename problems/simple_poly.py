from geometry_objects.vector import Vector
from geometry_objects.point import Point


def simple_poly(points: list) -> list:

    # starting value
    bottom_most_index: int = 0

    # find the bottom-most point as follows:
    # 1. the bottom-most point must be the one with the lowest y value
    # 2. if two or more points satisfy 1., then choose the point with the lowest x
    for i in range(1, len(points)):

        if points[i].y < points[bottom_most_index].y:
            bottom_most_index = i

        elif points[i].y == points[bottom_most_index].y and points[i].x < points[bottom_most_index].x:
            bottom_most_index = i

    # swap bottom-most point with points[0]
    if points[bottom_most_index] != points[0]:
        points[bottom_most_index], points[0] = points[0], points[bottom_most_index]

    bottom_most = points[0]

    # create a dummy vector which we will use to sort other points, this vector is (bottom_most.x+1, bottom_most.y)
    dummy: Point = Point(bottom_most.x + 1, bottom_most.y)
    dummy_vector = Vector(head=bottom_most, tail=dummy)

    # sort the sublist points[1:] by calculating:
    # 1. angles between dummy_vector and the vector (head=bottom_most, tail=p)
    # 2. if there are more than one point p having same 1. sort them by their euclidean distance from bottom_most point
    points = sorted(points[1:],
                    key=lambda p:
                    (dummy_vector.angle_between(Vector(bottom_most, p)), bottom_most.euclidean_distance(p)))

    # return [bottom_most] + sorted sublist
    return [bottom_most] + points


print(simple_poly([Point(0, 3), Point(1, 1), Point(2, 2), Point(4, 4),
                   Point(0, 0), Point(1, 2), Point(3, 1), Point(3, 3)]))

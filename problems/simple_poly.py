from geometry_objects.point import Point
from geometry_objects.vector import Vector


def simple_poly(vertices: list) -> list:

    # find point with min y and max x coordinates
    index = vertices.index(min(vertices, key=lambda x: (x[1], -x[0])))

    # swap with first point
    vertices[0], vertices[index] = vertices[index], vertices[0]

    vertices = sorted(vertices, key=lambda x: (
        Vector(Point(*vertices[0]), Point(*x)).slope(), Point(*vertices[0]).euclidean_distance(Point(*x))
    ))

    bottom_most = Point(*vertices[0])

    k = -1

    while Point(*vertices[k]) != bottom_most and \
        Vector(bottom_most, Point(*vertices[k])).slope() == Vector(bottom_most, Point(*vertices[k-1])).slope():

        k -= 1

    return vertices[:k] + vertices[:len(vertices)+k-1:-1]


if __name__ == '__main__':

    l1 = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
    print('points: ', l1)
    print('simple poly: ', simple_poly(l1))

    l2 = [(0, 0), (0, 1), (1, 0), (0, -1), (0, -2), (0, -3)]
    print('points: ', l2)
    print('simple poly: ', simple_poly(l2))

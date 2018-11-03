from math import atan2
from math import pi
from math import sqrt

from data_structures.stack import Stack

# Time complexities for data structures can be found at https://wiki.python.org/moin/TimeComplexity


"""
    Created by mchahin at 11/2/2018
"""
"""
    Implementations in the following script are completely from scratch
    (not using other packages in this project)
"""


# reflects the math function sgn
def sgn(x: float) -> int:

    if x > 0.0:
        return 1
    elif x < 0.0:
        return -1
    return 0


# returns the orientation of point p3 from segment p1p2
def orientation(p1: tuple, p2: tuple, p3: tuple) -> int:

    a = (p2[0]-p1[0], p2[1]-p1[1])
    b = (p3[0]-p1[0], p3[1]-p1[1])

    return sgn(a[0]*b[1] - a[1]*b[0])


# Calculates slope of the vector with ending point as the point parameter
#   and the starting point from the (0, 0) point
def slope(point: tuple) -> float:

    x, y = point[0], point[1]

    theta = atan2(y, x)
    theta *= (180 / pi)
    return theta if y >= 0.0 else 360.0 + theta


# Calculates the Eucledian distance between two points represented
#   as the function parameters
def distance(point1: tuple, point2: tuple) -> float:
    return sqrt((point1[0]-point2[0])**2 + (point1[1] - point2[1])**2)


# Calculates the angle between vectors with ending points as the
#   function parameters
def angle_between(point1: tuple, point2: tuple) -> float:
    return slope((point2[0] - point1[0], point2[1] - point1[1]))


# Creates a simple polygon over a given set of vertices
# Algorithm complexity: O(nlogn)
def simple_polygon_over_points(vertices: list, clockwise: bool = False) -> list:

    # choose start point as the point with the min y coordinate
    # if more points satisfy the condition above then the point with the max x coordinate is chosen
    # start_point = min(vertices, key=lambda x: (x[1], -x[0]))

    start_point_index = get_point_index(vertices, x=True, max_x=False, max_y=True)
    vertices[0], vertices[start_point_index] = vertices[start_point_index], vertices[0]
    start_point = vertices[0]

    if not clockwise:
        return [vertices[0]] + sorted(vertices[1:], key=lambda x: (
            angle_between(x, start_point), distance(x, start_point)))[::-1]

    return [vertices[0]] + sorted(vertices[1:], key=lambda x: (
        angle_between(x, start_point), distance(x, start_point)))


def get_point_index(vertices, x: bool = False, y: bool = False, max_x: bool = True, max_y: bool = True):

    if x == y:
        raise SyntaxError('Method argument values x and y must be of different values.')

    i1: int = 0
    i2: int = 1

    if y:
        i1, i2 = i2, i1

    start_point_index: int = 0

    for i in range(1, len(vertices)):

        if vertices[i][i1] < vertices[start_point_index][0]:

            if not max_x:
                start_point_index = i

        elif vertices[i][i1] > vertices[start_point_index][0]:

            if max_x:
                start_point_index = i

        else:
            if vertices[i][i2] > vertices[start_point_index][1]:

                if max_y:
                    start_point_index = i

            elif vertices[i][i2] < vertices[start_point_index][1]:

                if not max_y:
                    start_point_index = i

    return start_point_index


def get_tangents(hull1: list, hull2: list, i1: int, i2: int) -> tuple:

    j1, j2 = i1, i2
    n1 = len(hull1)
    n2 = len(hull2)

    found_t: bool = False

    while not found_t:

        found_t = True

        if orientation(hull2[i2], hull1[i1], hull1[(n1 + i1 - 1) % n1]) < 0:
            i1 = (n1 + i1 - 1) % n1
            found_t = False

        if orientation(hull1[i1], hull2[i2], hull2[(n2 + j2 + 1) % n2]) > 0:
            i2 = (i2 + 1) % n2
            found_t = False

    found_t: bool = False

    while not found_t:

        found_t = True

        if orientation(hull2[j2], hull1[j1], hull1[(j1 + 1) % n1]) > 0:
            j1 = (j1 + 1) % n1
            found_t = False

        if orientation(hull1[j1], hull2[j2], hull2[(n2 + j2 - 1) % n2]) < 0:
            j2 = (j2 - 1) % n2
            found_t = False

    return (i1, j1), (i2, j2)


"""
    Ex 1.3

    Let E be an unsorted set of n segments that are the edges of a convex
    polygon. Describe an O(nlogn) algorithm that computes from E a list
    containing all vertices of the polygon, sorted in clockwise order.
"""


def hull_from_hull_segments(edges: list) -> list:

    vertices_set: set = set()

    for e in edges:

        vertices_set.add(e[0])
        vertices_set.add(e[1])

    return simple_polygon_over_points(list(vertices_set))


"""
    Ex 1.6 b)

    Let P be a non-convex polygon. Describe an algorithm that computes
    the convex hull of P in O(n) time.
"""


def hull_from_vertices(vertices: list) -> list:

    s: Stack = Stack()
    start_point_index = get_point_index(vertices, x=True, max_x=False, max_y=True)
    vertices = vertices[start_point_index:] + vertices[:start_point_index]

    s.push(vertices[0])
    s.push(vertices[1])

    for i in range(2, len(vertices)):

        while len(s) > 1 and orientation(s.second_last(), s.peek(), vertices[i]) > 0:
            s.pop()

        s.push(vertices[i])

    return s.list_from_stack()


"""
    Ex 1.8 a)
    
    Let P1 and P2 be two disjoint convex polygons with n vertices in total.
    Give an O(n) time algorithm that computes the convex hull of P1 ∪P2.
"""


def find_convex_union(hull1: list, hull2: list) -> list:
    h1_max_x = get_point_index(hull1, x=True, max_x=True)
    h2_min_x = get_point_index(hull2, x=True, max_x=False)

    tang1, tang2 = get_tangents(hull1, hull2, h1_max_x, h2_min_x)
    return hull1[:tang1[0]+1] + hull2[tang2[0]:tang2[1]+1] + hull1[tang1[1]:]

    # if hull1[h1_max_x][0] > hull2[h2_max_x][0]:
    #     hull1, hull2 = hull2, hull1
    #     h1_max_x, h2_max_x = h2_max_x, h1_max_x
    #
    # h2_min_x = get_point_index(hull2, x=True, max_x=False)
    #
    # # hull1 is to te hull2's left
    # if hull1[h1_max_x][0] < hull2[h2_min_x][0]:
    #     tang1, tang2 = get_tangents(hull1, hull2, h1_max_x, h2_min_x)
    #     print(tang1, tang2)
    #     return hull1[:tang1[0]] + hull2[tang2[0]:] + hull2[:tang2[1]+1:-1] + hull1[tang1[1]:]
    #
    # h1_max_y = get_point_index(hull1, y=True, max_y=True)
    # h2_max_y = get_point_index(hull2, y=True, max_y=True)
    #
    # if hull1[h1_max_y][1] < hull2[h2_max_y][1]:
    #     hull1, hull2 = hull2, hull1
    #     h1_max_y, h2_max_y = h2_max_y, h1_max_y
    #
    # h1_min_y = get_point_index(hull1, y=True, max_y=False)
    # tang1, tang2 = get_tangents(hull1, hull2, h1_min_y, h2_max_y)
    # return hull1[:tang1[0] + 1] + hull2[tang2[0]:tang2[1] + 1] + hull1[tang1[1]:]


if __name__ == '__main__':

    # l1 = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
    #
    # print('points: ', l1)
    # print('simple poly: ', simple_polygon_over_points(l1))
    #
    # l2 = [(0, 0), (0, 1), (1, 0), (0, -1), (0, -2), (0, -3)]
    #
    # print()
    # print('points: ', l2)
    # print('simple poly: ', simple_polygon_over_points(l2))
    #
    # print()
    # print('hull 1: ', hull_from_vertices(simple_polygon_over_points(l1)))
    #
    # print()
    # print('hull 2: ', hull_from_vertices(simple_polygon_over_points(l2)))
    #
    # points = [(0, 0), (0, 1), (1, 1), (2, 2), (1, -1), (3, 3), (3, 2), (3, 1), (3, 0), (3, -1), (3, -2), (3, -3)]
    #
    # print()
    # print('hull 2: ', hull_from_vertices(simple_polygon_over_points(points)))

    hull1 = [(0, 0), (0, 1), (1, 0)]
    hull2 = [(5, 1), (6, 0), (5, 0)]

    print(find_convex_union(hull1, hull2))

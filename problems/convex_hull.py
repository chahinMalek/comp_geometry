from geometry_objects.point import Point
from geometry_objects.vector import Vector
from problems.simple_poly import simple_poly


def find_centroid(vertices: list) -> Point:

    centroid: 'Point' = Point()

    for v in vertices:
        centroid += Point(*v)

    return centroid / len(vertices)


def get_edges(vertices: list) -> list:

    edges = []

    for i in range(len(vertices)-1):
        for j in range(i, len(vertices)):
            edges.append((vertices[i], vertices[j]))

    return edges


#   Assumption: list of edges is sorted in the way that every edge e_i has its start point same as the
#   e_{i-1} end point
def get_vertices(edges: list) -> list:
    return [e[0] for e in edges]


def get_hull_edges(vertices: list) -> list:

    size: int = len(vertices)
    edges = []
    fail_flag = -2

    for i in range(size - 1):
        for j in range(i+1, size):

            current_orientation = None

            for v in vertices:

                if v == vertices[i] or v == vertices[j]:
                    continue

                orientation = Point.orientation(Point(*vertices[i]), Point(*vertices[j]), Point(*v))

                if orientation == 0:
                    continue

                if current_orientation is None:
                    current_orientation = orientation
                    continue

                if current_orientation != orientation:
                    current_orientation = fail_flag
                    break

            if current_orientation is None or current_orientation == fail_flag:
                continue

            if current_orientation == -1:
                edges.append((vertices[i], vertices[j]))

            else:
                edges.append((vertices[j], vertices[i]))

    return edges


def sort_hull(edges: list) -> None:

    for i in range(len(edges)-1):

        for j in range(i+1, len(edges)):

            if edges[i][1] == edges[j][0]:

                if i+1 != j:
                    edges[i+1], edges[j] = edges[j], edges[i+1]

                break

    i = 0

    while i < len(edges)-1:

        current_v = edges[i]
        j = (i + 1) % len(edges)

        while j < len(edges):

            next_v = edges[j % len(edges)]

            if current_v[0] == next_v[0]:

                if Point.distance(current_v[0], current_v[1]) > Point.distance(next_v[0], next_v[1]):
                    edges.remove(edges[i])

                else:
                    edges.remove(edges[j % len(edges)])

            else:
                j += 1

        i += 1

    return None


def find_neighbour_edge(last_edge, edges: list):

    for e in edges:

        if e[1] == last_edge[0]:

            edges.remove(e)
            return e

    return None


def convex_hull_quad(vertices: list) -> list:

    hull = []

    for l in vertices:

        p_l = Point(l[0], l[1])
        is_in_hull = True

        for i in range(len(vertices) - 2):
            p_i = Point(vertices[i][0], vertices[i][1])

            for j in range(i+1, len(vertices) - 1):
                p_j = Point(vertices[j][0], vertices[j][1])

                for k in range(j+1, len(vertices)):
                    p_k = Point(vertices[k][0], vertices[k][1])

                    if p_i == p_l or p_j == p_l or p_k == p_l:
                        continue

                    if p_l.in_triangle(p_i, p_j, p_k):
                        is_in_hull = False
                        break

                if not is_in_hull:
                    break

            if not is_in_hull:
                break

        if is_in_hull:
            hull.append(l)

    return simple_poly(hull)


def convex_hull_cubic(vertices: list) -> list:

    hull = get_hull_edges(vertices)
    sort_hull(hull)
    return simple_poly(get_vertices(hull))


def convex_hull_jarvis_march(vertices: list) -> list:

    i: int = vertices.index(min(vertices, key=lambda x: (x[0], x[1])))
    vertices[0], vertices[i] = vertices[i], vertices[0]

    point: 'Point' = Point(vertices[i][0], vertices[i][1] + 1)
    vec = Vector(Point(*vertices[0]), point)

    j: int = vertices.index(
        min(vertices, key=lambda x: vec.angle_between(Vector(Point(*vertices[0]), Point(*x))))
    )

    vertices[1], vertices[j] = vertices[j], vertices[1]
    hull = vertices[:2]

    i: int = 0
    j: int = 1
    size: int = len(vertices)

    for k in range(2, size):

        p_j = Point(*vertices[j])
        p_i = Point(*vertices[i])

        v1 = Vector(p_j, p_i)
        # max_angle = -inf
        min_angle = 180.0 - v1.angle_between(Vector(p_j, Point(*hull[0])))
        min_dist = Point(*hull[0]).euclidean_distance(p_j)

        next = k

        for l in range(k, size):

            current_angle = 180.0 - v1.angle_between(Vector(p_j, Point(*vertices[l])))
            current_dist = p_j.euclidean_distance(Point(*vertices[l]))

            if current_angle < min_angle:
                next = l
                min_angle = current_angle

            # elif current_angle == min_angle and current_dist < min_dist:
            #     next = l
            #     min_angle = current_angle
            #     min_dist = current_dist

        print(v1, vertices[next], min_angle)

        if min_angle == 180.0 - v1.angle_between(Vector(p_j, Point(*hull[0]))):
            return hull

        if next != k:
            vertices[k], vertices[next] = vertices[next], vertices[k]

        hull.append(vertices[k])
        i += 1
        j += 1

    return hull


def convex_hull_graham_scan(vertices: list) -> list:

    vertices = simple_poly(vertices)
    hull = vertices[:2]

    for v in vertices[2:]:

        # edge case if only one point is in hull
        while len(hull) > 1 and Point.orientation(Point(*hull[-2]), Point(*hull[-1]), Point(*v)) < 0:
            hull.pop()

        hull.append(v)

    return hull


"""
    02.11.2018
"""


def divide_vertices(vertices: list, left_point: tuple) -> tuple:

    upper = []
    lower = []

    for v in vertices:

        if v[1] > left_point[1]:
            upper.append(v)
        else:
            lower.insert(0, v)

    return upper, lower


def graham_scan(vertices: list) -> list:

    vertices.sort()
    left_p = min(vertices)
    upper_vertices, lower_vertices = divide_vertices(vertices, left_p)

    upper_hull = find_hull(upper_vertices)
    lower_hull = find_hull(lower_vertices)

    return upper_hull + lower_hull


def find_hull(vertices: list) -> list:

    hull = vertices[:2]

    for v in vertices[2:]:

        while Point.orientation(Point(*hull[-2]), Point(*hull[-1]), Point(*v)) > 0:
            hull.pop()

        hull.append(v)

    return hull


if __name__ == '__main__':

    # points = [(2, 1), (1, 2), (1, 4), (4, -2), (1, 1)]
    # points = [(1, 1), (1, 2), (1, 3), (2, 2), (3, 3), (4, 4)]
    points = [(0, 0), (0, 1), (1, 1), (2, 2), (1, -1), (3, 3), (3, 2), (3, 1), (3, 0), (3, -1), (3, -2), (3, -3)]
    # print(convex_hull_quad(points))
    # print(convex_hull_cubic(points))
    # print(convex_hull_jarvis_march(points))
    print(convex_hull_graham_scan(points))
    print(graham_scan(points))

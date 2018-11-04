from berg_problems.chapter_1 import get_point_index
from berg_problems.chapter_1 import orientation
from geometry_objects.point import Point
from geometry_objects.vector import Vector
from problems.simple_poly import simple_poly

"""
    Utility functions for convex hull algorithms
"""


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


def orientate_vertices(p1: tuple, p2: tuple, p3: tuple) -> tuple:

    points = [p1, p2, p3]

    points.sort(key=lambda x: x[0])

    ori = orientation(points[0], points[1], points[2])

    if ori > 0:
        return points[0], points[2], points[1]

    else:
        return tuple(points)


def find_closest_point_index(vertices: list, p: tuple) -> int:

    min_dist_index: int = 0
    min_dist = Point.distance(Point(*vertices[0]), Point(*p))

    for i in range(1, len(vertices)):

        current_distance = Point.distance(Point(*vertices[i]), Point(*p))

        if current_distance < min_dist:
            min_dist_index = i
            min_dist = current_distance

    return min_dist_index


def find_tangent_point_index(vertices: list, start: int, p: tuple, clockwise: bool = True) -> int:

    i: int = start
    size: int = len(vertices)

    if clockwise:
        while orientation(p, vertices[i], vertices[(size+i-1) % size]) < 0:
            i = (size + i - 1) % size

    else:
        while orientation(p, vertices[i], vertices[(i+1) % size]) > 0:
            i = (i + 1) % size

    return i


def union_point_poly(hull: list, p: tuple):

    start: int = find_closest_point_index(hull, p)

    left_tan_index = find_tangent_point_index(hull, start=start, p=p, clockwise=False)
    right_tan_index = find_tangent_point_index(hull, start=start, p=p, clockwise=True)

    if left_tan_index < right_tan_index:
        hull[:] = hull[left_tan_index:right_tan_index+1] + [p]

    else:
        hull[:] = hull[:right_tan_index+1] + [p] + hull[left_tan_index:]


"""
    Convex hull algorithms
"""


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

    i: int = get_point_index(vertices, x=True, max_x=False, max_y=False)
    vertices[0], vertices[i] = vertices[i], vertices[0]

    vec = Vector(Point(*vertices[0]), Point(vertices[0][0], vertices[0][1] + 1))
    j = vertices.index(min(vertices, key=lambda x: vec.angle_between(Vector(Point(*vertices[0]), Point(*x)))))
    vertices[1], vertices[j] = vertices[j], vertices[1]

    vertices.append(vertices[0])
    hull_size = 2
    vec.tail = Point(*vertices[1])

    while True:

        vec.head = vec.tail
        vec.tail = Point(*vertices[hull_size])
        k = hull_size
        min_dist = vec.head.distance(vec.tail)

        for j in range(hull_size, len(vertices)):

            p_j = Point(*vertices[j])
            ori = Point.orientation(vec.head, vec.tail, p_j)
            curr_dist = vec.tail.distance(p_j)

            if ori > 0:
                k = j
                vec.tail = p_j

            elif ori == 0 and curr_dist < min_dist:
                k = j
                vec.tail = p_j
                min_dist = curr_dist

        if vertices[k] == vertices[0]:
            break

        else:
            vertices[hull_size], vertices[k] = vertices[k], vertices[hull_size]
            hull_size += 1

    vertices.pop()
    return vertices[:hull_size]


def convex_hull_incremental(vertices: list) -> list:

    hull = list(orientate_vertices(vertices[0], vertices[1], vertices[2]))

    for i in range(3, len(vertices)):

        p_i = Point(*vertices[i])

        if not p_i.in_poly(hull):
            union_point_poly(hull, vertices[i])

    return hull


def convex_hull_incremental_fast(vertices: list) -> list:

    vertices.sort()
    hull = vertices[:3]

    for i in range(3, len(vertices)):
        union_point_poly(hull, vertices[i])

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


if __name__ == '__main__':

    # points = [(2, 1), (1, 2), (1, 4), (4, -2), (1, 1)]
    # points = [(1, 1), (1, 2), (1, 3), (2, 2), (3, 3), (4, 4)]
    points = [(0, 0), (0, 1), (1, 1), (2, 2), (1, -1), (3, 3), (3, 2), (3, 1), (3, 0), (3, -1), (3, -2), (3, -3)]
    # print(convex_hull_quad(points))
    # print(convex_hull_cubic(points))
    # print(convex_hull_jarvis_march(points))
    # print(convex_hull_incremental(points))
    print(convex_hull_incremental_fast(points))
    print(convex_hull_graham_scan(points))

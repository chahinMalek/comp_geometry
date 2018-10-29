from geometry_objects.point import Point
from geometry_objects.vector import Vector


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


def get_hull_edges(vertices: list) -> list:

    edges = []
    fail_flag = -2

    for i in range(len(vertices) - 1):
        for j in range(i+1, len(vertices)):

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

            if current_orientation == fail_flag:
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


def divide_and_sort_vertices(leftmost_point, vertices: list) -> list:

    upper_vertices = []
    lower_vertices = []

    vertices = sorted(vertices, key=lambda x: x[0])
    centroid: 'Point' = find_centroid(vertices)

    for v in vertices:

        if Point.orientation(Point(*leftmost_point), centroid, Point(*v)) >= 0:
            upper_vertices.append(v)

        else:
            lower_vertices.insert(0, v)

    return upper_vertices + lower_vertices


def find_hull(vertices: list) -> list:

    hull = vertices[:2]

    for v in vertices[2:]:

        # edge case if only one point is in hull
        while len(hull) > 1 and Point.orientation(Point(*hull[-2]), Point(*hull[-1]), Point(*v)) > 0:
            hull.pop()

        hull.append(v)

    return hull


def convex_hull_1(points: list) -> list:

    hull = get_hull_edges(points)
    sort_hull(hull)
    return hull


def convex_hull_graham_scan(vertices: list) -> list:

    # divide in two subsets
    # orientate the two subsets clockwise

    centroid = find_centroid(vertices)
    sorted(vertices, key=lambda x: Vector(centroid, Point(*x)).slope())
    return find_hull(vertices)


# points = [(2, 1), (1, 2), (1, 4), (4, -2), (1, 1)]
# points = [(1, 1), (1, 2), (1, 3), (2, 2), (3, 3), (4, 4)]
points = [(0, 0), (1, -1), (1, 1), (2, 2), (3, 3), (3, 2), (3, 1), (3, 0), (3, -1), (3, -2), (3, -3)]
print(convex_hull_1(points))
print(convex_hull_graham_scan(points))

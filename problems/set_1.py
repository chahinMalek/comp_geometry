from geometry_objects.point import Point
from problems.convex_hull import find_centroid
from problems.simple_poly import simple_poly

"""
    Given a poly as an array of segments (non-sorted).
    
    O(nLogn) sorting in the clockwise orientation
"""


def sort_cw(edges) -> list:

    vertices_map = set()

    for e in edges:
        vertices_map.add(e[0])
        vertices_map.add(e[1])

    return simple_poly(list(vertices_map))


def traverse_map(vertices_map: dict):

    sorted_list = []
    prev_p = vertices_map[0]

    for i in range(len(vertices_map)-1):
        sorted_list.append(prev_p)
        prev_p = vertices_map[prev_p]

    return sorted_list


def orientate_edges(edges):

    centroid = find_centroid()

    for e in edges:

        if Point.orientation(*e, centroid) < 0:
            e[1], e[0] = e[0], e[1]


"""
    Given a poly as a list of segments (non-sorted).
    
    O(n) sorting in the clockwise orientation
"""


def sort_cw_linear(edges) -> list:

    vertices_map = {}
    # construct vertices map
    return traverse_map(vertices_map)

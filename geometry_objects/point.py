from math import atan2
from math import pi
from math import sqrt
from sys import maxsize

from berg_problems.chapter_1 import orientation


class BaseNode:

    def __init__(self):

        self.next_node = self
        self.previous_node = self

    def next(self) -> 'BaseNode':
        return self.next_node

    def previous(self) -> 'BaseNode':
        return self.previous_node

    def insert(self, b: 'BaseNode') -> 'BaseNode':

        b.previous_node = self
        b.next_node = self.next_node
        self.next_node.previous_node = b
        self.next_node = b

        return b

    def remove(self) -> 'BaseNode':

        self.previous_node.next_node = self.next_node
        self.next_node.previous_node = self.previous_node
        self.next_node = self.previous_node = self

        return self

    def connect(self, b: 'BaseNode'):

        a = self
        pom1 = self.next_node
        pom2 = b.next_node

        a.next_node = pom2
        b.next_node = pom1
        pom1.previous_node = b
        pom2.previous_node = a


class Point:

    CLASSIFICATIONS = {'between': 0, 'left': -1, 'right': 1, 'head': 2, 'tail': -2, 'front': 3, 'back': -3}

    def __init__(self, x: float = 0.0, y: float = 0.0):

        self.x = x
        self.y = y

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)

    def __rmul__(self, other: int):
        return self.__mul(other)

    def __mul__(self, other: float):
        return self.__mul(other)

    def __mul(self, other: float):
        return Point(other * self.x, other * self.y)

    def __truediv__(self, other):
        return self.__div(other)

    def __div(self, other: float):

        if other == 0.0:
            return Point(maxsize, maxsize)

        else:
            return Point(self.x / other, self.y / other)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other: 'Point'):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other: 'Point'):
        return not self.__eq__(other)

    def __lt__(self, other: 'Point'):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def __gt__(self, other: 'Point'):
        return self.x > other.x or (self.x == other.x and self.y > other.y)

    def __len__(self) -> float:
        return self.x ** 2 + self.y ** 2

    def euclidean_distance(self, other: 'Point') -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def between(self, p1: 'Point', p2: 'Point'):
        return min(p1.x, p2.x) <= self.x <= max(p1.x, p2.x) and min(p1.y, p2.y) <= self.y <= max(p1.y, p2.y)

    def classify(self, p1: 'Point', p2: 'Point'):

        # if triangle p1, p2, self is negatively oriented, then the self point is on the the left side
        if Point.orientation(p1, p2, self) < 0:
            return Point.CLASSIFICATIONS['left']

        # if triangle p1, p2, self is positively oriented, then the self point is on the the right side
        elif Point.orientation(p1, p2, self) > 0:
            return Point.CLASSIFICATIONS['right']

        # points are collinear in the following code
        # if vectors p1,p2 and p1,p3 are oriented countrary, the point is classified as behind
        elif (p2 - p1).x * (self - p1).x < 0 or (p2 - p1).y * (self - p1).y < 0:
            return Point.CLASSIFICATIONS['back']

        # if the points x and y values are between ones of the p1 and p2 pointsm point is classified as between
        elif self.between(p1, p2):
            return Point.CLASSIFICATIONS['between']

        elif p1 == self:
            return Point.CLASSIFICATIONS['head']

        elif p2 == self:
            return Point.CLASSIFICATIONS['tail']

        else:
            return Point.CLASSIFICATIONS['front']

    def self_orientation(self, p1: 'Point', p2: 'Point') -> int:
        return Point.orientation(p1, p2, self)

    def in_triangle(self, p1, p2, p3) -> bool:

        o1 = self.self_orientation(p1, p2)
        o2 = self.self_orientation(p2, p3)
        o3 = self.self_orientation(p3, p1)

        if o1 == 0 or o2 == 0 or o3 == 0:
            return False

        return o1 == o2 == o3

    @staticmethod
    def orientation(p1: 'Point', p2: 'Point', p3: 'Point') -> int:

        a: Point = p2 - p1
        b: Point = p3 - p1

        theta = a.x * b.y - a.y * b.x

        # oriented counter clockwise (positive) <=> p3 is on the p1p2 left
        if theta > 0:
            return 1

        # oriented clockwise (negative) <=> p3 is on the p1p2 right
        if theta < 0:
            return -1

        # collinear
        return 0

    @staticmethod
    def distance(p1: tuple, p2: tuple) -> float:
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def distance(self, p: 'Point'):
        return sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

    def slope(self):

        theta: float = atan2(self.y, self.x)
        theta *= (360 / 2 / pi)
        return theta if self.y >= 0.0 else 360 + theta

    def in_poly(self, vertices: list) -> bool:

        size: int = len(vertices)
        point: tuple = (self.x, self.y)

        for i in range(size):

            if orientation(vertices[i], vertices[(i+1) % size], point) > 0:
                return False

        return True


class Vertex(BaseNode, Point):

    def __init__(self, x: float = 0.0, y: float = 0.0):

        BaseNode.__init__(self)
        Point.__init__(self, x, y)

    def __repr__(self):
        return Point.__repr__(self)

    def insert(self, b: 'Vertex'):
        return BaseNode.insert(self, b)

    def next_vertex(self, orientation: int = 1):
        return self.next() if orientation > 0 else self.previous()

    def get_point(self):
        return Point.__init__(self, self.x, self.y)

    def is_convex(self):

        next_v = self.next_vertex()
        prev_v = self.next_vertex(-1)

        classification = prev_v.classify(self, next_v)

        if classification == Point.CLASSIFICATIONS['right'] or classification == Point.CLASSIFICATIONS['back']:
            return True

        else:
            return False

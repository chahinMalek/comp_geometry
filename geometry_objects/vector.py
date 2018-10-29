from geometry_objects.point import Point
from math import acos
from math import pi
from math import inf


class Vector:

    def __init__(self, head: 'Point', tail: 'Point'):

        self.head = head
        self.tail = tail

    def magnitude(self) -> float:
        return self.head.euclidean_distance(self.tail)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '{}, {}'.format(self.head, self.tail)

    def direction_vector(self):
        return self.tail - self.head

    def orientation_vector(self):

        direction_vector: Point = self.direction_vector()
        return Point(direction_vector.y, -direction_vector.x)

    def rotate(self, positive: bool = True) -> None:

        middle: Point = (self.tail + self.head) / 2
        orientation_vector: Point = self.orientation_vector()
        orientation_vector *= 0.5

        mul: int = 1

        if not positive:
            mul = -1

        self.head = middle - mul * orientation_vector
        self.tail = middle + mul * orientation_vector

    def flip(self):
        self.tail, self.head = self.head, self.tail

    def dot(self, other: 'Vector') -> float:

        prod_x = (self.tail.x - self.head.x) * (other.tail.x - other.head.x)
        prod_y = (self.tail.y - self.head.y) * (other.tail.y - other.head.y)
        return prod_x + prod_y

    def angle_between(self, other: 'Vector') -> float:

        alpha = (180 / pi) * acos(self.dot(other) / self.magnitude() / other.magnitude())
        return round(alpha, 10)

    def slope(self):
        return (self.tail - self.head).slope()

    def do_intersect(self, s_2: 'Vector') -> bool:

        # orientation of the (self.tail, self.head, s_2.tail) triangle
        s_1_orientation_tail = Point.orientation(self.tail, self.head, s_2.tail)

        # orientation of the (self.tail, self.head, s_2.head) triangle
        s_1_orientation_head = Point.orientation(self.tail, self.head, s_2.head)

        # orientation of the (s_2.tail, s_2.head, self.tail) triangle
        s_2_orientation_tail = Point.orientation(s_2.tail, s_2.head, self.tail)

        # orientation of the (s_2.tail, s_2.head, self.head) triangle
        s_2_orientation_head = Point.orientation(s_2.tail, s_2.head, self.head)

        # general case
        if s_1_orientation_tail != s_1_orientation_head and s_2_orientation_tail != s_2_orientation_head:
            return True

        # collinear case
        if s_1_orientation_tail == 0 and s_1_orientation_head == 0 and s_2_orientation_tail == 0 and s_2_orientation_head == 0:

            if self.tail.between(s_2.head, s_2.tail) or self.head.between(s_2.head, s_2.tail) \
                    or s_2.tail.between(self.head, self.tail) or s_2.head.between(self.head, self.tail):
                return True

        return False

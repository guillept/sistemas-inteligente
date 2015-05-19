from collections import namedtuple
import math


Point = namedtuple('Point', ('x', 'y'))


def rects_are_overlapping(rect_a, rect_b, epsilon=0):
    # http://stackoverflow.com/a/306332/742501
    a_top_left, a_bottom_right = rect_a
    b_top_left, b_bottom_right = rect_b
    return (a_top_left.x - epsilon < b_bottom_right.x and
            a_bottom_right.x + epsilon > b_top_left.x and
            a_top_left.y - epsilon < b_bottom_right.y and
            a_bottom_right.y + epsilon > b_top_left.y)


def rect_in_world(rect, world):
    top_left, bottom_right = rect
    if (top_left.x < 0 or top_left.y < 0 or
        bottom_right.x > world.width or bottom_right.y > world.height):
        return False
    return True


def compute_abs(dx, dy):
    return math.sqrt(dx**2 + dy**2)


def normalize(dx, dy):
    abs = compute_abs(dx, dy)
    return dx / abs, dy / abs

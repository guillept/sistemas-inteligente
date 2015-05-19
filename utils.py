from collections import namedtuple
import random

from obstacle import Obstacle


Point = namedtuple('Point', ('x', 'y'))


def rects_are_overlapping(rect_a, rect_b):
    # http://stackoverflow.com/a/306332/742501
    a_top_left, a_bottom_right = rect_a
    b_top_left, b_bottom_right = rect_b
    return (a_top_left.x < b_bottom_right.x and
            a_bottom_right.x > b_top_left.x and
            a_top_left.y < b_bottom_right.y and
            a_bottom_right.y > b_top_left.y)


def is_valid_obstacle(obstacle, obstacles, world):
    top_left, bottom_right = obstacle.get_bounds()

    if (top_left.x < 0 or top_left.y < 0 or
        bottom_right.x > world.width or bottom_right.y > world.height):
        return False

    for other in obstacles + world.entities:
        if rects_are_overlapping(obstacle.get_bounds(),
                                 other.get_bounds()):
            return False

    return True


def generate_obstacles(num_obstacles, world):
    obstacles = []
    for _ in range(num_obstacles):
        x = random.randint(0, world.width)
        y = random.randint(0, world.height)

        obstacle = Obstacle(x, y)
        if is_valid_obstacle(obstacle, obstacles, world):
            obstacles.append(obstacle)

    return obstacles

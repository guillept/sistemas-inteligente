import random

from drawable_entity import DrawableEntity
from utils import rects_are_overlapping


class Obstacle(DrawableEntity):
    SIZE = 20
    COLOR = 'gray'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        top_left, bottom_right = self.get_bounds()
        canvas.create_rectangle(top_left.x,
                                top_left.y,
                                bottom_right.x,
                                bottom_right.y,
                                fill=self.COLOR)

    def has_room(self, obstacles, world):
        """Checks whether self has room in world, among other obstacles."""
        top_left, bottom_right = self.get_bounds()

        if (top_left.x < 0 or top_left.y < 0 or
                    bottom_right.x > world.width or bottom_right.y > world.height):
            return False

        for other in obstacles + world.entities:
            if rects_are_overlapping(self.get_bounds(),
                                     other.get_bounds()):
                return False

        return True

    @staticmethod
    def generate_many(num_obstacles, world):
        obstacles = []
        for _ in range(num_obstacles):
            x = random.randint(0, world.width)
            y = random.randint(0, world.height)

            obstacle = Obstacle(x, y)
            if obstacle.has_room(obstacles, world):
                obstacles.append(obstacle)

        return obstacles

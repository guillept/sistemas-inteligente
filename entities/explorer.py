import random

from entities.drawable_entity import DrawableEntity
from utils import rect_in_world, rects_are_overlapping


class Explorer(DrawableEntity):
    SIZE = 15
    MAX_VELOCITY = 1.4
    COLOR = 'blue'

    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world

        self.dx, self.dy = self._get_new_direction()

    def draw(self, canvas):
        top_left, bottom_right = self.get_bounds()
        canvas.create_rectangle(top_left.x,
                                top_left.y,
                                bottom_right.x,
                                bottom_right.y,
                                fill=self.COLOR)

    def tick(self):
        while not self._can_move():
            self.dx, self.dy = self._get_new_direction()
        self._move()

    def _move(self):
        self.x += self.dx
        self.y += self.dy

    def _get_new_direction(self):
        dx = random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
        dy = random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
        return dx, dy

    def _can_move(self):
        new_self = Explorer(self.x + self.dx,
                            self.y + self.dy,
                            self.world)
        bounds = new_self.get_bounds()

        if not rect_in_world(bounds, new_self.world):
            return False

        for other in new_self.world.entities:
            if other == self:
                continue
            if rects_are_overlapping(bounds, other.get_bounds()):
                return False

        return True

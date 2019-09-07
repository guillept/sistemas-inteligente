import random

from entities.drawable_entity import DrawableEntity
from utils import rects_are_overlapping, rect_in_world

class Morona(DrawableEntity):
    SIZE = 3
    COLOR = 'brown'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        top_left, bottom_right = self.get_bounds()
        canvas.create_oval(top_left.x,
                            top_left.y,
                            bottom_right.x,
                            bottom_right.y,
                            fill=self.COLOR)

    def has_room(self, moronas, world):
        """Checks whether self has room in world, among other moronas."""
        bounds = self.get_bounds()

        if not rect_in_world(bounds, world):
            return False

        for other in world.entities_but_explorer:

            if rects_are_overlapping(bounds, other.get_bounds()):
                return False

        return True

    @staticmethod
    def generate_many(num, world, explorer_x, explorer_y):
        moronas = []
        up = 2

        while len(moronas) < num:
            x = explorer_x #random.randint(0, world.width)
            y = explorer_y + up#random.randint(0, world.height)
            up = up * -1

            morona = Morona(x, y)
            if morona.has_room(moronas, world):
                moronas.append(morona)
        
        return moronas

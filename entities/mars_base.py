from entities.drawable_entity import DrawableEntity


class MarsBase(DrawableEntity):
    SIZE = 40
    COLOR = 'green'

    def __init__(self, world_width, world_height):
        self.x = world_width / 2
        self.y = world_height / 2

    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.SIZE / 2,
                                self.y - self.SIZE / 2,
                                self.x + self.SIZE / 2,
                                self.y + self.SIZE / 2,
                                fill=self.COLOR)

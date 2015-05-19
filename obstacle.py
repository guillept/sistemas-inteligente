from drawable_entity import DrawableEntity


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

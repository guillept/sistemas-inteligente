from entities.drawable_entity import DrawableEntity


class World(DrawableEntity):
    COLOR = '#abc'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entities = []

    def draw(self, canvas):
        canvas.configure(background=self.COLOR)

    def add_entity(self, entity):
        assert isinstance(entity, DrawableEntity)
        self.entities.append(entity)

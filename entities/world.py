from entities.drawable_entity import DrawableEntity
from entities.mars_base import MarsBase
from entities.obstacle import Obstacle
from entities.rock import Rock


class World(DrawableEntity):
    COLOR = '#abc'

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.entities = []
        self.rocks = []
        self.obstacles = []
        self.mars_base = None

    def draw(self, canvas):
        canvas.configure(background=self.COLOR)

    def add_entity(self, entity):
        assert isinstance(entity, DrawableEntity)

        self.entities.append(entity)

        if isinstance(entity, Rock):
            self.rocks.append(entity)
        elif isinstance(entity, Obstacle):
            self.obstacles.append(entity)
        elif isinstance(entity, MarsBase):
            self.mars_base = entity

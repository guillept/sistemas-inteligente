from entities.carrier import Carrier
from entities.explorer import Explorer
from gui import GUI
from entities.mars_base import MarsBase
from entities.obstacle import Obstacle
from entities.rock import Rock
from entities.world import World


NUM_OBSTACLES = 10
NUM_ROCKS = 100
NUM_EXPLORERS = 5
NUM_CARRIERS = 2


def init_entities():
    world = World(800, 600, NUM_ROCKS)

    mars_base = MarsBase(world.width, world.height)
    world.add_entity(mars_base)

    for _ in range(NUM_EXPLORERS):
        explorer = Explorer(mars_base.x + mars_base.SIZE,
                            mars_base.y + mars_base.SIZE,
                            world)
        world.add_entity(explorer)

    for _ in range(NUM_CARRIERS):
        carrier = Carrier(mars_base.x + mars_base.SIZE,
                          mars_base.y + mars_base.SIZE,
                          world)
        world.add_entity(carrier)

    obstacles = Obstacle.generate_many(NUM_OBSTACLES, world)
    for obstacle in obstacles:
        world.add_entity(obstacle)

    rocks = Rock.generate_many(NUM_ROCKS, world)
    for rock in rocks:
        world.add_entity(rock)

    return world


def main():
    world = init_entities()

    gui = GUI(world)
    gui.start()


if __name__ == '__main__':
    main()

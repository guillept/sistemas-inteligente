from gui import GUI
from mars_base import MarsBase
from obstacle import Obstacle
from world import World


def main():

    world = World(800, 600)
    mars_base = MarsBase(world.width, world.height)
    obstacles = Obstacle.generate_many(10, world)

    world.add_entity(world)
    world.add_entity(mars_base)
    for obstacle in obstacles:
        world.add_entity(obstacle)

    gui = GUI(world)
    gui.start()


if __name__ == '__main__':
    main()

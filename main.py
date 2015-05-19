from gui import GUI
from mars_base import MarsBase
from world import World


def main():
    gui = GUI(800, 600)

    world = World(gui.width, gui.height)
    mars_base = MarsBase(world.width, world.height)

    gui.add_entity(world)
    gui.add_entity(mars_base)

    gui.start()


if __name__ == '__main__':
    main()

from entities.explorer import Explorer
from entities.message import MESSAGE_COME, WaitMessage
from utils import normalize, rects_are_overlapping, distance, Point


class Carrier(Explorer):
    COLOR = 'red'
    EN_ROUTE_COLOR = 'green'

    def __init__(self, x, y, world):
        super(Carrier, self).__init__(x, y, world)
        self.rocks = 0
        self.en_route = False
        self.en_route_to = None

    def draw(self, canvas):
        top_left, bottom_right = self.get_bounds()
        canvas.create_rectangle(top_left.x,
                                top_left.y,
                                bottom_right.x,
                                bottom_right.y,
                                fill=self.EN_ROUTE_COLOR if self.en_route else self.COLOR)

    def _tick(self):
        # If all rocks are collected, take what it has to the base.
        if self._all_rocks_collected():
            if self._drop_available():
                for _ in range(self.rocks):
                    self.world.rock_collected()
                    self.rocks -= 1
                return
            self.dx, self.dy = normalize(self.world.mars_base.x - self.x,
                                         self.world.mars_base.y - self.y)

        else:
            # Pick up from nearby explorer.
            explorer = self._pickup_available()
            if explorer:
                explorer.transfer_rock_to_carrier()
                explorer.clear_inbox()
                self.rocks += 1
                self._reset()
                return

            if not self.en_route:
                # Check for closest explorer that needs pickup.
                p = Point(self.x, self.y)
                msgs = [msg for msg in self.inbox if msg.type == MESSAGE_COME]
                msgs.sort(key=lambda m: m.point, cmp=lambda p1, p2: distance(p1, p) < distance(p2, p))
                if msgs:
                    msg = msgs[0]
                    explorer = msg.source
                    explorer.inbox.append(WaitMessage(self))
                    self.en_route = True
                    self.en_route_to = msg

            else:
                # If some other explorer picked it up, reset.
                if not self.en_route_to.source.has_rock:
                    self._reset()
                    return

                self.dx, self.dy = normalize(self.en_route_to.point.x - self.x,
                                             self.en_route_to.point.y - self.y)

        # Keep walkin'.
        while not self._can_move():
            self.dx, self.dy = self._get_new_direction()
        self._move()

    def _pickup_available(self):
        for explorer in self.world.explorers:
            if (rects_are_overlapping(self.get_bounds(),
                                     explorer.get_bounds(),
                                     self.PICKUP_REACH) and
                explorer.has_rock):
                return explorer

        return None

    def _all_rocks_collected(self):
        rocks_in_explorer = [True for explorer in self.world.explorers if explorer.has_rock]
        return not bool(self.world.rocks) and not rocks_in_explorer

    def _reset(self):
        self.en_route = False
        self.en_route_to = None
        self.clear_inbox()

import random

from entities.drawable_entity import DrawableEntity
from entities.message import MESSAGE_WAIT, ComeMessage
from utils import rect_in_world, rects_are_overlapping, normalize
from entities.morona import Morona
from entities.rock import Rock

class Explorer(DrawableEntity):
    SIZE = 7
    MAX_VELOCITY = 1.3
    PICKUP_REACH = 2
    SENSOR_RANGE = 15
    SENSE_DELAY = 100
    COLOR = 'blue'
    HAS_ROCK_COLOR = 'yellow'
    SENSOR_COLOR = 'yellow'

    def __init__(self, x, y, world):
        self.x = self.last_x = x
        self.y = self.last_y = y
        self.world = world
        self.dx, self.dy = self._get_new_direction()
        self.ticks = 0
        self.has_rock = False
        self.inbox = []
        self.index = 0
        self.last_index = -1

    def draw(self, canvas):
        helper = Explorer(self.x, self.y, self.world)
        helper.SIZE = 2 * self.SENSOR_RANGE + self.SIZE
        top_left, bottom_right = helper.get_bounds()
        canvas.create_oval(top_left.x,
                           top_left.y,
                           bottom_right.x,
                           bottom_right.y,
                           outline=self.SENSOR_COLOR)

        top_left, bottom_right = self.get_bounds()
        canvas.create_rectangle(top_left.x,
                                top_left.y,
                                bottom_right.x,
                                bottom_right.y,
                                fill=self.HAS_ROCK_COLOR if self.has_rock else self.COLOR)

    def clear_inbox(self):
        self.inbox = []

    def clear_inbox_from(self, source):
        self.inbox = [msg for msg in self.inbox if msg.source != source]

    def transfer_rock_to_carrier(self):
        self.has_rock = False

    def tick(self):
        self._tick()
        self.ticks += 1

    def _tick(self):

        # CAPA 1
        if not self._can_move():
            
            self.last_index = -1  
            self.dx, self.dy = self._get_new_direction()
            self.x = self.last_x
            self.y = self.last_y
            self._move()


        else:
            # Keep walkin'.
            self.last_x = self.x
            self.last_y = self.y

            if self.has_rock:
                self.last_index = -1
                # Try to drop at base.
                # CAPA 2
                if self._drop_available():
                    self.has_rock = False
                    self.world.rock_collected()
                    self.dx, self.dy = self._get_new_direction()
                    return

                self.dx, self.dy = normalize(self.world.mars_base.x - self.x, self.world.mars_base.y - self.y)

            else:
                # Pick up.
                # CAPA 3
                rock = self._rock_available()
                if rock:
                    self.has_rock = True

                    moronas = Morona.generate_many(2, self.world, self.x, self.y)
                    for morona in moronas:
                        self.world.add_entity(morona, self.index)   
                    self.index += 1
                
                    self.world.remove_entity(rock)

                    self.dx, self.dy = normalize(self.world.mars_base.x - self.x, self.world.mars_base.y - self.y)
                    return
                
                # Pick up morona
                # CAPA 4
                morona, index = self._morona_available()
                if morona:
                    if self.last_index != index:
                        self.world.remove_entity(morona, index)
                        self.last_index = index
                        return


                # Head towards rock.
                # CAPA 4
                rock = self._sense_rock()
                if rock:
                    self.dx, self.dy = normalize(rock.x - self.x, rock.y - self.y)

            # CAPA 5
            self._move()

    def _move(self):
        self.x += self.dx
        self.y += self.dy

    def _get_new_direction(self):
        dx = random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
        dy = random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
        return normalize(dx, dy)

    def _can_move(self):
        new_self = Explorer(self.x + self.dx,
                            self.y + self.dy,
                            self.world)
        bounds = new_self.get_bounds()

        # Tengo una piedra y la puedo dejar en base
        if self.has_rock and self._drop_available():
            return True

        if not rect_in_world(bounds, new_self.world):
            return False

        for other in new_self.world.entities:
            # Allow collisions with other explorers.
            if isinstance(other, Explorer):
                continue

            # Allow collisions with other moronas.
            if isinstance(other, Morona):
                continue

            if not self.has_rock and isinstance(other, Rock):
                return True

            if rects_are_overlapping(bounds, other.get_bounds(), 2):
                return False

        return True

    def _rock_available(self):
        for rock in self.world.rocks:
            if rects_are_overlapping(self.get_bounds(),
                                     rock.get_bounds(),
                                     self.PICKUP_REACH):
                return rock

        return None

    def _morona_available(self):

        for siblings in self.world.moronas:
            for morona in self.world.moronas[siblings]:
                if rects_are_overlapping(self.get_bounds(), morona.get_bounds()):
                    return morona, siblings

        return None, 0

    def _sense_rock(self):
        # Wait a bit so that the explorers spread out.
        if self.ticks < self.SENSE_DELAY:
            return None

        for rock in self.world.rocks:
            if rects_are_overlapping(self.get_bounds(),
                                     rock.get_bounds(),
                                     self.SENSOR_RANGE):
                return rock

        return None

    def _drop_available(self):
        if rects_are_overlapping(self.get_bounds(),
                                 self.world.mars_base.get_bounds(),
                                 self.PICKUP_REACH):
            return True
        return False

    def _incoming_carrier(self):
        incoming = [msg for msg in self.inbox if msg.type == MESSAGE_WAIT]
        if incoming:
            return incoming[0]
        return None

    def _broadcast_come_message(self):
        for carrier in self.world.carriers:
            carrier.inbox.append(ComeMessage(self, self.x, self.y))

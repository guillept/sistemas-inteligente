from entities.explorer import Explorer
from utils import normalize


class Carrier(Explorer):
    COLOR = 'red'

    def draw(self, canvas):
        top_left, bottom_right = self.get_bounds()
        canvas.create_rectangle(top_left.x,
                                top_left.y,
                                bottom_right.x,
                                bottom_right.y,
                                fill=self.COLOR)

    def _tick(self):

        # Keep walkin'.
        while not self._can_move():
            self.dx, self.dy = self._get_new_direction()
        self._move()

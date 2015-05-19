from utils import Point


class DrawableEntity(object):
    """Drawable on the canvas."""

    def draw(self, canvas):
        raise NotImplementedError()

    def get_bounds(self):
        """
        :return: ((x1, y1), (x2, y2))
        """
        return (
            Point(self.x - self.SIZE / 2,
                  self.y - self.SIZE / 2),
            Point(self.x + self.SIZE / 2,
                  self.y + self.SIZE / 2)
        )


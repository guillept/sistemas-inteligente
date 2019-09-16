from Tkinter import Tk, Canvas


class GUI(object):
    def __init__(self, world, is_collab):
        self.ticks = 0
        self.world = world
        self.width = world.width
        self.height = world.height

        self.root = Tk()
        self.root.title("Mars Explorer")
        window_x, window_y = self._compute_window_coords()
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height,
                                            window_x, window_y))

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.after(1, self._tick)

    def start(self):
        self.root.mainloop()

    def _tick(self):
        # Stop if done.
        if self.world.is_done():
            return

        self.world.tick()
        self._draw()

        self.ticks += 1
        self.canvas.after(1, self._tick)

    def _draw(self):
        self.canvas.delete('all')

        self.world.draw(self.canvas)
        for entity in self.world.entities:
            entity.draw(self.canvas)

        self.canvas.create_text(self.width - 20, 10, text=str(self.ticks))
        self.canvas.create_text(self.width - 70, 30,
                                text='Rocks in carriers: %d' % self.world.rocks_in_carriers())
        self.canvas.create_text(self.width - 70, 50, text='Rocks delivered: %d' % self.world.rocks_collected)
        self.canvas.create_text(self.width - 55, 70, text='Total rocks: %d' % self.world.num_rocks)

    def _compute_window_coords(self):
        # http://stackoverflow.com/a/14912644/742501
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_x = screen_width / 2 - self.width / 2
        window_y = screen_height / 2 - self.height / 2
        return window_x, window_y

from Tkinter import Tk, Canvas

class GUI(object):
    def __init__(self, width, height):
        self.ticks = 0
        self.width = width
        self.height = height

        self.root = Tk()
        self.root.title("Mars Explorer")

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.after(1, self._tick)

    def _tick(self):
        self._draw()

        self.ticks += 1
        self.canvas.after(1, self._tick)

    def _draw(self):
        self.canvas.delete('all')

        self.canvas.create_text(self.width - 20, 10, text=str(self.ticks))

    def start(self):
        self.root.mainloop()

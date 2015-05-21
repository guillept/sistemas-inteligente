from utils import Point

MESSAGE_WAIT = 'wait'
MESSAGE_COME = 'come'


class Message(object):
    type = None

    def __init__(self, source):
        self.source = source


class ComeMessage(Message):
    type = MESSAGE_COME

    def __init__(self, source, x, y):
        super(ComeMessage, self).__init__(source)
        self.x = x
        self.y = y

    @property
    def point(self):
        return Point(self.x, self.y)


class WaitMessage(Message):
    type = MESSAGE_WAIT

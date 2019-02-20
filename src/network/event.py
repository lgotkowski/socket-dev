class Event(object):
    def __init__(self):
        self._handlers = []

    def add(self, handler):
        self._handlers.append(handler)

    def remove(self, handler):
        self._handlers.remove(handler)

    def emit(self, sender, args=None):
        for handler in self._handlers:
            handler(sender, args)

    def __iadd__(self, handler):
        self.add(handler)

    def __isub__(self, handler):
        self.remove(handler)

    def __call__(self, sender, args):
        self.emit(sender, args)
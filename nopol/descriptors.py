class Singular:
    def __init__(self, func):
        self.func = func

    def __get__(self, inst, cls):
        if inst is None:
            return self

        return lambda arg: getattr(inst, self.func.__name__)([arg])

import inspect


class Event:
    def __init__(self, name, func):
        self.name = name
        self.func = func

def event(name):
    def predicate(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Event functions must be coroutine.")
        return Event(name, func)
    return predicate
import inspect


class Command():
    def __init__(self, name, func, _type):
        self.name = name
        self.func = func
        self.type = _type

def command(name, _type):
    def predicate(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Command functions must be coroutine.")
        return Command(name, func, _type)
    return predicate
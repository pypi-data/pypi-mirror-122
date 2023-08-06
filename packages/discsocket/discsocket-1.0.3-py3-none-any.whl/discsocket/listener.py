from . import utils

class EventContainer:
    def __init__(self):
        self.commands = {}
        self.components = {}
        self.user_commands = {}
        self.message_commands = {}
        self.events = {}

    def command(self, command):
        if command.type == utils.SLASH:
            self.commands[command.name] = command.func
        elif command.type == utils.USER:
            self.user_commands[command.name] = command.func
        elif command.type == utils.MESSAGE:
            self.message_commands[command.name] = command.func

    def component(self, component):
        self.components[component.ucid] = component.func

    def event(self, event):
        try:
            self.events[event.name].append(event.func)
        except KeyError:
            self.events[event.name] = [event.func]
from typing import Optional
import aiohttp
import asyncio
import json
import importlib
import threading
import time
import concurrent.futures
import sys
import traceback
import inspect

from . import utils
from .listener import EventContainer
from .commands import Command
from .components import Component
from .events import Event
from .models.context import ButtonContext, Context, SelectMenuContext
from .models.user import User


class MaintainSocketAlive(threading.Thread):
    def __init__(self, *args, **kwargs):
        socket = kwargs.pop('socket')
        interval = kwargs.pop('interval')
        threading.Thread.__init__(self, *args, **kwargs)
        self.socket = socket
        self.interval = interval / 1000
        self.daemon = True
        self._stop_event = threading.Event()
        self._last_ack = time.perf_counter()
        self._last_recv = time.perf_counter()
        self._last_send = time.perf_counter()
        self.latency = float('inf')
        self.main_id = socket.thread_id

    def run(self):
        while not self._stop_event.wait(self.interval):
            if self._last_recv + 60 < time.perf_counter():
                func = self.socket.close(4000)
                f = asyncio.run_coroutine_threadsafe(func, loop=self.socket.loop)
                try:
                    f.result()
                except Exception:
                    pass
                finally:
                    self.stop()
                    return
            
            coro = self.socket.send_heartbeat(self.payload())
            f = asyncio.run_coroutine_threadsafe(coro, loop=self.socket.loop)
            try:
                total = 0
                while True:
                    try:
                        f.result(10)
                        break
                    except concurrent.futures.TimeoutError:
                        total += 10
                        try:
                            frame = sys._current_frames()[self.main_id]
                        except KeyError:
                            pass
            
            except Exception:
                self.stop()
                traceback.print_exc()
            else:
                self._last_send = time.perf_counter()

    def payload(self):
        return {
            "op": 1,
            "d": None
        }
    def stop(self):
        self._stop_event.set()

    def tick(self):
        self._last_recv = time.perf_counter()
    def ack(self):
        ack_time = time.perf_counter()
        self._last_ack = ack_time
        self.latency = ack_time - self._last_send


class Socket:
    """Connects to the Discord websocket"""
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self.session: aiohttp.BaseConnector = None
        self.__token: str = None
        self.headers: dict = None
        self.user = None
        self.alive_handler = None
        self.events = EventContainer()
        self.thread_id = threading.get_ident()
        self.connection = None
        self.unchecked_decorators = {"event": [], "command": [], "component": []}

    def add_component_listener(self, ucid, func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Component functions must be a coroutine")
        self.events.component(Component(ucid, func))

    def event(self, name):
        def predicate(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("Event function must be coroutine")
            self.unchecked_decorators['event'].append(Event(name, func))
        return predicate
    
    def command(self, name, _type):
        def predicate(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("Command functions must be coroutine")
            self.unchecked_decorators['command'].append(Command(name, func, _type))
        return predicate

    def component(self, ucid):
        def predicate(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("Component function must be coroutine")
            self.unchecked_decorators['component'].append(Component(ucid, func))
        return predicate

    async def send_heartbeat(self, payload):
        await self.connection.send_json(payload)

    async def run_command(self, context):
        try: 
            coro = None
            if context.type == utils.SLASH:
                coro = self.events.commands.get(context.command, None)
            elif context.type == utils.USER:
                coro = self.events.user_commands.get(context.command, None)
            elif context.type == utils.MESSAGE:
                coro = self.events.message_commands.get(context.command, None)

            if coro is None:
                raise ValueError(f"No command with name {context.name} was found.")
        
            await coro(context)
        except Exception:
            traceback.print_exc()

    async def run_component_command(self, context):
        coro = None
        coro = self.events.components.get(context.ucid, None)
        
        if coro is None:
            raise ValueError(f"No component with unique id {context.ucid} was found.")
        try:
            await coro(context)
        except Exception:
            traceback.print_exc()

    async def run_ready_event(self):
        coro = None
        coro = self.events.events['on_ready'][0]
        if coro is not None:
            await coro()

    async def before_login(self):
        # Construct headers
        self.headers = {"Authorization": f"Bot {self.__token}"}
        self.session = aiohttp.ClientSession()
        # Make user
        self.user = User(await (await self.session.get('https://discord.com/api/v8/users/@me', headers=self.headers)).json())

    async def connect(self):
        await self.before_login()
        async with self.session.ws_connect("wss://gateway.discord.gg/") as connection:
            self.connection = connection
            async for message in connection:
                msg = json.loads(message.data)
                op, t, d = msg['op'], msg['t'], msg['d']

                if self.alive_handler:
                    self.alive_handler.tick()

                try:    

                    if op == utils.HELLO:  # Discord's 'Hello' payload
                        await connection.send_json(
                            {
                                "op": utils.IDENTIFY,
                                "d": {
                                    "token": self.__token,
                                    "intents": 513,
                                    "properties": {
                                        "$os": "Windows",
                                        "$browser": "discsocket 1.0.1",
                                        "$device": "discsocket 1.0.1"
                                    },
                                    "compress": False,
                                    "large_threshold": 250
                                }
                            }   
                        )
                        self.alive_handler = MaintainSocketAlive(socket=self, interval=d['heartbeat_interval'])
                        await connection.send_json(self.alive_handler.payload())
                        self.alive_handler.start()
                
                    elif op == utils.HEARTBEAT_ACK:
                        if self.alive_handler:
                            self.alive_handler.ack()
                
                    elif op == utils.HEARTBEAT:
                        if self.alive_handler:
                            connection.send_json(self.alive_handler.payload())

                    elif t == 'INTERACTION_CREATE':
                        if d['type'] == 2: # Slash command
                            try:
                                # inject type
                                d['injected'] = {"type": utils.SLASH}
                                model = Context(self, d)
                                await self.run_command(model)
                            except Exception:
                                traceback.print_exc()
                        elif d['type'] == 3:  # Component interaction
                            if d['data']['component_type'] == 3:
                                model = SelectMenuContext(self, d)
                            elif d['data']['component_type'] == 2:
                                model = ButtonContext(self, d)
                            await self.run_component_command(model)
                    elif t == 'READY':
                        await self.run_ready_event()
                except Exception:
                    traceback.print_exc()

    def add_extension(self, extension_path):
        extension = importlib.import_module(extension_path)
        for name in dir(extension):
            attr = getattr(extension, name)
            
            if isinstance(attr, Command):
                self.events.command(attr)
            elif isinstance(attr, Component):
                self.events.component(attr)
            elif isinstance(attr, Event):
                self.events.event(attr)
                    
    def run(self, token: str):

        for _type in ['event', 'command', 'component']:
            if len(self.unchecked_decorators[_type]) > 0:
                for listener in self.unchecked_decorators[_type]:
                    if isinstance(listener, Command):
                        self.events.command(listener)
                    elif isinstance(listener, Event):
                        self.events.event(listener)
                    elif isinstance(listener, Component):
                        self.events.component(listener)

        self.__token = token
        self.loop.create_task(self.connect())
        self.loop.run_forever()
    
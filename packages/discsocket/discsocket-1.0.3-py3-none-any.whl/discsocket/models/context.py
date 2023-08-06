from .components import ActionRow, Button, SelectMenu, SelectMenuOption
from .user import User
from .message import Message


class Context:
    def __init__(self, socket, data):
        injected = data.get('injected', None)
        self.socket = socket
        self.command = data['data'].get('name', None)
        self.command_id = data['data'].get('id', None)
        self.ucid = data['data'].get('custom_id')
        self.channel_id = data.get('channel_id', None)
        self.id = data['id']
        self.token = data['token']
        self.callback_url = f"https://discord.com/api/v8/interactions/{self.id}/{self.token}/callback"
        self.message = None
        self.data = data
        if injected is not None:
            self.type = injected['type']

    async def callback(self, content: str = '', embeds: list = [], components: list = [], mentions: list = []):
        built_action_rows = []
        for action_row in components:
            if isinstance(action_row, ActionRow):
                built_action_rows.append(action_row.build())

        fully_built = []
        for bar in built_action_rows:
            new_ar = {"type": 1, "components": []}
            for component in bar['components']:
                if isinstance(component, Button):
                    new_ar['components'].append(component.build())
                elif isinstance(component, SelectMenu):
                    select_options = []
                    built_select = component.build()
                    for option in built_select['options']:
                        if isinstance(option, SelectMenuOption):
                            select_options.append(option.build())
                    new_ar['components'].append({"type": 3, "custom_id": built_select['custom_id'], "options": select_options})
            fully_built.append(new_ar)

        message = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
                "components": fully_built,
                "allowed_mentions": mentions
            }
        }

        async with self.socket.session.post(self.callback_url, json=message, headers=self.socket.headers) as maybe_send:
            self.message = Message(self.socket, await (await self.socket.session.get(f"https://discord.com/api/v8/webhooks/{self.data['application_id']}/{self.token}/messages/@original", headers=self.socket.headers)).json())
            if maybe_send.status != 204:
                print(await maybe_send.json())


class SelectMenuContext:
    def __init__(self, socket, data):
        self.socket = socket
        self.data = data
        self.values = data['data']['values']
        self.used = User(data['member']['user'])
        self.invoked = User(data['message']['interaction']['user'])
        self.callback_url = f"https://discord.com/api/v8/interactions/{data['id']}/{data['token']}/callback"
        self.ucid = data['data']['custom_id']

    async def callback(self, content: str = '', embeds: list = [], allowed_mentions: list = []):
        message = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions
            }
        }

        async with self.socket.session.post(self.callback_url, json=message, headers=self.socket.headers) as maybe_send:
            print(maybe_send.status)
            if maybe_send.status != 204:
                print(await maybe_send.json())

class ButtonContext:
    def __init__(self, socket, data):
        self.socket = socket
        self.data = data
        self.ucid = data['data']['custom_id']
        self.invoked = User(data['message']['interaction']['user'])
        self.used = User(data['member']['user'])
        self.callback_url = f"https://discord.com/api/v8/interactions/{data['id']}/{data['token']}/callback"

    async def callback(self, content: str = '', embeds: list = [], allowed_mentions: list = []):
        message = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions
            }
        }

        async with self.socket.session.post(self.callback_url, json=message, headers=self.socket.headers) as maybe_send:
            print(maybe_send.status)
            if maybe_send.status != 204:
                print(await maybe_send.json())


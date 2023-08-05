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
        if injected is not None:
            self.type = injected['type']

    async def callback(self, content: str = '', embeds: list = [], components:list = [], mentions: list = []):
        cleaned_components = []
        for ar in components:
            new_ar = {"type": 1, "components": []}
            for component in ar['components']:
                if isinstance(component, dict):
                    new_ar['components'].append(component)
                else:
                    new_ar['components'].append(component.build())
            cleaned_components.append(new_ar)

        message = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
                "components": cleaned_components,
                "allowed_mentions": mentions
            }
        }

        async with self.socket.session.post(self.callback_url, json=message, headers=self.socket.headers) as maybe_send:
            if maybe_send.status not in [200, 201, 202, 204]:
                print(await maybe_send.json())


import asyncio
from .user import User

class Message:
    def __init__(self, socket, data):
        self.socket = socket
        print(data)
        self.data = data
        self.author = User(data['author'])
        self.id = data['id']
        self.channel_id = data['channel_id']
        self.components = data['components']
        self.embeds = data['embeds']
        self.content = data['content']

    async def component_timeout(self, timeout):
        async def process_timeout(self, timeout):
            await asyncio.sleep(timeout)
            for ar in self.components:
                for component in ar['components']:
                    component['disabled'] = True
                    print(component)
                    del self.socket.events.components[component['custom_id']]
            self.data['components'] = self.components
            await self.socket.session.patch(f"https://discord.com/api/v8/channels/{self.channel_id}/messages/{self.id}", json=self.data, headers=self.socket.headers)

        await process_timeout(self, timeout)
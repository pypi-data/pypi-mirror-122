from .. import utils

class User:
    """Represents a Discord user"""
    def __init__(self, data):
        self.data = data
        self.id = int(data['id']) # Discord sends the id as a string, convert to int
        self.discriminator = int(data['discriminator'])
        self.name = data['username']

    @property
    def avatar(self):
        return utils.return_cdn_avatar(self.data)
    
    @property
    def username(self):
        return str(self.name) + "#" + str(self.discriminator)

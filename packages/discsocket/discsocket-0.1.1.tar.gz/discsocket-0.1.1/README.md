# discsocket

Python framework for Discord interactions.

Example for a minimal application with an on_ready listener
```py
import discsocket

client = discsocket.Client()

# Event names go in the event decorator
# The function can be named whatever
@socket.event('on_ready')
async def ready():
  print("Socket is connected")
 
client.run('token')
```

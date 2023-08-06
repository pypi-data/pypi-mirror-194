# ZoomDotPy
Designed for use with a server-to-server oauth zoom developer app

# Install
`python3 -m pip install zoomdotpy`  

Bleeding Edge:  
`pip install git+https://github.com/Sceptyre/python-zoom.git@devel`

# Usage
```py
from zoomdotpy import ZoomClient

zoom = ZoomClient(
    '<API_KEY>',
    '<API_SECRET>'
)
```

```py
# List phone devices
zoom.phones.devices.list_devices()

# list phone sites
zoom.phones.sites.list_sites()

# List rooms
zoom.rooms.list_rooms()

# Get specific room
zoom.rooms.get_room('abc123')
```

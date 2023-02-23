import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from utils.parsers import json_serial


class JupyterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope["url_route"]["kwargs"]

        uid = kwargs["uid"]
        room = f"JUPYTER_{uid}"
        self.room_group_name = room

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept(subprotocol="Token")

    async def disconnect(self, close_code):
        if close_code == 401 or not hasattr(self, "room_group_name"):
            return
        else:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        raise StopConsumer()

    async def notify_jupyter_file_update(self, event):
        # Send message to webSocket (Frontend)
        data = event["data"]
        data = {
            "type": "update",
            "data": data,
        }
        await self.send(text_data=json.dumps(data, default=json_serial))

    async def notify_jupyter_server_progress(self, event):
        # Send message to webSocket (Frontend)
        data = event["data"]
        data = {
            "type": "loading_progress",
            "data": data,
        }
        await self.send(text_data=json.dumps(data, default=json_serial))

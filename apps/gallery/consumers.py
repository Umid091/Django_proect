import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GalleryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("gallery_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gallery_group", self.channel_name)

    async def send_image(self, event):
        await self.send(text_data=json.dumps({
            'image_url': event['image_url'],
            'id': event['id']
        }))

    async def delete_image(self, event):
        await self.send(text_data=json.dumps({
            'action': 'delete',
            'id': event['id']
        }))

    async def send_image_update(self, event):
        await self.send(text_data=json.dumps({
            'action': event['action'],
            'id': event['id'],
            'image_url': event['image_url']
        }))
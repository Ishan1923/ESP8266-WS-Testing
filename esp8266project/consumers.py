import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from . import models
from django.utils.timezone import now

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected!")
        await self.channel_layer.group_add("sensor_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected!")
        await self.channel_layer.group_discard("sensor_group", self.channel_name)
        
    async def receive(self, text_data):
        try:
            print("Recieved!")
            data = json.loads(text_data)
            print("RECIEVED DATA: ", text_data)
        except json.JSONDecodeError:
            data = {"error" : "Invalid JSON"}

        await self.save_to_db(data)

        await self.send(text_data = json.dumps({'message' : 'recieved', 'data' : data}))
        # await self.send(text_data = json.dumps({'message': 'recieved', 'data': data}))

        await self.channel_layer.group_send(
            "sensor_group",
            {
                "type" : "sensor_message",
                "text" : data,
            }
        )

    async def save_to_db(self, data):
        await sync_to_async(models.sensordata.objects.create)(text = data)

    async def sensor_message(self, event):
        # This is called when a message is sent to the group
        text = event["text"]
        await self.send(text_data=json.dumps({"text": text}))


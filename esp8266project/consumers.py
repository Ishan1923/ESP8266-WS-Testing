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
        await self.delete_from_curr_sess_db();
        await self.channel_layer.group_discard("sensor_group", self.channel_name)
        
    async def receive(self, text_data):
        try:
            print("Recieved!")
            data = json.loads(text_data)
            print("RECIEVED DATA: ", text_data)
        except json.JSONDecodeError:
            data = {"error" : "Invalid JSON"}
            return 
        
        if data.get("command") == "get_chart_data":
            print("GETTING CHART DATA")
            chart_data = await self.get_data()
            await self.send(text_data=json.dumps({"command": "get_chart_data", "data": chart_data}))
        elif data.get("command") == "delete_data":
            await self.delete_from_curr_sess_db()
            await self.send(text_data=json.dumps({"command": "delete_data", "status": "success"}))
            return

        await self.save_to_db(data)
        chart_data = await self.get_data()
        await self.send(text_data=json.dumps({
            "command": "get_chart_data", 
            "data": chart_data
            }))

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
        await sync_to_async(models.sensordata.objects.using('default').create)(text = data)
        await sync_to_async(models.sensordata.objects.using('current_session').create)(text = data)
    
    async def delete_from_curr_sess_db(self):
        await sync_to_async(
            lambda: models.sensordata.objects.using('current_session').all().delete()
            )()

    async def sensor_message(self, event):
        # This is called when a message is sent to the group
        text = event["text"]
        await self.send(text_data=json.dumps({"text": text}))

    async def get_data(self):
        raw_data = await sync_to_async(
            lambda: list(models.sensordata.objects.using('current_session').all().values('timestamp', 'text'))
        )()

        # formatted_data = [
        #     {
        #         "timestamp": str(item["timestamp"]),
        #         **item["text"]  # unpack JSONField into flat keys (like temperature, humidity, etc.)
        #     }
        #     for item in raw_data
        # ]

        filtered_data = []
        for item in raw_data:
            text = item['text']
            # Only include if 'data' key exists and x, y, z are numeric
            data = text.get('data')
            if data:
                x, y, z = data.get('x'), data.get('y'), data.get('z')
                if all(isinstance(v, (int, float)) for v in (x, y, z)):
                    filtered_data.append({
                        'timestamp': str(item['timestamp']),
                        **data
                    })


        return filtered_data
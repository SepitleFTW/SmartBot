import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join a room group
        await self.channel_layer.group_add(
            "chat_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            "chat_group",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['text']
        ai_choice = data['ai_choice']

        # Process the message and get a response from the AI
        response = await self.get_ai_response(message, ai_choice)

        # Send the response to the WebSocket
        await self.channel_layer.group_send(
            "chat_group",
            {
                'type': 'chat_message',
                'message': response
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }, cls=DjangoJSONEncoder))

    async def get_ai_response(self, message, ai_choice):
        # Implement AI response logic here
        # For example:
        if ai_choice == 'openai':
            response = await self.get_openai_response(message)
        elif ai_choice == 'huggingface':
            response = await self.get_huggingface_response(message)
        else:
            response = "Unknown AI choice"
        return response

    async def get_openai_response(self, message):
        # Placeholder function for OpenAI response
        # Replace with actual OpenAI API call
        return "OpenAI response to: " + message

    async def get_huggingface_response(self, message):
        # Placeholder function for HuggingFace response
        # Replace with actual HuggingFace API call
        return "HuggingFace response to: " + message

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from .ai_model import generate_response


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
        try:
            data = json.loads(text_data)
            message = data.get('text')  # Using get to avoid KeyError
            ai_choice = data.get('ai_choice')

            if message is None or ai_choice is None:
                raise ValueError("Both 'text' and 'ai_choice' must be provided.")

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
        except json.JSONDecodeError:
            logging.error("Invalid JSON received.")
            await self.send(text_data=json.dumps({'error': 'Invalid JSON received.'}))
        except Exception as e:
            logging.error(f"Error in receive: {str(e)}")
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }, cls=DjangoJSONEncoder))

    async def get_ai_response(self, message, ai_choice):
        if ai_choice == 'openai':
            response = await self.get_openai_response(message)
        elif ai_choice == 'huggingface':
            response = await self.get_huggingface_response(message)
        elif ai_choice == 't5':
            response = await self.get_t5_response(message)
        else:
            response = "Unknown AI choice"
        return response

    #below this will give responses
    async def get_openai_response(self, message):
        return generate_response(message, model_choice='openai')

    async def get_huggingface_response(self, message):
        return generate_response(message, model_choice='huggingface')

    async def get_t5_response(self, message):
        return generate_response(message, model_choice='t5')

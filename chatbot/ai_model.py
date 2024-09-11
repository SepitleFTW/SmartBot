from transformers import pipeline
import openai
import os
from dotenv import load_dotenv

load_dotenv() #loadiing env variables  from .env file

#API keys from env file
openai.api_key = os.getenv('OPENAI_API_KEY')
huggingface_token = os.getenv('HUGGINGFACE_TOKEN')

# Initialize the Hugging Face model
generator = pipeline('text-generation', model='gpt2', token=huggingface_token, temperature=0.2)

# Response generation for Hugging Face model
def generate_huggingface_response(user_input):
    try:
        """
        Generate a response from HF GPT-2 model
        """
        response = generator(user_input, max_length=50, num_return_sequences=1)
        return response[0]['generated_text'].strip()
    except Exception as e:
        return f"Error generating Hugging Face response: {str(e)}"

# OpenAI API key setting
openai.api_key = os.getenv('OPENAI_API_KEY')

# Response generation from OpenAI
def generate_openai_response(user_input):
    try:
        """Get a response from OpenAI using the relevant GPT model"""
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        # Access the response
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating OpenAI response: {str(e)}"

# This function allows choosing between both models
def generate_response(user_input, model_choice='openai'):
    if model_choice == 'huggingface':
        return generate_huggingface_response(user_input)
    elif model_choice == 'openai':
        return generate_openai_response(user_input)
    else:
        return "Invalid model choice"

<<<<<<< HEAD
from transformers import pipeline

# Initialize the Hugging Face model
generator = pipeline('text-generation', model='gpt2')

def generate_huggingface_response(user_input):
    try:
        # Generate a response
        response = generator(user_input, max_length=50, num_return_sequences=1)
        return response[0]['generated_text'].strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"
=======
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_huggingface_response(user_input):
    pass


def generate_openai_response(user_input):
    pass


def generate_response(user_input):
    try:
        # Create a chat completion
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        # Access the response content
        return response.choices[0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

print(generate_response("Guten tag! How are you?"))
>>>>>>> 3c64a5d7dd991056716409f1a8efe3cc9c005275

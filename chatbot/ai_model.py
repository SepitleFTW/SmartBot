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

import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_response(user_input):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_input,
        max_tokens=50
    )
    return response.choices[0].text.strip()

print(generate_response("Guten tag! How are you?"))

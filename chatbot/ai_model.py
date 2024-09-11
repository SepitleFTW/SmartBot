from transformers import pipeline
import openai
import os

#initing the huggingface model
generator = pipeline('text-generation', model='gpt-2')

#response generation for hugging face model
def generate_huggingface_response(user_input):
    try:
        """
        generate a response form HF GPT-2 model
        """
        response = generator(user_input, max_length=50, num_return_sequences=1)
        return response[0]['generated_text'].strip()
    except Exception as e:
        return f"Error generating Hugging Face response: {str(e)}"

# OpenAI API key setting
openai.api_key = os.getenv('OPENAI_API_KEY')

# response generation from OPENAI
def generate_openai_response(user_input):
    try:
        """getting a response from OPEN ai using
        relevant GPT model(might have to purchas)
        """
        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
        #access the response
        return response.choices[0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating OPENAI response {str(e)}"

#this function below allows to choose betweeen both Models
def generate_response(user_input, model_choice='openai'):
    if model_choice == 'huggingface':
        return generate_huggingface_response(user_input)
    elif model_choice == 'openai':
        return generate_openai_response(user_input)
    else:
        return "Invalid model choice"

#an example
print(generate_response("Guten tag! How are you?", model_choice='openai'))
print(generate_response("Guten tag! How are you?", model_choice='huggingface'))

from transformers import pipeline, AutoTokenizer
import openai
import os
from dotenv import load_dotenv
import logging
import nltk
from nltk.tokenize import word_tokenize
from transformers import T5Tokenizer, T5ForConditionalGeneration

#configuring logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv() #loadiing env variables  from .env file

#downloading the necessary NLTK data
nltk.download('punkt')

#API keys from env file
openai.api_key = os.getenv('OPENAI_API_KEY')
huggingface_token = os.getenv('HUGGINGFACE_TOKEN')

# Initialize the Hugging Face model
tokenizer = AutoTokenizer.from_pretrained('gpt2')
generator = pipeline('text-generation', model='gpt2', token=huggingface_token, temperature=0.7)

#preprocessing function
def preprocess_text(text):
    tokens = word_tokenize(text.lower()) #lowercase and tokenize text
    return ' '.join(tokens)

# Response generation for Hugging Face model
def generate_huggingface_response(user_input):
    logging.info(f"Generating Hugging Face response for input: {user_input}")
    try:
        """
        Generate a response from HF GPT-2 model
        and preprocess input
        """
        user_input = preprocess_text(user_input)


        response = generator(user_input, max_length=50, num_return_sequences=1) # response generation using HF model
        return response[0]['generated_text'].strip()
    except Exception as e:
        logging.error(f"Error generating Hugging Face response: {str(e)}")
        return f"Error generating Hugging Face response: {str(e)}"

# OpenAI API key setting
openai.api_key = os.getenv('OPENAI_API_KEY')

# Response generation from OpenAI
def generate_openai_response(user_input):
    logging.info(f"Generating OpenAi response for input: {user_input}")
    try:
        """Get a response from OpenAI using the relevant GPT model
        preprocess input.
        """

        user_input = preprocess_text(user_input)

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        # Access the response
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error generating OpenAI Response{str(e)}")
        return f"Error generating OpenAI response: {str(e)}"

# This function allows choosing between both models
def generate_response(user_input, model_choice='openai'):
    if model_choice == 'huggingface':
        return generate_huggingface_response(user_input)
    elif model_choice == 'openai':
        return generate_openai_response(user_input)
    else:
        return "Invalid model choice"


#loading the fine tuned model
model = T5ForConditionalGeneration.from_pretrained('chatbot/ml/trained_models/fine_tuned_t5')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

def generate_response(input_text):
    inputs = tokenizer(input_text, return_tensors='pt')
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

import google.generativeai as genai
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
import openai
import os
from dotenv import load_dotenv
import logging
import nltk

# Configuring logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()  # Loading env variables from .env file

# Downloading the necessary NLTK data, specifically 'punkt' tokenizer
try:
    nltk.download('punkt', quiet=True)
except Exception as e:
    logging.error(f"Error downloading NLTK data: {str(e)}")

# API keys from env file
openai.api_key = os.getenv('OPENAI_API_KEY')
huggingface_token = os.getenv('HUGGINGFACE_TOKEN')
gemini_api = os.getenv('GEMINI_API_KEY')

#setting up gemini client
#gemini_client = gemini.Client(api_key=gemini_api)

#Initializing the gemini model
gemini_model = genai.GenerativeModel(model_name='gemini-pro-vision')

# Initialize the Hugging Face model
generator = pipeline('text-generation', model='gpt2', token=huggingface_token, temperature=0.7)

# Initialize T5 model and tokenizer
t5_model_path = '/workspaces/SmartBot/chatbot/ml/trained_models/fine_tuned_t5'
t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_path)
t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_path)

# Preprocessing function
def preprocess_text(text):
    # Lowercase and tokenize text using the 'punkt' tokenizer
    try:
        tokens = nltk.word_tokenize(text.lower())
        return ' '.join(tokens)
    except Exception as e:
        logging.error(f"Error during tokenization: {str(e)}")
        return text  # Return the original text if tokenization fails

# Response generation for Hugging Face model
def generate_huggingface_response(user_input):
    logging.info(f"Generating Hugging Face response for input: {user_input}")
    try:
        user_input = preprocess_text(user_input)
        response = generator(
            user_input, 
            max_length=50, 
            num_return_sequences=1, 
            temperature=1,
            truncation=True,
            pad_token_id=t5_tokenizer.eos_token_id
        )
         
        return response[0]['generated_text'].strip()
    except Exception as e:
        logging.error(f"Error generating Hugging Face response: {str(e)}")
        return f"Error generating Hugging Face response: {str(e)}"

# Response generation from OpenAI
def generate_openai_response(user_input):
    logging.info(f"Generating OpenAI response for input: {user_input}")
    try:
        user_input = preprocess_text(user_input)
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error generating OpenAI Response: {str(e)}")
        return f"Error generating OpenAI response: {str(e)}"


# Generate response using the fine-tuned T5 model
def generate_t5_response(input_text):
    # Format the input for the model
    formatted_input = f"question: {input_text}" 
    inputs = t5_tokenizer(formatted_input, return_tensors='pt')

    # Checks input length
    input_ids = inputs.input_ids
    print("Input length:", input_ids.shape[1])

    try:
        outputs = t5_model.generate(
            **inputs,
            max_length=20,
            num_beams=5,
            num_return_sequences=1,
            early_stopping=True
        )
        return t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Error generating T5 response: {str(e)}")
        return f"Error generating T5 response: {str(e)}"

def generate_gemini_response(user_input):
    """
    calling the gemini API and getting a response
    """
    try:
        response = gemini_model.generate_conversation(prompt=user_input)
        return response['response']
    except Exception as e:
        logging.error(f"There was an unkown error generating Gemini response: {str(e)}")
        return f"There was an unkown  error generating Gemini response: {str(e)}"


# This function allows choosing between both models
def generate_response(user_input, model_choice='openai'):
    if model_choice == 'huggingface':
        return generate_huggingface_response(user_input)
    elif model_choice == 'openai':
        return generate_openai_response(user_input)
    elif model_choice == 't5':
        return generate_t5_response(user_input)
    elif model_choice == 'gemini':
        return generate_gemini_response(user_input)
    else:
        return "Invalid model choice"

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

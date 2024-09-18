from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the model and tokenizer (consider caching these for efficiency)
model = T5ForConditionalGeneration.from_pretrained('ml/trained_models')
tokenizer = T5Tokenizer.from_pretrained('ml/trained_models')

def generate_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'])
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response_text

from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset

# Load the pre-trained model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Load your custom dataset (you could have this stored locally or fetched from elsewhere)
dataset = load_dataset('csv', data_files='ml/training_data.csv')

# Tokenize the input
def preprocess_function(examples):
    return tokenizer(examples['input_text'], truncation=True, padding=True, max_length=512)

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./ml/trained_models',  # Where the model will be saved
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Define a Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['test']
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
trainer.save_model('./ml/trained_models/fine_tuned_t5')

from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset
import os

# Load tokenizer and model
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Define the path to your JSON file
data_path = "/workspaces/SmartBot/chatbot/ml/learning.json"

# Load the custom dataset (JSON)
dataset = load_dataset('json', data_files={'train': data_path})

# Split the dataset into training and validation sets
split_dataset = dataset['train'].train_test_split(test_size=0.1, seed=42)
train_dataset = split_dataset['train']
test_dataset = split_dataset['test']

# Preprocess the dataset by tokenizing inputs and targets
def preprocess_function(examples):
    inputs = examples['input_text']
    targets = examples['target_text']
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")

    # Tokenize targets
    labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length").input_ids
    model_inputs["labels"] = labels
    return model_inputs

# Apply the preprocessing to the dataset
train_dataset = train_dataset.map(preprocess_function, batched=True)
test_dataset = test_dataset.map(preprocess_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./ml/trained_models",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=1,
    weight_decay=0.01
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# Start training
trainer.train()

# Save the fine-tuned model and tokenizer
model_save_path = '/workspaces/SmartBot/chatbot/ml/trained_models/fine_tuned_t5'
os.makedirs(model_save_path, exist_ok=True)
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)

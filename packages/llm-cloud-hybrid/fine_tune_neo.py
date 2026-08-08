from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling

model_name = "EleutherAI/gpt-neo-125M"

# Load tokenizer and set pad token if missing
tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load model
model = AutoModelForCausalLM.from_pretrained(model_name)

# Add special tokens for QA tags if needed
special_tokens = {'additional_special_tokens': ['<question>', '</question>', '<answer>', '</answer>']}
num_added_toks = tokenizer.add_special_tokens(special_tokens)
if num_added_toks > 0:
    model.resize_token_embeddings(len(tokenizer))

# Load dataset (your QA data file)
dataset = load_dataset("text", data_files={"train": "my_training_data.txt"})

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="./fine_tuned_neo",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=500,
    save_total_limit=2,
    logging_steps=100,
    # Remove evaluation_strategy if your transformers version does not support it,
    # or upgrade transformers package to >=4.11.0
    overwrite_output_dir=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    data_collator=data_collator,
)

trainer.train()
trainer.save_model("./fine_tuned_neo")
tokenizer.save_pretrained("./fine_tuned_neo")

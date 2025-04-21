# Fine-tunes Meta’s LLaMA 3.2-1B-Instruct on the EmpatheticDialogues dataset
# Designed to scale to larger models with sufficient GPU resources

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import json
import os

# Optional: Disable MPS memory cap on Mac with limited GPU resources(harmless on other platforms)
# os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
# print("MPS high watermark cap disabled for macOS.")

# Load base model and tokenizer
model_name = "meta-llama/Llama-3.2-1B-Instruct"
print("Loading tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name)

# Enable memory optimizations
model.gradient_checkpointing_enable()
model.config.use_cache = False

# Load and truncate preprocessed data
print("Loading and truncating processed dataset...")
with open("processed_dataset.json", "r") as f:
    processed_data = json.load(f)

processed_data = processed_data[:len(processed_data) // 10]  # 10% for demo/faster runs but use full dataset with sufficient GPU resources
print(f"Loaded {len(processed_data)} examples.")

# Convert to Hugging Face Dataset format
dataset = Dataset.from_list(processed_data)
split = dataset.train_test_split(test_size=0.2)
train_dataset = split["train"]
eval_dataset = split["test"]

# Set up data collator for Causal LM
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Training configuration — adjust for larger models
training_args = TrainingArguments(
    output_dir="./empathetic_model",
    evaluation_strategy="steps",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=2,
    learning_rate=5e-5,
    num_train_epochs=1,
    eval_steps=100,
    save_steps=100,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=50,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    warmup_steps=100,
    weight_decay=0.01,
    # fp16=True  # Uncomment if using GPU with FP16 support
)

# Define Trainer with early stopping
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)

# Begin training
print("Starting fine-tuning...")
trainer.train()

# Save model + tokenizer
print("Saving fine-tuned model to ./empathetic_model")
model.save_pretrained("./empathetic_model")
tokenizer.save_pretrained("./empathetic_model")

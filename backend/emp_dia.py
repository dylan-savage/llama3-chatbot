from datasets import load_dataset
from transformers import AutoTokenizer
import json

dataset = load_dataset("Estwld/empathetic_dialogues_llm", split="train")

model_name = "meta-llama/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# Preprocess dataset
def preprocess_function(examples):
    processed_data = []
    
    for situation, conversations in zip(examples["situation"], examples["conversations"]):
        user_text = []
        assistant_text = []
        
        for turn in conversations:
            if turn["role"] == "user":
                user_text.append(turn["content"])
            elif turn["role"] == "assistant":
                assistant_text.append(turn["content"])
        
        input_text = f"[INST] Context: {situation}\nUser: {' '.join(user_text)}\nProvide an empathetic response: [/INST]"
        output_text = f"{' '.join(assistant_text)}</s>"
        
        # Ensure no empty inputs or labels
        if not input_text.strip() or not output_text.strip():
            print("Skipping empty input/output example...")
            continue
        
        full_text = input_text + " " + output_text
    
        tokenized = tokenizer(full_text, truncation=True, max_length=512, padding="max_length")
        
        processed_data.append({
            "input_ids": tokenized["input_ids"],
            "attention_mask": tokenized["attention_mask"],
            "labels": tokenized["input_ids"].copy()  
        })
    
    return processed_data

print("Processing dataset...")
processed_dataset = preprocess_function(dataset)

# Save processed dataset to file
output_file = "processed_dataset.json"


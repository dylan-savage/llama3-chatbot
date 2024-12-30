from transformers import AutoModelForCausalLM, AutoTokenizer

# Specify the model name
model_name = "meta-llama/Llama-3"  # Replace this with the actual Llama 3 model name from Hugging Face

# Load the tokenizer and model
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(model_name)

print("Model and tokenizer loaded successfully!")

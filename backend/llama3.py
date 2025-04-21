from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from sentiment_analyzer import SentimentAnalyzer

class EmpathyBot:
    def __init__(self, use_finetuned_model=False, model_path="./empathetic_model"):
        try:
            self.model_path = model_path if use_finetuned_model else "meta-llama/Llama-3.2-1B-Instruct"

            print(f"Loading model from: {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)

            self.sentiment_analyzer = SentimentAnalyzer()
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise RuntimeError(f"Failed to initialize EmpathyBot: {str(e)}")
    
    def generate_response(self, input_text):
        try:
            if not input_text or not isinstance(input_text, str):
                raise ValueError("Invalid input text")

            sentiment = self.sentiment_analyzer.get_sentiment_label(input_text)

            inputs = self.tokenizer(input_text, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=50,
                    temperature=0.8,
                    do_sample=True
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            return {
                "response": response,
                "sentiment": sentiment,
                "sentiment_scores": self.sentiment_analyzer.analyze(input_text)
            }

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return {
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your message."
            }


if __name__ == "__main__":
    # Run this block manually by running 'python llama3.py' to test with either model
    bot = EmpathyBot(use_finetuned_model=False)  # Set to True if your model is ready
    input_text = "I have been feeling sad lately"
    result = bot.generate_response(input_text)
    print("User Input:", input_text)
    print("Detected Sentiment:", result["sentiment"])
    print("Sentiment Scores:", result["sentiment_scores"])
    print("Bot Response:", result["response"])

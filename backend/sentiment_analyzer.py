from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            return_all_scores=True
        )
    
    def analyze(self, text):
 
        results = self.analyzer(text)[0]
        sentiment_scores = {score['label']: score['score'] for score in results}
        return sentiment_scores
    
    def get_sentiment_label(self, text):
 
        scores = self.analyze(text)
        return max(scores.items(), key=lambda x: x[1])[0] 
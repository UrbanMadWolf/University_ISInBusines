from textblob import TextBlob
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

class SentimentAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.classifier = MultinomialNB()
        
    def analyze_sentiment_textblob(self, text):
        """Analyze sentiment using TextBlob"""
        try:
            # Translate to English for better sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive', polarity
            elif polarity < -0.1:
                return 'negative', polarity
            else:
                return 'neutral', polarity
        except:
            return 'neutral', 0.0
    
    def train_sentiment_classifier(self, X_train, y_train):
        """Train sentiment classifier"""
        X_train_vec = self.vectorizer.fit_transform(X_train)
        self.classifier.fit(X_train_vec, y_train)
        
    def predict_sentiment(self, text):
        """Predict sentiment for new text"""
        text_vec = self.vectorizer.transform([text])
        return self.classifier.predict(text_vec)[0]
    
    def evaluate_sentiment(self, X_test, y_test):
        """Evaluate sentiment classifier performance"""
        X_test_vec = self.vectorizer.transform(X_test)
        y_pred = self.classifier.predict(X_test_vec)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        return accuracy, report
    
    def get_sentiment_distribution(self, texts):
        """Get distribution of sentiments in a list of texts"""
        sentiments = []
        for text in texts:
            sentiment, _ = self.analyze_sentiment_textblob(text)
            sentiments.append(sentiment)
            
        return {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral')
        } 
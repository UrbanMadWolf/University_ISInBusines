from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

class ReviewClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.classifier = MultinomialNB()
        self.categories = [
            'Качество обслуживания',
            'Качество размещения',
            'Транспортные услуги',
            'Бронирование и оплата',
            'Прочее'
        ]
        
    def train_classifier(self, X_train, y_train):
        """Train the review classifier"""
        X_train_vec = self.vectorizer.fit_transform(X_train)
        self.classifier.fit(X_train_vec, y_train)
        
    def predict_category(self, text):
        """Predict category for new text"""
        text_vec = self.vectorizer.transform([text])
        return self.classifier.predict(text_vec)[0]
    
    def predict_proba(self, text):
        """Get probability scores for each category"""
        text_vec = self.vectorizer.transform([text])
        return self.classifier.predict_proba(text_vec)[0]
    
    def evaluate_classifier(self, X_test, y_test):
        """Evaluate classifier performance"""
        X_test_vec = self.vectorizer.transform(X_test)
        y_pred = self.classifier.predict(X_test_vec)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        return accuracy, report
    
    def get_category_distribution(self, texts):
        """Get distribution of categories in a list of texts"""
        categories = []
        for text in texts:
            category = self.predict_category(text)
            categories.append(category)
            
        distribution = {}
        for category in self.categories:
            distribution[category] = categories.count(category)
            
        return distribution
    
    def get_confidence_scores(self, text):
        """Get confidence scores for each category"""
        probas = self.predict_proba(text)
        return dict(zip(self.categories, probas)) 
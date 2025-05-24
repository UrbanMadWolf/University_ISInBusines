import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk

class DataProcessor:
    def __init__(self):
        # Download necessary NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('russian'))
        
    def load_data(self, file_path):
        """Load data from CSV file"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def preprocess_text(self, text):
        """Preprocess text data"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        
        # Tokenization
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def prepare_data(self, df):
        """Prepare data for analysis"""
        if df is None:
            return None
            
        # Preprocess review text
        df['processed_text'] = df['review_text'].apply(self.preprocess_text)
        
        # Convert rating to sentiment (if available)
        df['sentiment'] = df['rating'].apply(
            lambda x: 'positive' if x >= 4 else 'negative' if x <= 2 else 'neutral'
        )
        
        return df
    
    def split_data(self, df, test_size=0.2):
        """Split data into train and test sets"""
        from sklearn.model_selection import train_test_split
        
        # Split only for labeled data
        labeled_data = df[df['manual_labels'].notna()]
        
        X = labeled_data['processed_text']
        y = labeled_data['manual_labels']
        
        return train_test_split(X, y, test_size=test_size, random_state=42) 
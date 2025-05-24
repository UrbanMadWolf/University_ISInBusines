import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

class Visualizer:
    def __init__(self):
        # Use a built-in style instead of seaborn
        plt.style.use('default')
        # Set seaborn style using the function instead
        sns.set_theme()
        
    def plot_sentiment_distribution(self, sentiment_dist):
        """Plot sentiment distribution"""
        plt.figure(figsize=(10, 6))
        plt.bar(sentiment_dist.keys(), sentiment_dist.values())
        plt.title('Распределение тональности отзывов')
        plt.xlabel('Тональность')
        plt.ylabel('Количество отзывов')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt
        
    def plot_category_distribution(self, category_dist):
        """Plot category distribution"""
        plt.figure(figsize=(12, 6))
        plt.bar(category_dist.keys(), category_dist.values())
        plt.title('Распределение отзывов по категориям')
        plt.xlabel('Категория')
        plt.ylabel('Количество отзывов')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt
        
    def plot_sentiment_trend(self, df):
        """Plot sentiment trend over time"""
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        monthly_sentiment = df.groupby('month')['sentiment'].value_counts().unstack()
        
        plt.figure(figsize=(12, 6))
        monthly_sentiment.plot(kind='line', marker='o')
        plt.title('Динамика тональности отзывов по месяцам')
        plt.xlabel('Месяц')
        plt.ylabel('Количество отзывов')
        plt.legend(title='Тональность')
        plt.tight_layout()
        return plt
        
    def plot_category_sentiment(self, df):
        """Plot sentiment distribution by category"""
        plt.figure(figsize=(12, 6))
        sns.countplot(data=df, x='manual_labels', hue='sentiment')
        plt.title('Распределение тональности по категориям')
        plt.xlabel('Категория')
        plt.ylabel('Количество отзывов')
        plt.xticks(rotation=45)
        plt.legend(title='Тональность')
        plt.tight_layout()
        return plt
        
    def create_summary_table(self, df):
        """Create summary statistics table"""
        summary = pd.DataFrame({
            'Количество отзывов': df.groupby('manual_labels').size(),
            'Средняя оценка': df.groupby('manual_labels')['rating'].mean(),
            'Процент негативных отзывов': df[df['sentiment'] == 'negative'].groupby('manual_labels').size() / 
                                        df.groupby('manual_labels').size() * 100
        })
        return summary
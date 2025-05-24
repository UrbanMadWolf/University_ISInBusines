import streamlit as st
import pandas as pd
import sys
import os

# Add the PZ_3 directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'PZ_3'))

from data_processor import DataProcessor
from sentiment_analyzer import SentimentAnalyzer
from review_classifier import ReviewClassifier
from visualizer import Visualizer

def main():
    st.title('Анализ отзывов клиентов ООО "ТурСервис"')
    
    # Initialize components
    data_processor = DataProcessor()
    sentiment_analyzer = SentimentAnalyzer()
    review_classifier = ReviewClassifier()
    visualizer = Visualizer()
    
    # File upload
    uploaded_file = st.file_uploader("Загрузите файл с отзывами (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        # Load and process data
        df = data_processor.load_data(uploaded_file)
        df = data_processor.prepare_data(df)
        
        # Split data for training
        X_train, X_test, y_train, y_test = data_processor.split_data(df)
        
        # Train models
        sentiment_analyzer.train_sentiment_classifier(X_train, df.loc[X_train.index, 'sentiment'])
        review_classifier.train_classifier(X_train, y_train)
        
        # Sidebar for navigation
        st.sidebar.title('Навигация')
        page = st.sidebar.radio('Выберите раздел:', 
                              ['Общая статистика', 'Анализ тональности', 
                               'Классификация отзывов', 'Рекомендации'])
        
        if page == 'Общая статистика':
            st.header('Общая статистика')
            
            # Display basic statistics
            st.subheader('Распределение тональности')
            sentiment_dist = sentiment_analyzer.get_sentiment_distribution(df['review_text'])
            st.pyplot(visualizer.plot_sentiment_distribution(sentiment_dist))
            
            st.subheader('Распределение по категориям')
            category_dist = review_classifier.get_category_distribution(df['review_text'])
            st.pyplot(visualizer.plot_category_distribution(category_dist))
            
            st.subheader('Динамика тональности')
            st.pyplot(visualizer.plot_sentiment_trend(df))
            
        elif page == 'Анализ тональности':
            st.header('Анализ тональности')
            
            # Single review analysis
            st.subheader('Анализ отдельного отзыва')
            review_text = st.text_area('Введите текст отзыва:')
            if review_text:
                sentiment, polarity = sentiment_analyzer.analyze_sentiment_textblob(review_text)
                st.write(f'Тональность: {sentiment}')
                st.write(f'Полярность: {polarity:.2f}')
            
            # Sentiment distribution by category
            st.subheader('Распределение тональности по категориям')
            st.pyplot(visualizer.plot_category_sentiment(df))
            
        elif page == 'Классификация отзывов':
            st.header('Классификация отзывов')
            
            # Single review classification
            st.subheader('Классификация отдельного отзыва')
            review_text = st.text_area('Введите текст отзыва:')
            if review_text:
                category = review_classifier.predict_category(review_text)
                confidence = review_classifier.get_confidence_scores(review_text)
                
                st.write(f'Предполагаемая категория: {category}')
                st.write('Уверенность в категориях:')
                for cat, conf in confidence.items():
                    st.write(f'{cat}: {conf:.2%}')
            
            # Model evaluation
            st.subheader('Оценка качества классификации')
            accuracy, report = review_classifier.evaluate_classifier(X_test, y_test)
            st.write(f'Точность классификации: {accuracy:.2%}')
            st.text(report)
            
        else:  # Recommendations
            st.header('Рекомендации')
            
            # Summary statistics
            st.subheader('Сводная статистика по категориям')
            summary = visualizer.create_summary_table(df)
            st.dataframe(summary)
            
            # Generate recommendations
            st.subheader('Рекомендации по улучшению')
            
            # Analyze negative reviews
            negative_reviews = df[df['sentiment'] == 'negative']
            category_issues = negative_reviews.groupby('manual_labels').size()
            
            for category, count in category_issues.items():
                st.write(f'**{category}**:')
                st.write(f'Количество негативных отзывов: {count}')
                st.write('Рекомендации:')
                if category == 'Качество обслуживания':
                    st.write('- Улучшить обучение персонала')
                    st.write('- Внедрить систему оценки качества обслуживания')
                elif category == 'Качество размещения':
                    st.write('- Проводить регулярные проверки качества номеров')
                    st.write('- Улучшить систему контроля чистоты')
                elif category == 'Транспортные услуги':
                    st.write('- Улучшить координацию с транспортными компаниями')
                    st.write('- Внедрить систему отслеживания задержек')
                elif category == 'Бронирование и оплата':
                    st.write('- Улучшить пользовательский интерфейс сайта')
                    st.write('- Расширить способы оплаты')
                st.write('---')

if __name__ == '__main__':
    main() 
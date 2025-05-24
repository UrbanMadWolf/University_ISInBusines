@echo off
echo Installing Python dependencies...

:: Set environment variables for build tools
set DISTUTILS_USE_SDK=1
set MSSdk=1

:: Install build tools
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel build

:: Install numpy and pandas using pre-built wheels
pip install --only-binary :all: numpy==2.2.6
pip install --only-binary :all: pandas==2.2.0

:: Install other dependencies with compatible versions
pip install --only-binary :all: scikit-learn==1.4.0
pip install nltk==3.8.1
pip install spacy==3.7.2
pip install --only-binary :all: matplotlib==3.8.2
pip install seaborn==0.13.1
pip install streamlit==1.31.0
pip install textblob==0.17.1
pip install python-dateutil==2.8.2
pip install pytz==2024.1

:: Download spaCy model
python -m spacy download ru_core_news_sm

echo Installation complete!
pause 
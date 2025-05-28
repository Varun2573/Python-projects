# Emotion Recognition from Text Using BERT

This project aims to recognize emotions from text using **BERT (Bidirectional Encoder Representations from Transformers)**, a state-of-the-art transformer-based language model. It applies advanced NLP and deep learning techniques to classify text into emotions like **joy, sadness, anger, fear, surprise**, and more. The system features a user-friendly web interface built with **Streamlit**.

## 📌 Features

- 🔠 Accepts free-form text as input.
- 🤖 Uses a fine-tuned BERT model for emotion classification.
- 📊 Displays prediction with emotion probabilities in bar chart form.
- 🌐 Simple, interactive frontend with Streamlit.
- 📁 Cleaned, preprocessed training data for accurate predictions.

## 🧠 Technologies Used

- Python 3.11
- BERT (via `ktrain`)
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Neattext

## Data

The data is availabel in data folder where the dataset contains many different sentences labeled with an emotion.

## Data Preprocessing

We have used several data cleaning techniques using NLP. You can see the code how the model is been trained in training folder

## BERT Model

BERT (Bidirectional Encoder Representations from Transformers) is used in this project because of its powerful ability to understand the context of words in a sentence by looking at both the left and right sides of a word simultaneously. Traditional models often struggle to capture subtle emotional cues, sarcasm, or complex sentence structures, but BERT’s deep, bidirectional transformer architecture allows it to grasp nuanced language patterns. This makes it particularly well-suited for emotion recognition tasks where understanding the full context of a sentence is critical for accurate classification. By fine-tuning a pre-trained BERT model on an emotion-labeled dataset, we significantly enhance the accuracy and generalizability of emotion detection from text.

## Setup

- Install these Libraries(pip install streamlit pandas numpy matplotlib scikit-learn ktrain neattext)
- Set the path for model to import the trained model into the code
- Use this command to run the project(streamlit run app.py)
- You can see the application running on (http://localhost:8501)

## Test the Application

- Enter a text phrase in the input box (e.g., "I am very happy today!").
- Submit and view the predicted emotion with a bar chart showing probabilities.


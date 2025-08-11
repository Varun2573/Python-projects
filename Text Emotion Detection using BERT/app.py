import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import ktrain
from ktrain import text

# Load the ktrain predictor
predictor = ktrain.load_predictor("https://drive.google.com/drive/folders/1Cp_oNp6S85lONClDbOUd7IW5VbthoY0C?usp=sharing/")

emotions_emoji_dict = {
    "anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗",
    "joy": "😂", "neutral": "😐", "sad": "😔", "sadness": "😔",
    "shame": "😳", "surprise": "😮"
}


def predict_emotions(docx):
    results = predictor.predict([docx])
    return results[0]


def get_prediction_proba(docx):
    results = predictor.predict_proba([docx])
    return results


def main():
    st.title("Text Emotion Detection")
    st.subheader("Detect Emotions In Text")

    with st.form(key='my_form'):
        raw_text = st.text_area("Type Here")
        submit_text = st.form_submit_button(label='Submit')

    if submit_text:
        col1, col2 = st.columns(2)

        prediction = predict_emotions(raw_text)
        probability = get_prediction_proba(raw_text)

        with col1:
            st.success("Original Text")
            st.write(raw_text)

            st.success("Prediction")
            emoji_icon = emotions_emoji_dict.get(prediction, "Unknown")
            st.write(f"{prediction}: {emoji_icon}")
            st.write(f"Confidence: {np.max(probability):.2f}")

        with col2:
            st.success("Prediction Probability")
            proba_df = pd.DataFrame(probability, columns=predictor.get_classes())

            # Clean up DataFrame
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["emotions", "probability"]

            # Plot using Seaborn
            fig, ax = plt.subplots()
            sns.barplot(x="emotions", y="probability", data=proba_df_clean, ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)


if __name__ == '__main__':
    main()

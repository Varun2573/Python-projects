import os
import gdown
import zipfile
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import ktrain
from ktrain import text


# ---------------------- MODEL SETUP ------------------------

FILE_ID = "1jk1QEsNH8nbhJnMbeV69arJ2J4_spNIu"
ZIP_URL = f"https://drive.google.com/uc?id={FILE_ID}"
ZIP_PATH = "Model.zip"
EXTRACT_DIR = "Model"
PREDICTOR_DIR = os.path.join(EXTRACT_DIR, "Model")  # Assuming zip contains a folder called Model


def download_and_extract_model():
    if not os.path.exists(PREDICTOR_DIR):
        with st.spinner("📦 Downloading and extracting model..."):
            # Download model.zip from Google Drive
            gdown.download(ZIP_URL, ZIP_PATH, quiet=False)

            # Unzip
            with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
                zip_ref.extractall(EXTRACT_DIR)

            # Remove zip file
            os.remove(ZIP_PATH)


@st.cache_resource
def load_predictor():
    download_and_extract_model()
    return ktrain.load_predictor(PREDICTOR_DIR)


predictor = load_predictor()

emotions_emoji_dict = {
    "anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗",
    "joy": "😂", "neutral": "😐", "sad": "😔", "sadness": "😔",
    "shame": "😳", "surprise": "😮"
}


# ---------------------- EMOTION FUNCTIONS ------------------------

def predict_emotions(docx):
    results = predictor.predict([docx])
    return results[0]


def get_prediction_proba(docx):
    results = predictor.predict_proba([docx])
    return results


# ---------------------- STREAMLIT APP UI ------------------------

def main():
    st.set_page_config(page_title="Text Emotion Detector", layout="wide")
    st.title("😃 Text Emotion Detection with BERT")
    st.subheader("Type a sentence and detect the underlying emotion")

    with st.form(key='my_form'):
        raw_text = st.text_area("💬 Enter Text Here", height=150)
        submit_text = st.form_submit_button(label='🚀 Submit')

    if submit_text and raw_text.strip():
        col1, col2 = st.columns(2)

        prediction = predict_emotions(raw_text)
        probability = get_prediction_proba(raw_text)

        with col1:
            st.success("✅ Original Text")
            st.write(raw_text)

            st.success("🎯 Prediction")
            emoji_icon = emotions_emoji_dict.get(prediction, "❓")
            st.write(f"**Emotion:** `{prediction}` {emoji_icon}")
            st.write(f"**Confidence:** `{np.max(probability):.2f}`")

        with col2:
            st.success("📊 Prediction Probability")
            proba_df = pd.DataFrame(probability, columns=predictor.get_classes())
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["emotions", "probability"]

            fig, ax = plt.subplots()
            sns.barplot(x="emotions", y="probability", data=proba_df_clean, ax=ax, palette="viridis")
            plt.xticks(rotation=45)
            st.pyplot(fig)

    elif submit_text:
        st.warning("⚠️ Please enter some text before submitting.")


if __name__ == '__main__':
    main()

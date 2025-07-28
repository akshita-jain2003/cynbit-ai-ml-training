import streamlit as st
import joblib
import numpy as np
import pandas as pd
import altair as alt

# -------------------------------
# Load saved model & objects
# -------------------------------
model = joblib.load("emotion_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Emoji dictionary
emoji_dict = {
    "anger": "😠",
    "fear": "😨",
    "joy": "😊",
    "love": "❤️",
    "sadness": "😢",
    "surprise": "😲"
}

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Emotion Detection App")
st.write("Enter text to detect emotion!")

# Input text box
text_input = st.text_area("Enter your text:")

# Detect emotion button
if st.button("Detect Emotion"):
    st.warning("Please enter text")
    # Validate input
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Preprocess
        processed_text = text_input.lower()

        # Vectorize
        vector = vectorizer.transform([processed_text])

        # Predict
        prediction = model.predict(vector)[0]
        emotion = label_encoder.inverse_transform([prediction])[0]

        # Show result
        st.success(
            f"Predicted Emotion: **{emotion}** {emoji_dict.get(emotion, '')}")

        # Show probabilities
        probs = model.predict_proba(vector)[0]

        # Create DataFrame for chart
        prob_df = pd.DataFrame({
            'Emotion': label_encoder.classes_,
            'Probability': probs
        })

        st.write("### Emotion Probabilities:")

        # Altair bar chart (better color & visibility)
        chart = (
            alt.Chart(prob_df)
            .mark_bar()
            .encode(
                x=alt.X('Emotion', sort=None),
                y='Probability',
                color=alt.Color('Emotion', scale=alt.Scale(scheme='tableau10'))
            )
            .properties(height=300)
        )

        st.altair_chart(chart, use_container_width=True)

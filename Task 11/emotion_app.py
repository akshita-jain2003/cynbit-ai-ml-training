import streamlit as st
import joblib
import numpy as np
import pandas as pd
import altair as alt
import os

# Load your saved model and vectorizer
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
# Sidebar
# -------------------------------
st.sidebar.title("Options")

# Description
st.sidebar.markdown("**This app predicts emotion from text input.**")

# Chart type selection
chart_type = st.sidebar.radio(
    "Select Probability Chart Type",
    ("Bar Chart", "Pie Chart")
)

# Toggle emoji display
show_emoji = st.sidebar.checkbox("Show Emoji", value=True)

# About section
if st.sidebar.button("About App"):
    st.sidebar.info(
        "Developed as part of training task. "
        "Uses scikit-learn model with TF-IDF and Label Encoding."
    )

# -------------------------------
# Main UI
# -------------------------------
st.title("Emotion Detection App")
st.write("Enter text to detect emotion!")

# Input text box
text_input = st.text_area("Enter your text:")

# Detect emotion button
if st.button("Detect Emotion"):
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

        # Display result
        if show_emoji:
            st.success(f"Predicted Emotion: **{emotion}** {emoji_dict.get(emotion, '')}")
        else:
            st.success(f"Predicted Emotion: **{emotion}**")

        # Show probabilities
        probs = model.predict_proba(vector)[0]
        prob_df = pd.DataFrame({
            'Emotion': label_encoder.classes_,
            'Probability': probs
        })

        st.write("### Emotion Probabilities:")

        # Chart options
        if chart_type == "Bar Chart":
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
        else:
            # Pie chart (simple Altair workaround: treat as bar chart but round edges)
            pie_chart = (
                alt.Chart(prob_df)
                .mark_arc()
                .encode(
                    theta='Probability',
                    color='Emotion',
                    tooltip=['Emotion', 'Probability']
                )
            )
            st.altair_chart(pie_chart, use_container_width=True)

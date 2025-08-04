import streamlit as st
import pickle
import os

# Load model and vectorizer if available
if os.path.exists("model.pkl") and os.path.exists("vectorizer.pkl"):
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
else:
    st.error("Model or vectorizer file not found! Please train and save them first.")
    st.stop()


# Streamlit App
st.title("Fake News Detector 📰")
st.write("Enter news title and content to predict if it's fake or real.")

title = st.text_input("News Title:")
text = st.text_area("News Content:")

if st.button("Predict"):
    combined_text = (title + " " + text).lower()
    transformed_text = vectorizer.transform([combined_text])
    prediction = model.predict(transformed_text)[0]

    if prediction == 1:
        st.success("This news seems **REAL** ✅")
    else:
        st.error("This news seems **FAKE** ❌")

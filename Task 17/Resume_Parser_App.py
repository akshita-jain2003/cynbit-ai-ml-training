import streamlit as st
import os
import docx2txt
import fitz  # PyMuPDF
import re
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Resume Parser", layout="wide")

st.title("📄 Resume Parser App")
st.write("Upload resumes in PDF or DOCX format to extract candidate details.")

uploaded_files = st.file_uploader("Upload Resumes", accept_multiple_files=True, type=['pdf', 'docx'])

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else ""

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        if len(line.strip().split()) >= 2 and len(line.strip()) < 40:
            return line.strip()
    return "Name Not Found"

def extract_skills(text):
    common_skills = ['python', 'java', 'sql', 'machine learning', 'html', 'css', 'c++', 'deep learning', 'nlp']
    found_skills = []
    text = text.lower()
    for skill in common_skills:
        if skill in text:
            found_skills.append(skill)
    return ", ".join(found_skills)

# Collect extracted data
parsed_data = []

if uploaded_files:
    for file in uploaded_files:
        if file.name.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        else:
            text = extract_text_from_docx(file)

        name = extract_name(text)
        email = extract_email(text)
        skills = extract_skills(text)

        parsed_data.append({
            "Name": name,
            "Email": email,
            "Skills": skills
        })

    df = pd.DataFrame(parsed_data)
    st.subheader("🧾 Extracted Resume Data")
    st.dataframe(df)

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download as CSV", csv, "parsed_resumes.csv", "text/csv")

    # WordCloud
    st.subheader("☁️ Top Skills WordCloud")
    all_skills = ', '.join(df['Skills'].str.replace(' ', '_'))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_skills)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    st.sidebar.header("🔍 Filter Options")
    selected_skill = st.sidebar.selectbox("Filter by Skill", options=["All"] + sorted(set(', '.join(df['Skills']).split(', '))))

    if selected_skill != "All":
     filtered_df = df[df['Skills'].str.contains(selected_skill, case=False)]
     st.dataframe(filtered_df)
    else:
     st.dataframe(df)  
else:
    st.info("Please upload one or more resumes to begin.")


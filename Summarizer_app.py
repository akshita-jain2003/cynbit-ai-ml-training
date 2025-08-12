import streamlit as st
import fitz
import docx

@st.cache_resource
def get_summarizer():
    from transformers import pipeline
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

@st.cache_data
def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page_num in range(len(pdf_document)):
            text += pdf_document.load_page(page_num).get_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    return text

def split_text(text, max_tokens=500):
    sentences = text.split('. ')
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk.split()) + len(sentence.split()) <= max_tokens:
            chunk += sentence + ". "
        else:
            chunks.append(chunk)
            chunk = sentence + ". "
    chunks.append(chunk)
    return chunks

st.title("📄 Text Summarizer Tool")
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

if uploaded_file is not None and st.button("Summarize"):
    text = extract_text_from_file(uploaded_file)
    if text.strip():
        chunks = split_text(text) if len(text.split()) > 500 else [text]
        summarizer = get_summarizer()
        summary_text = ""
        for chunk in chunks:
            result = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
            summary_text += result[0]['summary_text'] + " "
        st.subheader("Summary:")
        st.write(summary_text.strip())

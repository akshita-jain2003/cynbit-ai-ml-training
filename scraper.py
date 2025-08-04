import os
import streamlit as st
import pandas as pd
from pathlib import Path

# 1. Page configuration
st.set_page_config(
    page_title="Quotes Scraper 🧠",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Embed custom CSS to style emojis and sidebar
st.markdown("""
    <style>
    /* Add spacing for emojis in sidebar menu items */
    .css-8hkptd { margin-right: 8px; }

    /* Sidebar heading style */
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar content with emojis
st.sidebar.header("🔍 Filters")
author_filter = st.sidebar.text_input("Author name")
tag_filter = st.sidebar.text_input("Tag keyword")

st.sidebar.markdown("### ℹ️ Summary")
base = Path(__file__).parent.resolve()
csv_path = base / "quotes.csv"

if not csv_path.exists():
    st.error(f"⚠️ File not found at: {csv_path}")
    st.stop()
df = pd.read_csv(csv_path)
st.sidebar.write(f"- Total quotes: **{len(df)}**")
st.sidebar.write(f"- Unique authors: **{df['Author'].nunique()}**")

# 4. Filter & display
filtered = df.copy()
if author_filter:
    filtered = filtered[filtered['Author'].str.contains(author_filter, case=False)]
if tag_filter:
    filtered = filtered[filtered['Tags'].str.contains(tag_filter, case=False)]

st.title("📚 Quotes Browser")
st.write(f"Showing **{len(filtered)}** of **{len(df)}** quotes")
st.dataframe(filtered, use_container_width=True)

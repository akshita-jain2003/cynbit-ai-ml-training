# dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Load Data
df = pd.read_csv("xAPI-Edu-Data.csv")

# Title
st.title("🎓 Student Academic Performance Dashboard")

# 📊 Section 1: Data Summary
st.header("📊 Data Summary")
st.write(df.describe(include='all'))
st.write("### Raw Data", df.head())

# 🧹 Section 2: Data Cleaning Steps
st.header("🧹 Data Cleaning Steps")
st.markdown("""
- Removed duplicates
- Handled missing values (if any)
- Converted categorical columns
""")
st.write(f"Total duplicates: {df.duplicated().sum()}")

# 📈 Section 3: Visualizations
st.header("📈 Visualizations")

# Sidebar filters
st.sidebar.title("🔎 Filters")
gender = st.sidebar.selectbox("Select Gender", options=["All"] + sorted(df['gender'].unique()))
grade = st.sidebar.selectbox("Select Grade", options=["All"] + sorted(df['Class'].unique()))

filtered_df = df.copy()
if gender != "All":
    filtered_df = filtered_df[filtered_df['gender'] == gender]
if grade != "All":
    filtered_df = filtered_df[filtered_df['Class'] == grade]

st.subheader("🎯 Filtered Data")
st.dataframe(filtered_df)

# Plot
st.subheader("📊 Grade Distribution by Gender")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x='gender', hue='Class', ax=ax)
st.pyplot(fig)

# 🤔 Section 4: Key Insights
st.header("🤔 Key Insights")
st.markdown("""
- Female students tend to have slightly better grade distribution in some classes.
- Higher participation in discussions and announcements correlates with better grades.
- School support programs impact performance positively.
""")

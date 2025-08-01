import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import altair as alt

# 1. Load Dataset
df = pd.read_csv("students_cleaned.csv")

# Clean columns
df['Skills'] = df['Skills'].str.lower()
df['Interest'] = df['Interest'].str.lower()

# 2. Build TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Skills'])

# 3. Recommendation Function
def recommend_tfidf_cosine(user_skills, df, vectorizer, tfidf_matrix, top_n=3, domain=None):
    user_vector = vectorizer.transform([user_skills.lower()])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    df_copy = df.copy()
    df_copy['Score'] = similarities * 100

    if domain:
        df_copy = df_copy[df_copy['Interest'] == domain.lower()]

    return df_copy.sort_values('Score', ascending=False).head(top_n)


# 4. Streamlit UI
# ----------------------------
# --- Page Config ---
st.set_page_config(page_title="Student Collaboration Matcher", page_icon="🤝", layout="wide")

# --- Sidebar for Inputs ---
st.sidebar.header("🔧 Your Profile")
st.sidebar.write("Select your skills and domain to find best matches")

# Dynamic skill selection
all_skills = sorted({skill.strip() for skills in df['Skills'] for skill in skills.split(",")})
selected_skills = st.sidebar.multiselect("Select your skills:", options=all_skills)

# Dynamic domain selection
domains = ["None"] + sorted(df['Interest'].unique())
domain_filter = st.sidebar.selectbox("Select project domain (optional):", domains)

if domain_filter == "None":
    domain_filter = None

# Main Title
st.title("🤝 Student Collaboration Matcher")
st.markdown("Find the **best students** to collaborate with based on your skills and interests!")

# Button
if st.sidebar.button("🔍 Find Matches"):
    if not selected_skills:
        st.warning("⚠️ Please select at least one skill.")
    else:
        user_skills = ", ".join(selected_skills)
        tfidf_rec = recommend_tfidf_cosine(user_skills, df, vectorizer, tfidf_matrix, domain=domain_filter)

        if tfidf_rec.empty:
            st.warning("❌ No matches found for selected skills and domain.")
        else:
            st.subheader("🎯 Top Recommendations")

            # Show table
            st.dataframe(tfidf_rec[['Name', 'Skills', 'Interest', 'Score']])

            # Prepare data for chart
            chart_data = tfidf_rec[['Name', 'Score']]

            # Create colorful bar chart
            bar_chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Name:N', sort='-y', title='Student Name'),
            y=alt.Y('Score:Q', title='Match Score (%)'),
            color=alt.Color('Score:Q', scale=alt.Scale(scheme='turbo')),  # colorful scheme
            tooltip=['Name', 'Score']
            ).properties(
            width=600,
            height=400
            )

            st.altair_chart(bar_chart, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Collaboration Matcher 2025")

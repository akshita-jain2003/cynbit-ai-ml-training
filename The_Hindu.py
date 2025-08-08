import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
import plotly.express as px
import streamlit as st

# --------- SCRAPING FUNCTION ---------
def scrape_thehindu_headlines():
    url = "https://www.thehindu.com/news/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = []

    # First check <a class="title">
    for headline in soup.find_all('a', class_='title'):
        text = headline.get_text(strip=True)
        if text:
            headlines.append(text)

    # Fallback: <h3> tags
    if not headlines:
        for headline in soup.find_all('h3'):
            text = headline.get_text(strip=True)
            if text:
                headlines.append(text)

    return pd.DataFrame({'Headline': headlines})

# --------- SENTIMENT ANALYSIS ---------
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive 😊"
    elif polarity < 0:
        return "Negative 😡"
    else:
        return "Neutral 😐"

# --------- STREAMLIT APP ---------
st.title("📰 News Headlines Sentiment Analyzer")

# Sidebar
st.sidebar.title("⚙️ Controls")

sentiment_filter = st.sidebar.multiselect(
    "Filter by Sentiment",
    ["Positive 😊", "Negative 😡", "Neutral 😐"],
    default=["Positive 😊", "Negative 😡", "Neutral 😐"]
)

if st.sidebar.button("🔄 Refresh Headlines"):
    st.experimental_rerun()

st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ using Streamlit + Plotly + TextBlob")

# Scrape Headlines
df = scrape_thehindu_headlines()

# Perform Sentiment Analysis
df['Sentiment'] = df['Headline'].apply(analyze_sentiment)

# Apply Filter
filtered_df = df[df['Sentiment'].isin(sentiment_filter)]

# Show Data
st.subheader("📝 Headlines")
if filtered_df.empty:
    st.warning("⚠️ No headlines available for the selected sentiment(s).")
else:
    st.write(filtered_df)

# Colorful Pie Chart
fig_pie = px.pie(
    filtered_df,
    names='Sentiment',
    title='🎯 Sentiment Distribution',
    color='Sentiment',
    color_discrete_map={
        'Positive 😊': '#28a745',
        'Negative 😡': '#dc3545',
        'Neutral 😐':  '#ffc107'
    }
)
st.plotly_chart(fig_pie)

# Prepare data for Bar Chart
sentiment_counts = filtered_df['Sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']

# Colorful Bar Chart
fig_bar = px.bar(
    sentiment_counts,
    x='Sentiment', y='Count',
    title='📊 Sentiment Count',
    text='Count',
    color='Sentiment',
    color_discrete_map={
        'Positive 😊': '#28a745',
        'Negative 😡': '#dc3545',
        'Neutral 😐':  '#ffc107'
    }
)
fig_bar.update_traces(textposition='outside')
st.plotly_chart(fig_bar)

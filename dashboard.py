from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from utils.utils import get_gnews_articles


st.set_page_config(page_title="News Dashboard", layout="wide")
st.title("📰 News Article Summaries")


try:
    articles = get_gnews_articles()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Display each article in its own box
for idx, article in enumerate(articles):
    with st.container():
        st.markdown("---")  # horizontal line between articles

        col1, col2 = st.columns([1, 3])

        # Show image if available
        with col1:
            if article.get("image"):
                st.image(article["image"])

        # Show text content
        with col2:
            st.markdown(f"### {article.get('title', 'No Title')}")
            st.markdown(f"**Source:** [{article['source']['name']}]({article['source']['url']}) • 🗓️ {article['publishedAt'].split('T')[0]}")
            
            with st.expander("📌 Description", expanded=False):
                st.write(article.get("description", "No description available."))

            with st.expander("📚 Summary", expanded=False):
                st.write(article.get("summary", "No summary available."))

            # Link to full article
            st.markdown(f"[🔗 Read Full Article]({article['url']})", unsafe_allow_html=True)

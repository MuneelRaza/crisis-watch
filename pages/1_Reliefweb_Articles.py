import streamlit as st
from dotenv import load_dotenv
from utils.utils import get_reliefweb_articles
load_dotenv()

st.set_page_config(page_title="ReliefWeb Dashboard", layout="wide")
st.title("🌍 ReliefWeb Article Summaries")

try:
    articles = get_reliefweb_articles()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Display each article
for idx, article in enumerate(articles):
    with st.container():
        st.markdown("---")

        st.markdown(f"### {article.get('title', 'No Title')}")
        st.markdown(f"**Source:** {article.get('source')} • 🗓️ {article.get('date').split('T')[0]}")
        
        st.markdown(f"**Countries:** {', '.join(article.get('countries', []))}")
        
        with st.expander("📚 Summary", expanded=True):
            st.write(article.get("summary", "No summary available."))

        # Show full body if present
        if article.get("body"):
            with st.expander("📰 Full Body", expanded=False):
                st.write(article["body"])

        st.markdown(f"[🔗 Read Full Article]({article['resolved_url']})", unsafe_allow_html=True)

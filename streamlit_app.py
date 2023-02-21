import streamlit as st
import feedparser
import pandas as pd

st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")
st.title("The Ciber House")

# RSS feeds to read
rss_feeds = [
    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed",
    "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed",
    "https://feeds.feedburner.com/hispasec/zCAd"
]

# Read RSS feeds and save articles in a list of dictionaries
articles = []
for rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries:
        article = {}
        article['feed'] = feed.feed.title
        article['title'] = entry.title
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)

# Convert list of dictionaries to Pandas DataFrame
df = pd.DataFrame(articles)

# Convert "date" column to datetime
if 'date' in df:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Sort DataFrame by date
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# Show top 5 most recent articles for each feed
for feed in df['feed'].unique():
    st.write(f"### {feed}")
    feed_df = df[df['feed'] == feed].head(5)
    feed_df = feed_df.drop(['feed'], axis=1)
    st.dataframe(feed_df.style.hide_index().set_properties(**{'text-align': 'left'}))

st.footer("By Sebastian Vargas")

# Second table with ZDI RSS
st.title("ZDI RSS")
zdi_feed = "https://www.zerodayinitiative.com/rss/rss.xml"
zdi = feedparser.parse(zdi_feed)
zdi_articles = []
for entry in zdi.entries:
    zdi_article = {}
    zdi_article['title'] = entry.title
    zdi_article['date'] = entry.get('published', '')
    zdi_article['summary'] = entry.get('summary', '')
    zdi_article['url'] = entry.link
    zdi_articles.append(zdi_article)
zdi_df = pd.DataFrame(zdi_articles)
if 'date' in zdi_df:
    zdi_df['date'] = pd.to_datetime(zdi_df['date'], errors='coerce')
zdi_df = zdi_df.sort_values('date', ascending=False).reset_index(drop=True)

# Show 10 most recent articles from ZDI
st.write("### Latest articles from ZDI")
page_number = st.number_input('Page Number', min_value=1, max_value=zdi_df.shape[0]//10+1, value=1)
start_idx = (page_number - 1) * 10
end_idx = start_idx + 10
zdi_page_df = zdi_df[start_idx:end_idx]
zdi_page_df = zdi_page_df.drop(['date'], axis=1)
st.dataframe(zdi_page_df.style.hide_index().set_properties(**{'text-align': 'left'}))

# Add search functionality
search_query = st.text_input("Search articles", "")
if search_query:
    search_results = zdi_df[zdi_df['title'].str.contains(search_query, case=False)]
    search_results = search_results.drop(['date'], axis=1)
    st




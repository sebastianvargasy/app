
import streamlit as st
import feedparser
import pandas as pd

st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")
st.title("The Ciber House")

# Leer feeds RSS
rss_feeds = [    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed",    "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed",    "https://feeds.feedburner.com/hispasec/zCAd"]

articles = []
for rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries[:5]:  # Leer las 5 entradas más recientes
        article = {}
        article['feed'] = feed.feed.title
        article['title'] = entry.title
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)

df = pd.DataFrame(articles)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# Mostrar la tabla de noticias
st.write("Noticias RSS más recientes")
st.dataframe(df.style.hide_columns(['authors'])) 

# Leer feed del Zero Day Initiative
zdi_feed = "https://www.zerodayinitiative.com/rss/zdi-all.xml"

zdi_articles = []
zdi_feed = feedparser.parse(zdi_feed)
for entry in zdi_feed.entries[:10]:  # Leer las 10 entradas más recientes
    zdi_article = {}
    zdi_article['title'] = entry.title
    zdi_article['date'] = entry.get('published', '')
    zdi_article['summary'] = entry.get('summary', '')
    zdi_article['url'] = entry.link
    zdi_articles.append(zdi_article)

zdi_df = pd.DataFrame(zdi_articles)
zdi_df['date'] = pd.to_datetime(zdi_df['date'], errors='coerce')
zdi_df = zdi_df.sort_values('date', ascending=False).reset_index(drop=True)

# Mostrar la tabla de noticias del Zero Day Initiative con paginación
st.write("Noticias Zero Day Initiative más recientes")
page_size = 10
page = st.sidebar.slider("Página", 1, int(len(zdi_df) / page_size) + 1)
start = (page - 1) * page_size
end = start + page_size
st.dataframe(zdi_df.iloc[start:end].style.hide_index())
st.sidebar.write("By Sebastian Vargas") 

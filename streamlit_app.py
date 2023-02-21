import streamlit as st
import feedparser
from datetime import datetime

st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed"
]

# Leemos los feeds y guardamos los artículos en una lista de diccionarios
articles = []
for rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries:
        article = {}
        article['feed'] = feed.feed.title
        article['title'] = entry.title
        article['authors'] = entry.get('author', '')
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)

# Ordenamos la lista de artículos por fecha
articles = sorted(articles, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

# Configuramos la tabla con masonry
columns = st.beta_columns(3)
for article in articles:
    col = columns.pop(0)
    with col:
        st.write(f"## {article['feed']}")
        st.write(f"### [{article['title']}]({article['url']})")
        st.write(f"Autor(es): {article['authors']}")
        st.write(f"Fecha: {article['date']}")
        st.write(article['summary'])


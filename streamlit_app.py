import streamlit as st
import feedparser

st.set_page_config(page_title="Últimas noticias de RSS", page_icon=":newspaper:", layout="wide")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed",
    "https://elpais.com/sitemap.xml",
    "https://www.bbc.com/news/sitemap.xml"
]

# Leemos los feeds y guardamos las últimas 5 noticias de cada uno en una lista
articles = []
for rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries[:5]:
        article = {}
        article['feed'] = feed.feed.title
        article['title'] = entry.title
        article['authors'] = entry.get('author', '')
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)

# Mostramos las últimas 5 noticias de cada feed
for feed in set([a['feed'] for a in articles]):
    st.write(f"## {feed}")
    for article in [a for a in articles if a['feed'] == feed]:
        st.write(f"### {article['title']}")
        st.write(f"Autor(es): {article['authors']}")
        st.write(f"Fecha: {article['date']}")
        st.write(article['summary'])
        st.write(f"Leer más: [{article['url']}]({article['url']})")
    st.write("")


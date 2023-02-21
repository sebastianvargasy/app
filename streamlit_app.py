import streamlit as st
import feedparser
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed"]

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

# Convertimos la lista de diccionarios a un DataFrame de Pandas y ordenamos por fecha
df = pd.DataFrame(articles)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# Mostramos la tabla de noticias en Pandas
st.write(df)

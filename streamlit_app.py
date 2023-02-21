import streamlit as st
import feedparser
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.nytimes.com/sitemap.xml",
    "https://elpais.com/sitemap.xml",
    "https://www.bbc.com/news/sitemap.xml"
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

# Convertimos la lista de diccionarios a un DataFrame de Pandas
df = pd.DataFrame(articles)

# Verificamos si la columna "date" está presente en el DataFrame y, si es así, la convertimos a una columna de fecha
if 'date' in df:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Ordenamos el DataFrame por fecha
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# Mostramos la tabla de noticias en Pandas
st.write(df)


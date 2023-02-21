import streamlit as st
import feedparser
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>The Ciber House</h1>", unsafe_allow_html=True)
st.write(" ")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed",
    "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed",
    "https://feeds.feedburner.com/hispasec/zCAd"
]

# Leemos los feeds y guardamos los artículos en una lista de diccionarios
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

# Convertimos la lista de diccionarios a un DataFrame de Pandas
df = pd.DataFrame(articles)

# Convertimos la columna "date" a una columna de fecha
if 'date' in df:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Ordenamos el DataFrame por fecha
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# Limitamos el número de noticias a las últimas 30
df = df.head(30)

# Creamos un diccionario de DataFrames para cada fuente RSS
dfs = {}
for rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    articles = []
    for entry in feed.entries:
        article = {}
        article['feed'] = feed.feed.title
        article['title'] = entry.title
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)
    df = pd.DataFrame(articles)
    dfs[feed.feed.title] = df

# Mostramos las noticias de cada fuente RSS en pestañas separadas
for feed_title, df in dfs.items():
    st.write(f"## {feed_title}")
    st.write(df.head(10))
    st.write("")



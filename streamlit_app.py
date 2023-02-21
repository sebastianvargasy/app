import streamlit as st
import feedparser
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Encabezado de la página
st.header("The Ciber House")
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
    for entry in feed.entries[:10]:  # Tomamos sólo las 10 noticias más recientes
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

# Limitamos a las últimas 30 noticias
df = df[:30]

# Agrupamos los artículos por feed
dfs = {}
for feed in df.feed.unique():
    dfs[feed] = df[df.feed == feed]

# Creamos una pestaña por feed
for feed, df in dfs.items():
    st.write(f"## {feed}")
    st.write(df.to_html(escape=False), unsafe_allow_html=True)



import streamlit as st
import feedparser
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Encabezado de la página
st.write("<h1 style='text-align: center;'>The Ciber House</h1>", unsafe_allow_html=True)
st.write(" ")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed",
    "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed",
    "https://feeds.feedburner.com/hispasec/zCAd"
]

dfs = {}
for rss_feed in rss_feeds:
    # Leemos los feeds y guardamos los artículos en una lista de diccionarios
    articles = []
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries:
        article = {}
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

    # Limitamos a 10 noticias
    df = df[:10]

    # Guardamos el DataFrame en un diccionario con el título del feed como clave
    dfs[feed.feed.title] = df

# Creamos pestañas para cada feed
tabs = st.tabs(list(dfs.keys()))
for tab in tabs:
    st.write(dfs[tab])

# Pie de página
st.write(" ")
st.write("<p style='text-align: center;'>By Sebastian Vargas</p>", unsafe_allow_html=True)




import streamlit as st
import feedparser
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>The Ciber House</h1>", unsafe_allow_html=True)
st.write(" ")

# Creamos una lista de tuplas con los RSS que queremos leer y su nombre para la pestaña correspondiente
rss_feeds = [    ("CCN-CERT", "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed"),    ("Vulnerabilidades", "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed"),    ("Hispasec", "https://feeds.feedburner.com/hispasec/zCAd")]

# Leemos los feeds y guardamos los artículos en un diccionario donde la clave es el nombre del feed
dfs = {}
for rss_name, rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    articles = []
    for entry in feed.entries[:10]:  # Tomamos sólo las 10 noticias más recientes de cada feed
        article = {}
        article['title'] = entry.title
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)
    df = pd.DataFrame(articles)
    if 'date' in df:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values('date', ascending=False).reset_index(drop=True)
    dfs[rss_name] = df

# Creamos las pestañas y mostramos las tablas correspondientes
tabs = st.tabs(list(dfs.keys()))
for i, rss_name in enumerate(dfs.keys()):
    with tabs[i]:
        st.write(rss_name)
        st.write(dfs[rss_name])




import streamlit as st
import feedparser
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>Noticias RSS</h1>", unsafe_allow_html=True)
st.write(" ")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.cshub.com/rss/categories/attacks",
    "https://www.zerodayinitiative.com/rss/published",
    "https://feeds.feedburner.com/hispasec/zCAd"
]

# Leemos los feeds y guardamos los artículos en un diccionario de DataFrames de Pandas
dfs = {}
for rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    articles = []
    for entry in feed.entries[:10]:  # Tomamos sólo las 10 noticias más recientes de cada feed
        article = {}
        article['feed'] = feed.feed.title
        article['title'] = entry.title
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)
    df = pd.DataFrame(articles)
    if 'date' in df:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])  # Eliminamos las filas con fechas nulas
        df = df.sort_values('date', ascending=False).reset_index(drop=True)
        dfs[feed.feed.title] = df

# Mostramos las noticias en pestañas separadas para cada feed
if dfs:
    feed_names = list(dfs.keys())
    feed_index = st.sidebar.selectbox("Selecciona un feed:", feed_names)
    st.write(f"### Noticias de {feed_index}")
    st.write(dfs[feed_index])
else:
    st.write("No se pudieron leer los feeds de noticias.")    

# Pie de página
st.write(" ")
st.markdown("<p style='text-align: center;'>Hecho con Streamlit</p>", unsafe_allow_html=True)


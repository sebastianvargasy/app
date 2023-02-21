import streamlit as st
import feedparser
import pandas as pd
import html

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Función para crear enlaces clickeables
def make_clickable(url):
    if pd.isna(url):
        return ""
    url = html.escape(url)
    return f'<a href="{url}" target="_blank">{url}</a>'

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
        article['authors'] = entry.get('author', '')
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

# Agregamos una columna con enlaces clickeables
df['url_html'] = df['url'].fillna('').astype(str).apply(make_clickable, axis=1)
df = df[['feed', 'title', 'authors', 'date', 'summary', 'url_html']]

# Encabezado de la página
st.markdown("<h1 style='text-align: center; color: black;'>The Cyber House</h1>", unsafe_allow_html=True)

# Tabla de noticias en Pandas
st.write(df, unsafe_allow_html=True)

# Pie de página
st.markdown("<p style='text-align: center; color: black;'>By Sebastian Vargas</p>", unsafe_allow_html=True)

import streamlit as st
import feedparser
from datetime import datetime
import pandas as pd
import html

# Configuramos la página con un encabezado y un pie de página personalizados
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide", initial_sidebar_state="collapsed")

# Creamos un encabezado personalizado
header_container = st.beta_container()
with header_container:
    st.title("The Ciber House")

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
def make_clickable(url):
    url = html.escape(url)
    url = url.replace("&amp;", "&")
    return f'<a href="{url}" target="_blank">{url}</a>'

df['url'] = df['url'].astype(str)
df['url_html'] = df['url'].apply(make_clickable, axis=1)
df = df[['feed', 'title', 'authors', 'date', 'url_html']]

# Mostramos la tabla de noticias en Pandas
st.write(df, unsafe_allow_html=True)

# Creamos un pie de página personalizado
footer_container = st.beta_container()
with footer_container:
    col1, col2 = st.beta_columns([1, 3])
    col1.write("")
    col2.write("By Sebastian Vargas")

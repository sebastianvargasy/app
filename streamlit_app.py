import streamlit as st
import feedparser
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Encabezado de la página
st.beta_container()
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
    for entry in feed.entries[:5]:  # Tomamos sólo las 5 noticias más recientes
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

# Eliminamos la columna "authors"
df = df.drop(['authors'], axis=1)

# Mostramos la tabla de noticias en Pandas
st.write("Noticias de ciberseguridad", df)

# Creamos una segunda tabla con el feed de Zero Day Initiative
rss_feed_zdi = "https://www.zerodayinitiative.com/rss/published/"
feed_zdi = feedparser.parse(rss_feed_zdi)

# Leemos los artículos del feed y guardamos en una lista de diccionarios
articles_zdi = []
for entry in feed_zdi.entries:
    article = {}
    article['title'] = entry.title
    article['date'] = entry.get('published', '')
    article['summary'] = entry.get('summary', '')
    article['url'] = entry.link
    articles_zdi.append(article)

# Convertimos la lista de diccionarios a un DataFrame de Pandas
df_zdi = pd.DataFrame(articles_zdi)

# Convertimos la columna "date" a una columna de fecha
if 'date' in df_zdi:
    df_zdi['date'] = pd.to_datetime(df_zdi['date'], errors='coerce')

# Ordenamos el DataFrame por fecha
df_zdi = df_zdi.sort_values('date', ascending=False).reset_index(drop=True)

# Creamos una barra de búsqueda
search_term = st.text_input("Buscar en las noticias de Zero Day Initiative:", "")

# Filtramos la tabla según el término de búsqueda
if search_term:
    df_zdi = df_zdi[df_zdi['title'].str.contains(search_term, case=False)]

# Mostramos la tabla de noticias de Zero Day Initiative en Pandas
st.write



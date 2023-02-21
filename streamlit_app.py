import streamlit as st
import feedparser
import pandas as pd

st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed",    "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed",    "https://feeds.feedburner.com/hispasec/zCAd"]

# Leemos los feeds y guardamos los artículos en una lista de diccionarios
articles = []
for rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries[:5]:
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

# Ocultamos la columna 'authors'
if 'authors' in df:
    df = df.drop(['authors'], axis=1)

# Agregamos el header y footer
st.header('The Cyber House')
st.dataframe(df, height=500)

st.markdown("---")
st.write('By Sebastian Vargas')

# Agregamos una segunda tabla con los feeds de Zero Day Initiative
st.markdown("---")
st.header('Zero Day Initiative RSS Feed')
rss_feed = "https://www.zerodayinitiative.com/rss/published/"
feed = feedparser.parse(rss_feed)

articles = []
for entry in feed.entries[:10]:
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

# Agregamos la funcionalidad de búsqueda
search_query = st.sidebar.text_input('Buscar noticias', '')
if search_query:
    df = df[df['title'].str.contains(search_query, case=False)]

# Paginación
total_articles = len(df.index)
articles_per_page = 10
total_pages = total_articles // articles_per_page + (1 if total_articles % articles_per_page > 0 else 0)
current_page = st.sidebar.slider('Página', 1, total_pages, 1)
start_idx = (current_page - 1) * articles_per_page
end_idx = start_idx + articles_per_page
paginated_df = df.iloc[start_idx:end_idx]

st.dataframe(paginated_df, height=500)



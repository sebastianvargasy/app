import streamlit as st
import feedparser
from newspaper import Article

st.set_page_config(page_title="Buscador de RSS", page_icon=":mag:", layout="wide")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.nytimes.com/sitemap.xml",
    "https://elpais.com/sitemap.xml",
    "https://www.bbc.com/news/sitemap.xml"
]

# Leemos los feeds y guardamos los artículos en una lista
articles = []
for rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries:
        article = Article(entry.link)
        article.download()
        article.parse()
        articles.append(article)

# Creamos la barra de búsqueda
search_query = st.text_input("Busca una noticia")

# Filtramos los artículos según la búsqueda
filtered_articles = []
for article in articles:
    if search_query.lower() in article.title.lower():
        filtered_articles.append(article)

# Mostramos los artículos filtrados
for article in filtered_articles:
    st.write(f"## {article.title}")
    st.write(f"### {article.authors}")
    st.write(f"Fecha: {article.publish_date}")
    st.write(article.summary)
    st.write(f"Leer más: [{article.source_url}]({article.url})")

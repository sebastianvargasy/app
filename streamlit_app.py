import streamlit as st
import feedparser
import pandas as pd
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(page_title="El pasquin de Ciberseguridad", page_icon="📰", layout="wide")

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>El pasquin de Ciberseguridad</h1>", unsafe_allow_html=True)
st.write(" ")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.cisa.gov/uscert/ncas/current-activity.xml/",
    "https://www.google.com/alerts/feeds/04729041965786430663/10669661265694116875",
    "https://feeds.feedburner.com/NoticiasSeguridadInformatica",
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
    df_feed = dfs[feed_index]
    for i, row in df_feed.iterrows():
        st.write(f"<h2>{row['title']}</h2>", unsafe_allow_html=True)
        st.write(f"<i>{row['date'].strftime('%d-%m-%Y')}</i>", unsafe_allow_html=True)
        st.write(f"<p>{row['summary']}</p>", unsafe_allow_html=True)
        components.html(f"<a href='{row['url']}' target='_blank'>Leer más</a>", height=50)
        st.write("<hr>", unsafe_allow_html=True)
else:
    st.write("No se pudieron leer los feeds de noticias.")    

# Pie de página
st.write(" ")
st.markdown("<p style='text-align: center;'>Hecho con ❤️ por Sebastian Vargas</p>", unsafe_allow_html=True)


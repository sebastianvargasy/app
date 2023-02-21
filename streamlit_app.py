import streamlit as st
import feedparser
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>Noticias RSS</h1>", unsafe_allow_html=True)
st.write(" ")

# Creamos una lista con los feeds que queremos leer
rss_feeds = {
    "CCN-CERT Noticias": "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed",
    "CCN-CERT Vulnerabilidades": "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed",
    "Hispasec": "https://feeds.feedburner.com/hispasec/zCAd"
}

dfs = {}
for title, url in rss_feeds.items():
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:10]:  # Tomamos sólo las 10 noticias más recientes
        article = {}
        article['feed'] = title
        article['title'] = entry.title
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)

    df = pd.DataFrame(articles)
    if 'date' in df:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values('date', ascending=False).reset_index(drop=True)

    dfs[title] = df

# Creamos las pestañas
tabs = st.sidebar.multiselect(
    "Seleccione los RSS a mostrar",
    list(rss_feeds.keys()),
    default=list(rss_feeds.keys())
)

# Mostramos los RSS seleccionados
for tab in tabs:
    st.write(f"## {tab}")
    df = dfs[tab]
    st.write(df[['title', 'date', 'summary']].to_html(escape=False, index=False), unsafe_allow_html=True)

# Pie de página
st.write(" ")
st.markdown("<p style='text-align: center;'>Hecho con ❤️ por Sebastian Vargas</p>", unsafe_allow_html=True)




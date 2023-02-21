
import streamlit as st
import feedparser

# Configuración de página
st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>The Ciber House</h1>", unsafe_allow_html=True)
st.write(" ")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    ("Noticias", "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed"),
    ("Vulnerabilidades", "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed"),
    ("Hispasec", "https://feeds.feedburner.com/hispasec/zCAd")
]

dfs = {}

# Leemos los feeds y guardamos los artículos en un diccionario de DataFrames de Pandas
for title, rss_feed in rss_feeds:
    feed = feedparser.parse(rss_feed)
    articles = []
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

    dfs[title] = df

# Creamos una pestaña para cada feed
for title, df in dfs.items():
    st.write(f"# {title}")
    for _, row in df.iterrows():
        st.write(f"<h2>{row.title}</h2>", unsafe_allow_html=True)
        st.write(f"<p><em>{row.date}</em></p>", unsafe_allow_html=True)
        st.write(f"<p>{row.summary}</p>", unsafe_allow_html=True)
        st.write(f"<a href='{row.url}'>Leer más</a>", unsafe_allow_html=True)
        st.write("<hr>", unsafe_allow_html=True)


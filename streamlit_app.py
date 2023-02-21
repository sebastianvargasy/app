import streamlit as st
import feedparser
import pandas as pd

st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")
st.title('The Ciber House')

# Leer los feeds y guardar los artículos en una lista de diccionarios
def read_feed(rss_feed):
    feed = feedparser.parse(rss_feed)
    articles = []
    for entry in feed.entries[:5]:
        article = {}
        article['feed'] = feed.feed.title
        article['title'] = entry.title
        article['date'] = entry.get('published', '')
        article['summary'] = entry.get('summary', '')
        article['url'] = entry.link
        articles.append(article)
    return pd.DataFrame(articles)

# Leer los feeds y guardar los artículos en un DataFrame de Pandas
rss_feeds = [
    "https://www.ccn-cert.cni.es/component/obrss/rss-noticias.feed",
    "https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed",
    "https://feeds.feedburner.com/hispasec/zCAd"
]

dfs = [read_feed(feed) for feed in rss_feeds]
df = pd.concat(dfs, ignore_index=True)

# Convertir la columna "date" a una columna de fecha
if 'date' in df:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Ordenar el DataFrame por fecha
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# Eliminar la columna de autores
if 'authors' in df:
    df = df.drop(['authors'], axis=1)

# Crear tabla con las noticias
st.write(df, unsafe_allow_html=True)

# Crear footer
st.text("By Sebastian Vargas")

# Crear segunda tabla
st.title("Zero Day Initiative")
rss_feed = "https://www.zerodayinitiative.com/rss/updated/"
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

# Convertir la columna "date" a una columna de fecha
if 'date' in df:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Ordenar el DataFrame por fecha
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# Crear un buscador para la tabla
search = st.text_input("Buscar en las noticias de Zero Day Initiative")

if search != "":
    df = df[df['title'].str.contains(search, case=False) | df['summary'].str.contains(search, case=False)]
    
# Paginación de la tabla
num_pages = len(df) // 10 + 1
page_number = st.number_input("Selecciona la página", min_value=1, max_value=num_pages, step=1)

start = (page_number-1) * 10
end = start + 10
st.table(df.iloc[start:end].style.set_properties(subset=['summary'], **{'width': '600px'}))

# Crear footer
st.text("By Sebastian Vargas")



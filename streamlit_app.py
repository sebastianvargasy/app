import streamlit as st
import feedparser
from datetime import datetime
import pandas as pd
from streamlit_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.set_page_config(page_title="Noticias RSS en HTML", page_icon="📰", layout="wide")

# Creamos una lista con los feeds que queremos leer
rss_feeds = [
    "https://www.nytimes.com/sitemap.xml",
    "https://elpais.com/sitemap.xml",
    "https://www.bbc.com/news/sitemap.xml"
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

# Convertimos la lista de diccionarios a un DataFrame de Pandas y ordenamos por fecha
df = pd.DataFrame(articles)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# Configuramos la tabla con masonry
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("feed", minWidth=120)
gb.configure_column("title", minWidth=300)
gb.configure_column("authors", minWidth=100)
gb.configure_column("date", minWidth=120, valueFormatter="(date) 'YYYY-MM-DD HH:mm:ss'")
gb.configure_column("summary", minWidth=300)
go = gb.build()
go.enable_masonry = True
go.pagination = False
go.rowModelType = 'clientSide'
go.rowSelection = 'single'
go.suppressRowClickSelection = True
go.autoSizeColumns = True

# Mostramos la tabla con masonry
AgGrid(df, gridOptions=go, height=600, width='100%', update_mode=GridUpdateMode.SELECTION_CHANGED, data_return_mode=DataReturnMode.AS_FILTERED_AND_SORTED)


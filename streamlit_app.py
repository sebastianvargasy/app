import streamlit as st
import requests
import schedule
import time

st.set_page_config(page_title="Web Monitor", page_icon=":computer:")

site_url = st.text_input("Ingrese la URL del sitio web a monitorear")

status_text = st.empty()

history = []

def check_site():
    try:
        response = requests.get(site_url)
        status_code = response.status_code
        if status_code == 200:
            status_text.success("El sitio está en línea.")
        else:
            status_text.warning("El sitio está en línea, pero ha devuelto un código de estado distinto de 200.")
    except requests.exceptions.ConnectionError:
        status_text.error("El sitio no está disponible.")
        status_code = None
    
    history.append({"timestamp": time.time(), "status": status_code})

schedule.every(5).seconds.do(check_site)

while True:
    schedule.run_pending()
    time.sleep(1)

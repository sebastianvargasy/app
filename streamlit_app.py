import streamlit as st
import numpy as np

st.title("Simulation[tm]")
st.write("Here is our super important simulation")

x = st.slider('Slope', min_value=0.01, max_value=0.10, step=0.01)
y = st.slider('Noise', min_value=0.01, max_value=0.10, step=0.01)

st.write(f"x={x} y={y}")

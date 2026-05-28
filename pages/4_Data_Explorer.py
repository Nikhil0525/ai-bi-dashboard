import streamlit as st
import pandas as pd

with open("styles/main.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📂 Data Explorer")

df = pd.read_csv("data/dataset.csv")

st.dataframe(df, use_container_width=True)

st.subheader("Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())

st.subheader("Column Types")

st.write(df.dtypes)
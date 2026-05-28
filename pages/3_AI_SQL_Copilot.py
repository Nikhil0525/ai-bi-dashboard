import streamlit as st
import pandas as pd
from ai.llm_service import generate_sql_from_question

with open("styles/main.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🧠 AI SQL Copilot")

df = pd.read_csv("data/dataset.csv")

question = st.text_input("Ask your data:", placeholder="show sales by region")

if question:
    sql = generate_sql_from_question(question)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    q = question.lower()

    if "region" in q:
        result = df.groupby("region")["sales_amount"].sum().reset_index()
    elif "product" in q:
        result = df.groupby("product")["sales_amount"].sum().reset_index()
    elif "category" in q:
        result = df.groupby("category")["sales_amount"].sum().reset_index()
    elif "total sales" in q or "revenue" in q:
        result = pd.DataFrame({"total_sales": [df["sales_amount"].sum()]})
    else:
        result = df.head(10)

    st.subheader("Result")
    st.dataframe(result, use_container_width=True)
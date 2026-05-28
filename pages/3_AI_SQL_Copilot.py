import streamlit as st
from ai.llm_service import generate_sql_from_question
from database.connection import run_query

with open("styles/main.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🧠 AI SQL Copilot")

question = st.text_input("Ask your data:", placeholder="show sales by region")

if question:
    sql = generate_sql_from_question(question)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    result = run_query(sql)

    st.subheader("Result")
    st.dataframe(result, use_container_width=True)
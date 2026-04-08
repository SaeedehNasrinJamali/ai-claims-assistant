import streamlit as st
import sqlite3

from parser import parse_question
from sql_builder import build_sql_advanced
from sql_executor import execute_sql
from explainer import explain_result
from database import load_data

# Load data into database
load_data()

# Database connection
conn = sqlite3.connect("claims.db")

# =========================
# App UI
# =========================
st.title("AI Claims Assistant")

st.info("Ask questions about claim totals, averages, and counts.")

st.markdown("### Example questions")
st.markdown("""
- What is the total claim amount in Ontario?
- What is the average claim amount for Auto policies?
- How many claims are there in Quebec?
- Show total claims by region
""")

question = st.text_input(
    "Enter your question:",
    placeholder="e.g. What is the total claim amount in Ontario?"
)

if st.button("Run Question"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        try:
            parsed = parse_question(question)
            st.write("### Parsed Output")
            st.json(parsed)

            query, params = build_sql_advanced(parsed)
            st.write("### Generated SQL")
            st.code(query, language="sql")

            st.write("### Parameters")
            st.write(params)

            sql_result = execute_sql(query, params, conn)
            final_response = explain_result(question, sql_result)

            st.write("### Assistant Answer")
            st.success(final_response["final_answer"])

        except Exception as e:
            st.error(f"Error: {e}")

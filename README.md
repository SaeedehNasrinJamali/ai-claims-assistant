AI Claims Assistant

- Overview  
This project builds an AI-powered assistant that translates natural language questions into SQL queries to analyze insurance claims data.

The goal is to simulate how business users interact with data — asking questions in plain English and receiving clear, data-driven answers.

- How It Works  

The system follows a 4-step pipeline:

1. Question Parsing (LLM)  
   Converts a user question into structured JSON (intent, metric, filters)

2. SQL Generation  
   Translates structured JSON into safe SQL queries

3. SQL Execution  
   Runs queries on the database and returns results

4. Result Explanation (LLM)  
   Converts results into business-friendly answers

- Example   

User Question  
What is the average claim amount for Auto policies in Quebec?

Final Answer  
The average claim amount for Auto policies in Quebec is approximately $1,415.

- Demo Video  

This demo shows the full workflow using a Streamlit interface:
question → parsed output → query → final answer  

Demo Video

https://youtu.be/mztlE-iEQdM?si=mqmgqJW-hWgVxSvE
---
- Tech Stack  
Python, SQL, OpenAI API, Pandas, Streamlit



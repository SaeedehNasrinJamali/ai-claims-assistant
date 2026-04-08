import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def explain_result(question, sql_result):
    """
    Turn SQL results into a clear business-friendly answer.
    """

    if sql_result["status"] == "error":
        return {
            "status": "error",
            "final_answer": f"The query could not be completed. Reason: {sql_result['message']}"
        }

    if sql_result["data"] is None:
        return {
            "status": "success",
            "final_answer": "No data was found for the requested question and filters."
        }

    result_text = json.dumps(sql_result["data"], indent=2)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a business data assistant. "
                "Write a short, clear, professional answer based only on the SQL result. "
                "Do not invent numbers. "
                "If the result is a single value, answer in one sentence. "
                "If the result is grouped data, summarize it clearly."
            )
        },
        {
            "role": "user",
            "content": f"""
User question:
{question}

SQL result:
{result_text}

Write a concise business-friendly answer.
"""
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        temperature=0
    )

    final_answer = response.choices[0].message.content.strip()

    return {
        "status": "success",
        "final_answer": final_answer
    }

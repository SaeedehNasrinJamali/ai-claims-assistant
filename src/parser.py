import json
from openai import OpenAI
from config import OPENAI_API_KEY

# Create API client safely (no hardcoded key)
client = OpenAI(api_key=OPENAI_API_KEY)


def parse_question(question: str) -> dict:
    """
    Takes a user question and returns a structured dictionary
    with intent, metric, and filters.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are a data query parser. "
                "Extract the user's question into structured fields."
            ),
        },
        {
            "role": "user",
            "content": f"""
Extract the following fields from the question:

- intent: one of ["aggregation", "comparison", "trend", "detail"]
- metric: one of ["total_claim", "average_claim", "count_claim"]
- filters: a JSON object of conditions like region, policy_type, or year

Return ONLY valid JSON.

Use exactly this structure:
{{
  "intent": "string",
  "metric": "string",
  "filters": {{}}
}}

Question: {question}
"""
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0
    )

    output_text = response.choices[0].message.content
    data = json.loads(output_text)

    # Validation
    required_keys = ["intent", "metric", "filters"]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing key in model output: {key}")

    if not isinstance(data["filters"], dict):
        raise ValueError("The 'filters' field must be a dictionary.")

    return data

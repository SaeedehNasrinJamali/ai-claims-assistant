import pandas as pd


def execute_sql(query, params, connection):
    """
    Execute SQL query safely and return results.
    """

    try:
        df = pd.read_sql(query, connection, params=params)

        if df.empty:
            return {
                "status": "success",
                "data": None,
                "message": "No data found for the given query."
            }

        result = df.to_dict(orient="records")

        return {
            "status": "success",
            "data": result,
            "message": "Query executed successfully."
        }

    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "message": str(e)
        }

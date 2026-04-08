def build_sql_advanced(parsed_output):
    """
    Convert parsed LLM output into a safe SQL query.
    """

    # Define allowed schema
    ALLOWED_METRICS = {
        "average_claim": "AVG(claim_amount)",
        "average_claim_amount": "AVG(claim_amount)",
        "avg_claim_amount": "AVG(claim_amount)",
        "total_claim": "SUM(claim_amount)",
        "total_claims": "SUM(claim_amount)",
        "total_claim_amount": "SUM(claim_amount)",
        "sum_claim_amount": "SUM(claim_amount)",
        "count_claim": "COUNT(*)",
        "claim_count": "COUNT(*)",
        "count_claims": "COUNT(*)",
        "number_of_claims": "COUNT(*)"
    }

    ALLOWED_COLUMNS = {
        "region": "region",
        "policy_type": "policy_type",
        "year": "claim_year"
    }

    TABLE_NAME = "claims_cleaned"

    # Extract parsed fields
    metric_key = parsed_output.get("metric")
    filters = parsed_output.get("filters", {})

    # Validate metric
    if metric_key not in ALLOWED_METRICS:
        raise ValueError(f"Invalid metric: {metric_key}")

    metric_sql = ALLOWED_METRICS[metric_key]

    # Build SELECT
    query = f"SELECT {metric_sql} AS result FROM {TABLE_NAME}"

    # Build WHERE safely
    where_clauses = []
    params = []

    for key, value in filters.items():
        if key not in ALLOWED_COLUMNS:
            raise ValueError(f"Invalid filter column: {key}")

        column = ALLOWED_COLUMNS[key]
        where_clauses.append(f"{column} = ?")
        params.append(value)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    # GROUP BY
    group_by = parsed_output.get("group_by")

    if group_by:
        if group_by not in ALLOWED_COLUMNS:
            raise ValueError(f"Invalid group_by: {group_by}")

        group_column = ALLOWED_COLUMNS[group_by]
        query = query.replace("SELECT", f"SELECT {group_column}, ", 1)
        query += f" GROUP BY {group_column}"

    return query, params

import pandas as pd
import sqlite3


def load_data():
    df = pd.read_csv("data/claims_cleaned.csv")
    conn = sqlite3.connect("claims.db")
    df.to_sql("claims_cleaned", conn, index=False, if_exists="replace")
    conn.close()

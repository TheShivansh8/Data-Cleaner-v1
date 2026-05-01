""" Project: Smart Dataset Cleaner (Python CLI Tool)

What it does:

Takes a messy CSV
Cleans nulls
Standardizes columns
Outputs a structured dataset ready for analysis """
import pandas as pd
import os
import sqlite3

def load_data(source, source_type="file"):
    if source_type == "file":
        return load_file(source)
    elif source_type == "sql":
        return load_sql(source)
    else:
        raise ValueError("Unsupported source type")


def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format")

    print(f"[INFO] Loaded file: {df.shape}")
    return df


def load_sql(db_config):
    if db_config["db_type"] == "sqlite":
        conn = sqlite3.connect(db_config["db_path"])
        df = pd.read_sql_query(db_config["query"], conn)
        conn.close()
    else:
        raise ValueError("Only SQLite supported for now")

    print(f"[INFO] Loaded SQL data: {df.shape}")
    return df
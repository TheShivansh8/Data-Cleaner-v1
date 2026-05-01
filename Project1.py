""" Project: Smart Dataset Cleaner (Python CLI Tool)

What it does:

Takes a messy CSV
Cleans nulls
Standardizes columns
Outputs a structured dataset ready for analysis """
import pandas as pd
import os
import sqlite3
import argparse
import logging

# ---------- LOGGING ----------
logging.basicConfig(level=logging.INFO)

# ---------- LOADERS ----------
def load_data(source, source_type="file"):
    if source_type == "file":
        return load_file(source)
    elif source_type == "sql":
        return load_sql(source)
    else:
        raise ValueError("Unsupported source type")


def load_file(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")

        logging.info(f"Loaded file with shape: {df.shape}")
        return df

    except Exception as e:
        logging.error(f"Failed to load file: {e}")
        exit()


def load_sql(db_config):
    try:
        if db_config["db_type"] == "sqlite":
            conn = sqlite3.connect(db_config["db_path"])
            df = pd.read_sql_query(db_config["query"], conn)
            conn.close()
        else:
            raise ValueError("Only SQLite supported")

        logging.info(f"Loaded SQL data: {df.shape}")
        return df

    except Exception as e:
        logging.error(f"SQL loading failed: {e}")
        exit()


# ---------- CLEANING ----------
def clean_data(df):
    logging.info("Cleaning data...")

    df = df.drop_duplicates()

    for col in df.select_dtypes(include=["float64", "int64"]).columns:
        df[col].fillna(df[col].mean(), inplace=True)

    for col in df.select_dtypes(include=["object"]).columns:
        if not df[col].mode().empty:
            df[col].fillna(df[col].mode()[0], inplace=True)

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    logging.info("Cleaning complete")
    return df


# ---------- SAVE ----------
def save_data(df, output_path):
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"Saved cleaned data to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save file: {e}")
        exit()


# ---------- MAIN ----------
def main():
    parser = argparse.ArgumentParser(description="Dataset Cleaner Tool")

    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()

    df = load_data(args.input, "file")
    cleaned_df = clean_data(df)
    save_data(cleaned_df, args.output)


if __name__ == "__main__":
    main()

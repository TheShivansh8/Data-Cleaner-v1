""" Project: Smart Dataset Cleaner (Python CLI Tool)

What it does:

Takes a messy CSV
Cleans nulls
Standardizes columns
Outputs a structured dataset ready for analysis """
import streamlit as st
import pandas as pd

st.title("Smart Dataset Cleaner")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

def clean_data(df):
    df = df.drop_duplicates()

    for col in df.select_dtypes(include=["float64", "int64"]).columns:
        df[col].fillna(df[col].mean(), inplace=True)

    for col in df.select_dtypes(include=["object"]).columns:
        if not df[col].mode().empty:
            df[col].fillna(df[col].mode()[0], inplace=True)

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df
if uploaded_file is not None:
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        except ImportError:
            st.warning("Excel not supported on this deployment. Convert to CSV.")
            st.stop()
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
            st.stop()

    else:
        st.error("Unsupported file format. Use CSV or Excel.")
        st.stop()

    st.subheader("Original Data")
    st.dataframe(df.head())

    cleaned_df = clean_data(df)

    st.subheader("Cleaned Data")
    st.dataframe(cleaned_df.head())

    st.write(f"Rows before: {len(df)}")
    st.write(f"Rows after: {len(cleaned_df)}")

    st.download_button(
        "Download Cleaned File",
        cleaned_df.to_csv(index=False),
        "cleaned.csv"
    )

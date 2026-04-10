import pandas as pd
import sqlite3
import os

def run_etl(csv_path, db_path='retail_dw.db'):
    print(f"Starting ETL Process for {csv_path}...")
    
    # 1. Extract
    print("Extracting data...")
    try:
        # Read the core columns
        cols = ['Transaction ID', 'Date', 'Gender', 'Age', 'Age Group', 'Product Category', 'Quantity', 'Price per Unit', 'Total Amount']
        df = pd.read_csv(csv_path, usecols=cols)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # 2. Transform
    print("Transforming data...")
    # Drop empty rows
    df = df.dropna(subset=['Transaction ID'])
    
    # Format Date to YYYY-MM-DD
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    
    # Ensure numerical columns are proper types
    df['Age'] = df['Age'].astype(int)
    df['Quantity'] = df['Quantity'].astype(int)
    df['Price per Unit'] = df['Price per Unit'].astype(float)
    df['Total Amount'] = df['Total Amount'].astype(float)

    # 3. Load
    print(f"Loading data into {db_path}...")
    conn = sqlite3.connect(db_path)
    
    # We load it as a single Analytics Flat Table suitable for BI dashboards
    df.to_sql('Sales_Analytics', conn, if_exists='replace', index=False)
    
    conn.close()
    print("ETL Process Complete! Data Warehouse is ready.")

if __name__ == "__main__":
    csv_file = r"C:\Users\Magizh P\Downloads\Retail Sales Data Set.csv"
    run_etl(csv_file)

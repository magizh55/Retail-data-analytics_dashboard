# Retail Business Intelligence Dashboard

This project is a dynamic, end-to-end Business Intelligence (BI) system for retail data analysis. Built completely in Python, it transforms raw sales data into an interactive, visually appealing Streamlit dashboard.

## Objective
To provide retail managers and analysts an easy-to-use platform to track key performance indicators (KPIs) like Total Revenue, Items Sold, and Demographics breakdown, allowing them to rapidly extract actionable insights from flat `.csv` datasets.

## Architecture

1. **Extraction**: The system reads raw flat-file data, specifically the `Retail Sales Data Set.csv`.
2. **Transformation**: Using **Pandas**, the data is cleaned (dropping invalid records), transformed (formatting dates), and types are normalized.
3. **Loading**: The transformed dataset is persisted into a lightweight, local **SQLite** Database (`retail_dw.db`) designed for fast analytical queries.
4. **Presentation**: A **Streamlit** dashboard uses **Plotly Express** to visualize the localized SQLite data in real-time.

## Technology Stack

- **Python 3.x**
- **Pandas**: Fast data manipulation and ETL.
- **SQLite3**: Serverless Data Warehouse / analytical database.
- **Streamlit**: Rapid web-application framework for the UI.
- **Plotly Express**: Interactive charts and dynamic visualizations.

## How to Run

1. Place your dataset (`Retail Sales Data Set.csv`) in the base directory.
2. Ensure you have the required libraries installed:
   ```bash
   pip install pandas streamlit plotly
   ```
3. Run the ETL Pipeline to build the SQLite database:
   ```bash
   python etl/etl_pipeline.py
   ```
4. Start the interactive dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

## Features

- **Dynamic Demographics Analysis**: Visualizations tailored explicitly for Gender and Age Group segmentations.
- **Category Economics**: Deep dive into Revenue by Product Category via interactive Pie Charts.
- **Trend Tracking**: Time-series charts mapping Revenue Over Time to detect seasonality and spikes.
- **Robust Filtering**: Sidebar controls allowing users to drill down by Gender, Age Group, and Product Category simultaneously.

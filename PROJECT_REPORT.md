# Project Report: Retail Sales Data Intelligence

## 1. Executive Summary
This project successfully implemented an end-to-end extraction, transformation, load (ETL) pipeline and business intelligence dashboard. Specifically calibrated for the `Retail Sales Data Set.csv`, the architecture was transitioned from generating synthetic geographic mock data to prioritizing 100% genuine insights based purely on the original dataset's parameters.

## 2. Dataset Overview
The application consumes a `.csv` encompassing individual retail transactions. The core fields isolated and ingested into the system are:
- `Transaction ID` (Primary Identifier)
- `Date` (Chronological tracking)
- `Gender` & `Age Group` (Customer Demographics)
- `Product Category` (Inventory Categorization)
- `Quantity`, `Price per Unit`, `Total Amount` (Financial Metrics)

## 3. Data Engineering (ETL) Process
The pipeline (`etl_pipeline.py`) performs the following streamlined operations:
1. **Extraction**: Loads targeted columns directly from the `.csv` file via Pandas.
2. **Cleansing**: Automatically purges Excel junk columns and eradicates rows missing crucial `Transaction ID` keys.
3. **Typing & Formatting**: Enforces chronological `YYYY-MM-DD` string parsing for robust SQL compatibility and ensures financial metrics are safely typed as floating-point decimals.
4. **Data Warehousing**: Pushes the fully cleansed DataFrame into a localized `SQLite` database (`retail_dw.db`), residing in a core `Sales_Analytics` table. This acts as our localized Data Warehouse, ensuring the frontend dashboard never has to perform computationally heavy CSV re-parsing.

## 4. Dashboard Implementation
The presentation layer (`app.py`) leverages Streamlit to provide real-time interaction with the SQLite Warehouse.

### Key Visualizations:
- **KPI Dashboards**: Top-line summary of Total Revenue, Total Items Sold, and Total Unique Transactions.
- **Revenue Over Time**: A spline-curve line chart plotting fluid financial trends chronologically.
- **Market Share**: A donut-style pie chart visualizing absolute revenue per Product Category.
- **Demographic Penetration**: A clustered bar chart (`Revenue per Age Group by Gender`) evaluating how different demographic cross-sections perform monetarily.

### Filtering Capabilities:
The user is empowered with a persistent sidebar permitting global data slicing by:
- Gender
- Age Group
- Product Category
Any filter manipulation executes a live SQL/Pandas slice and completely ripples through every single visualization and KPI simultaneously.

## 5. Conclusion
By transitioning from a bulky Mock-Star Schema to a streamlined, flat Analytical Database, the application now boasts lightning-fast data loads and charts that faithfully represent undeniable ground truth. The system is scalable, easily deployable, and ready to ingest future subsets of the Retail Sales Data seamlessly.

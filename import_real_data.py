import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

def import_real_data(csv_path, output_dir='data'):
    print(f"Reading real data from: {csv_path}")
    
    # Read only the relevant columns to ignore excel junk
    cols = ['Transaction ID', 'Date', 'Gender', 'Age', 'Age Group', 'Product Category', 'Quantity', 'Price per Unit', 'Total Amount']
    df = pd.read_csv(csv_path, usecols=cols)
    
    # Clean data (drop rows where Transaction ID is NaN)
    df = df.dropna(subset=['Transaction ID'])
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Generate Products Dimension
    # We group by Product Category and Price per Unit to create unique products
    unique_products = df[['Product Category', 'Price per Unit']].drop_duplicates().reset_index(drop=True)
    unique_products['product_id'] = unique_products.index + 1
    unique_products['product_name'] = unique_products.apply(lambda x: f"{x['Product Category']} at ${x['Price per Unit']:.2f}", axis=1)
    
    products_dim = unique_products[['product_id', 'product_name', 'Product Category', 'Price per Unit']].copy()
    products_dim.columns = ['product_id', 'product_name', 'category', 'price']
    products_dim.to_csv(os.path.join(output_dir, 'mock_products.csv'), index=False)
    print("Generated mock_products.csv")

    # 2. Generate Stores Dimension (Synthetic since real data lacks it)
    regions = ['North', 'South', 'East', 'West']
    stores = []
    for i in range(1, 11): # 10 Stores
        stores.append({
            'store_id': i,
            'store_name': f"Store {fake.city()}",
            'city': fake.city(),
            'region': random.choice(regions)
        })
    pd.DataFrame(stores).to_csv(os.path.join(output_dir, 'mock_stores.csv'), index=False)
    print("Generated mock_stores.csv")

    # 3. Generate Customers Dimension
    # We group by Gender and Age Group to create synthetic customers
    customer_groups = df[['Gender', 'Age Group']].drop_duplicates().reset_index(drop=True)
    customer_groups['customer_id'] = customer_groups.index + 1
    # Generate fake names considering gender roughly
    def generate_name(gender):
        if gender.lower() == 'male': return fake.name_male()
        elif gender.lower() == 'female': return fake.name_female()
        return fake.name()
        
    customer_groups['customer_name'] = customer_groups['Gender'].apply(generate_name)
    customers_dim = customer_groups[['customer_id', 'customer_name', 'Age Group']].copy()
    customers_dim.columns = ['customer_id', 'customer_name', 'segment']
    customers_dim.to_csv(os.path.join(output_dir, 'mock_customers.csv'), index=False)
    print("Generated mock_customers.csv")

    # 4. Generate Sales Facts
    # Map back IDs
    merged_df = df.merge(unique_products, on=['Product Category', 'Price per Unit'], how='left')
    merged_df = merged_df.merge(customer_groups, on=['Gender', 'Age Group'], how='left')
    
    # Format Date
    # Date in dataset looks like 11/24/2023. ETL expects '%Y-%m-%d' typically (or pandas to_datetime handles it)
    merged_df['Date'] = pd.to_datetime(merged_df['Date']).dt.strftime('%Y-%m-%d')
    
    # Assign a random store to each transaction
    merged_df['store_id'] = [random.choice(stores)['store_id'] for _ in range(len(merged_df))]
    
    sales_dim = merged_df[['Transaction ID', 'Date', 'product_id', 'store_id', 'customer_id', 'Quantity', 'Total Amount']].copy()
    sales_dim.columns = ['sale_id', 'date', 'product_id', 'store_id', 'customer_id', 'quantity', 'total_amount']
    # Cast Transaction ID to int if it's numeric
    sales_dim['sale_id'] = sales_dim['sale_id'].astype(int)
    
    sales_dim.to_csv(os.path.join(output_dir, 'mock_sales.csv'), index=False)
    print("Generated mock_sales.csv")

if __name__ == "__main__":
    import_real_data(r"C:\Users\Magizh P\Downloads\Retail Sales Data Set.csv")

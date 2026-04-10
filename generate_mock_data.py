import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

def generate_mock_data(output_dir='data'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Generate Products
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys']
    products = []
    for i in range(1, 101):
        cat = random.choice(categories)
        price = round(random.uniform(10.0, 500.0), 2)
        products.append({
            'product_id': i,
            'product_name': f"{cat} Item {i}",
            'category': cat,
            'price': price
        })
    pd.DataFrame(products).to_csv(os.path.join(output_dir, 'mock_products.csv'), index=False)
    print("Generated mock_products.csv")

    # 2. Generate Stores
    regions = ['North', 'South', 'East', 'West']
    stores = []
    for i in range(1, 21):
        stores.append({
            'store_id': i,
            'store_name': f"Store {fake.city()}",
            'city': fake.city(),
            'region': random.choice(regions)
        })
    pd.DataFrame(stores).to_csv(os.path.join(output_dir, 'mock_stores.csv'), index=False)
    print("Generated mock_stores.csv")

    # 3. Generate Customers
    segments = ['Regular', 'Premium', 'VIP']
    customers = []
    for i in range(1, 1001):
        customers.append({
            'customer_id': i,
            'customer_name': fake.name(),
            'segment': random.choice(segments)
        })
    pd.DataFrame(customers).to_csv(os.path.join(output_dir, 'mock_customers.csv'), index=False)
    print("Generated mock_customers.csv")

    # 4. Generate Sales Facts
    sales = []
    start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    for i in range(1, 10001): # 10,000 sales
        days_offset = random.randint(0, 365)
        sale_date = start_date + timedelta(days=days_offset)
        prod = random.choice(products)
        qty = random.randint(1, 5)
        total = round(prod['price'] * qty, 2)
        
        sales.append({
            'sale_id': i,
            'date': sale_date.strftime('%Y-%m-%d'),
            'product_id': prod['product_id'],
            'store_id': random.choice(stores)['store_id'],
            'customer_id': random.choice(customers)['customer_id'],
            'quantity': qty,
            'total_amount': total
        })
    pd.DataFrame(sales).to_csv(os.path.join(output_dir, 'mock_sales.csv'), index=False)
    print("Generated mock_sales.csv")

if __name__ == "__main__":
    generate_mock_data()

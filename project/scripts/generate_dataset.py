import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

NUM_RECORDS = 5500

cities = [
    "Chennai", "chennai", "CHENNAI", " Chennai ", "Mumbai", "mumbai", "MUMBAI",
    "Delhi", "delhi", "DELHI", "Bangalore", "bangalore", "BANGALORE",
    "Hyderabad", "hyderabad", "Kolkata", "kolkata", "Pune", "pune"
]

customer_segments = [
    "Premium", "premium", "PREMIUM", "Regular", "regular", "REGULAR",
    "New", "new", "NEW", "Inactive", "inactive"
]

product_categories = [
    "Electronics", "electronics", "ELECTRONICS", "Clothing", "clothing",
    "Groceries", "groceries", "GROCERIES", "Furniture", "furniture",
    "Sports", "sports", "Books", "books"
]

payment_types = [
    "Credit Card", "credit card", "CREDIT CARD", "Debit Card", "debit card",
    "UPI", "upi", "Net Banking", "net banking", "Cash", "cash"
]

records = []

for i in range(1, NUM_RECORDS + 1):
    customer_id = i
    age = random.randint(18, 70)
    city = random.choice(cities)
    customer_segment = random.choice(customer_segments)
    product_category = random.choice(product_categories)
    order_count = random.randint(1, 50)
    average_order_value = round(random.uniform(500, 50000), 2)
    total_spend = round(order_count * average_order_value, 2)
    discount_percentage = round(random.uniform(0, 50), 2)
    days_since_last_order = random.randint(1, 365)
    website_visits = random.randint(1, 200)
    support_tickets = random.randint(0, 20)
    return_count = random.randint(0, order_count)
    payment_type = random.choice(payment_types)
    customer_tenure_days = random.randint(30, 1825)

    records.append({
        "customer_id": customer_id,
        "age": age,
        "city": city,
        "customer_segment": customer_segment,
        "product_category": product_category,
        "order_count": order_count,
        "average_order_value": average_order_value,
        "total_spend": total_spend,
        "discount_percentage": discount_percentage,
        "days_since_last_order": days_since_last_order,
        "website_visits": website_visits,
        "support_tickets": support_tickets,
        "return_count": return_count,
        "payment_type": payment_type,
        "customer_tenure_days": customer_tenure_days
    })

df = pd.DataFrame(records)

# missing values
missing_indices = np.random.choice(df.index, size=300, replace=False)
df.loc[missing_indices[:100], "age"] = np.nan
df.loc[missing_indices[100:200], "city"] = np.nan
df.loc[missing_indices[200:300], "average_order_value"] = np.nan

# missing values in order_count (simulates data entry gaps)
# also zero out return_count for those rows — can't have returns without a known order count
nan_order_indices = np.random.choice(df.index, size=40, replace=False)
df.loc[nan_order_indices, "order_count"] = np.nan
df.loc[nan_order_indices, "return_count"] = 0

# duplicate records
duplicate_rows = df.sample(n=100, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# invalid numeric values
invalid_indices = np.random.choice(df.index, size=50, replace=False)
df.loc[invalid_indices[:25], "age"] = -5
df.loc[invalid_indices[25:], "discount_percentage"] = 150

# outliers
outlier_indices = np.random.choice(df.index, size=30, replace=False)
df.loc[outlier_indices[:15], "total_spend"] = round(random.uniform(5000000, 9000000), 2)
df.loc[outlier_indices[15:], "website_visits"] = random.randint(5000, 10000)

os.makedirs("data", exist_ok=True)
df.to_csv("data/customers_raw.csv", index=False)
print(f"Dataset generated: {len(df)} records saved to data/customers_raw.csv")

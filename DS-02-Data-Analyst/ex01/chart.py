import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# 1. Database Connection
db_user = 'abelhadj' 
db_password = 'mysecretpassword'
db_host = 'localhost'
db_name = 'piscineds'

try:
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}')
    print("Connected to PostgreSQL successfully!\n")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

# 2. Query the Data (Let SQL do the heavy lifting!)
# We only grab 'purchase' events, and we only need the time, price, and user_id
query = """
    SELECT event_time, price, user_id
    FROM customers
    WHERE event_type = 'purchase'
"""

try:
    df = pd.read_sql(query, engine)
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

# 3. Clean and Prep the Data in Pandas
# Convert event_time to actual DateTime objects so Pandas can understand the dates
df['event_time'] = pd.to_datetime(df['event_time'])

# Create a 'date' column for daily math, and a 'month' column for monthly math
df['date'] = df['event_time'].dt.date
# .dt.to_period('M') keeps the months in strict chronological order (2022-10, 2022-11...)
df['month'] = df['event_time'].dt.to_period('M') 

# --- Crunching the numbers ---
# Chart 1: Daily unique customers
daily_customers = df.groupby('date')['user_id'].nunique()

# Chart 2: Total sales per month (divided by 1,000,000 to get "millions")
monthly_sales = df.groupby('month')['price'].sum() / 1000000

# Chart 3: Average spend per customer per day
daily_sales = df.groupby('date')['price'].sum()
avg_spend_per_customer = daily_sales / daily_customers


# 4. Paint the Dashboard
# Create 1 big figure with 3 canvases (axes) stacked on top of each other
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))

# --- Chart 1: Number of Customers (Line Chart) ---
daily_customers.plot(ax=ax1, color='#4c72b0')
ax1.set_ylabel('Number of customers')
ax1.set_xlabel('')

# --- Chart 2: Total Sales in Millions (Bar Chart) ---
# We use .dt.strftime('%b') to make the labels just say 'Oct', 'Nov', 'Feb', etc.
monthly_sales.index = monthly_sales.index.strftime('%b')
monthly_sales.plot.bar(ax=ax2, color='#8da0cb', width=0.8, rot=0)
ax2.set_ylabel('total sales in million of ₳')
ax2.set_xlabel('month')

# --- Chart 3: Average Spend per Customer (Filled Area Chart) ---
avg_spend_per_customer.plot(ax=ax3, color='#8da0cb')
# .fill_between fills the space under the line to mimic the PDF example
ax3.fill_between(avg_spend_per_customer.index, avg_spend_per_customer.values, color='#8da0cb', alpha=1)
ax3.set_ylabel('average spend/customers in ₳')
ax3.set_xlabel('')

# Clean up layout so nothing overlaps and display!
plt.tight_layout()
plt.show()
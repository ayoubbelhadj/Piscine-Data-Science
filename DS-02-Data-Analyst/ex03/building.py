import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

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
query = """
    SELECT user_id, user_session, price
    FROM customers
    WHERE event_type = 'purchase'
"""
try:
    df = pd.read_sql(query, engine)
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()


# FREQUENCY: Count the number of unique shopping trips (sessions) per user
frequency = df.groupby('user_id')['user_session'].nunique()

# MONETARY: Calculate the total lifetime spend for each user
monetary = df.groupby('user_id')['price'].sum()


fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

freq_filtered = frequency[frequency < 10]

ax1.hist(freq_filtered, bins=10, color='#a0b9d9', edgecolor='white')
ax1.set_xlabel('frequency')
ax1.set_ylabel('customers')

mon_filtered = monetary[monetary < 250]

ax2.hist(mon_filtered, bins=5, color='#a0b9d9', edgecolor='white')
ax2.set_xlabel('monetary value in ₳')
ax2.set_ylabel('customers')


for ax in [ax1, ax2]:
    ax.set_facecolor('#eaeaf2')
    ax.grid(color='white', linestyle='-', linewidth=1)
    ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
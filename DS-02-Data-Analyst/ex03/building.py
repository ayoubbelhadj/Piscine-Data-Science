import sys
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

DB_USER = 'abelhadj'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_NAME = 'piscineds'

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

query = """
    SELECT user_id, user_session, price
    FROM customers
    WHERE event_type = 'purchase'
"""

try:
    df = pd.read_sql(query, engine)
except Exception as e:
    print(f"Error running query: {e}")
    sys.exit(1)

frequency = df.groupby('user_id')['user_session'].nunique()
monetary  = df.groupby('user_id')['price'].sum()

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

ax1.hist(frequency, bins=range(1, 11), color='#a0b9d9', edgecolor='white')
ax1.set_xlabel('frequency')
ax1.set_ylabel('customers')

ax2.hist(monetary, bins=range(0, 251, 50), color='#a0b9d9', edgecolor='white')
ax2.set_xlabel('monetary value in ₳')
ax2.set_ylabel('customers')

for ax in [ax1, ax2]:
    ax.set_facecolor('#eaeaf2')
    ax.grid(color='white', linestyle='-', linewidth=1)
    ax.set_axisbelow(True)

plt.savefig('building.png')
plt.show()
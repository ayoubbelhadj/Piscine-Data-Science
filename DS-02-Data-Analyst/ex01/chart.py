import sys
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DB_USER = 'abelhadj'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_NAME = 'piscineds'

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

query = """
    SELECT event_time, price, user_id
    FROM customers
    WHERE event_type = 'purchase'
"""

try:
    df = pd.read_sql(query, engine)
except Exception as e:
    print(f"Error running query: {e}")
    sys.exit(1)

df['event_time'] = pd.to_datetime(df['event_time'])
df['date']  = df['event_time'].dt.normalize()

df['month'] = df['event_time'].dt.to_period('M')

# One groupby, two aggregations
daily = df.groupby('date').agg(
    customers=('user_id', 'nunique'),
    sales=('price', 'sum')
)

monthly_sales = df.groupby('month')['price'].sum() / 1_000_000
monthly_sales.index = monthly_sales.index.strftime('%b')

avg_spend = daily['sales'] / daily['customers']

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))

daily['customers'].plot(ax=ax1, color='#4c72b0')
ax1.set_ylabel('Number of customers')
ax1.set_xlabel('')
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

monthly_sales.plot.bar(ax=ax2, color='#8da0cb', width=0.8, rot=0)
ax2.set_ylabel('total sales in million of ₳')
ax2.set_xlabel('month')

avg_spend.plot(kind='area', ax=ax3, color='#8da0cb', alpha=1)
ax3.set_ylabel('average spend/customers in ₳')
ax3.set_xlabel('')
ax3.xaxis.set_major_locator(mdates.MonthLocator())
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.savefig('chart.png')
plt.show()
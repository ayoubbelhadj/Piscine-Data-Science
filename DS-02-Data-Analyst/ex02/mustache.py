import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

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

pd.set_option('display.float_format', lambda x: '%.6f' % x)

query = """
    SELECT price, user_id, user_session
    FROM customers
    WHERE event_type = 'purchase'
"""

try:
    df = pd.read_sql(query, engine)
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

print("-- Purchase Item Price Statistics --")
print(df['price'].describe().to_string())
print("-" * 36)

basket_totals = df.groupby(['user_id', 'user_session'])['price'].sum().reset_index()

avg_basket_per_user = basket_totals.groupby('user_id')['price'].mean()

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))

# --- Chart 1: Full Item Prices ---
sns.boxplot(x=df['price'], ax=ax1, color='#768973', orient='h')
ax1.set_xlabel('price')

# --- Chart 2: Zoomed-In Item Prices ---
sns.boxplot(x=df['price'], ax=ax2, color='#84ca84', orient='h', showfliers=False)
ax2.set_xlabel('price')

# --- Chart 3: Average Basket Price per User ---
sns.boxplot(x=avg_basket_per_user, ax=ax3, color='#7cb2d6', orient='h', showfliers=False)
ax3.set_xlabel('price')

for ax in [ax1, ax2, ax3]:
    ax.grid(True, linestyle='-', color='white', alpha=0.7)
    ax.set_facecolor('#eaeaf2')

plt.tight_layout()
plt.show()
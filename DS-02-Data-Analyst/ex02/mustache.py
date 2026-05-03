import sys
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

DB_USER = 'abelhadj'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_NAME = 'piscineds'

engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
)

pd.set_option('display.float_format', lambda x: '%.6f' % x)

query = """
    SELECT price, user_id, user_session
    FROM customers
    WHERE event_type = 'purchase'
"""

try:
    df = pd.read_sql(query, engine)
except Exception as e:
    print(f"Error running query: {e}")
    sys.exit(1)

print("-- Purchase Item Price Statistics --")
print(df['price'].describe().to_string())
print("-" * 36)

basket_totals = df.groupby(['user_id', 'user_session'])['price'].sum().reset_index()
avg_basket_per_user = basket_totals.groupby('user_id')['price'].mean()

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))

# --- Chart 1: Full item prices (with outliers visible) ---
sns.boxplot(x=df['price'], ax=ax1, color='lightgreen')
ax1.set_xlabel('price')

# --- Chart 2: Item prices, zoomed (outliers hidden) ---
sns.boxplot(x=df['price'], ax=ax2, color='#84ca84', showfliers=False)
ax2.set_xlabel('price')

# --- Chart 3: Average basket price per user ---
sns.boxplot(x=avg_basket_per_user, ax=ax3, color='#7cb2d6', showfliers=False)
ax3.set_xlabel('price')

for ax in [ax1, ax2, ax3]:
    ax.grid(True, linestyle='-', color='white', alpha=0.7)
    ax.set_facecolor('#eaeaf2')

plt.savefig('mustache.png')
plt.show()
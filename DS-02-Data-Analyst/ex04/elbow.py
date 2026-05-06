import sys
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

DB_USER = 'abelhadj'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_NAME = 'piscineds'

engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
)

query = """
    SELECT user_id, user_session, price, event_time
    FROM customers
    WHERE event_type = 'purchase'
"""

try:
    df = pd.read_sql(query, engine)
except Exception as e:
    print(f"Error running query: {e}")
    sys.exit(1)

reference_date = df['event_time'].max()
last_purchase = df.groupby('user_id')['event_time'].max()
recency = (reference_date - last_purchase).dt.days
frequency = df.groupby('user_id')['user_session'].nunique()
monetary = df.groupby('user_id')['price'].sum()

features = pd.DataFrame({
    'recency':   recency,
    'frequency': frequency,
    'monetary':  monetary,
})


scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)


inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)


plt.plot(range(1, 11), inertias, marker='o')
plt.xticks(range(1, 11))
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('The Elbow Method')
plt.grid(True)
plt.savefig('elbow.png')
plt.show()

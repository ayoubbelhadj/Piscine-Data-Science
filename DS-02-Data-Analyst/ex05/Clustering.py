import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

DB_USER = 'abelhadj'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_NAME = 'piscineds'

CHOSEN_K = 4

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
recency = (reference_date - df.groupby('user_id')['event_time'].max()).dt.days
frequency = df.groupby('user_id')['user_session'].nunique()
monetary = df.groupby('user_id')['price'].sum()

features = pd.DataFrame({
    'recency':   recency,
    'frequency': frequency,
    'monetary':  monetary,
}).dropna()


scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

km = KMeans(n_clusters=CHOSEN_K, random_state=42, n_init=10)
km.fit(X_scaled)

features['cluster'] = km.labels_

profile = features.groupby('cluster').agg(
    median_recency=('recency', 'median'),
    median_frequency=('frequency', 'median'),
    mean_monetary=('monetary', 'mean'),
    count=('recency', 'size'),
)
print("\n--- Cluster Profile ---")
print(profile)

cluster_names = {
    2: 'platinum',
    0: 'loyal',
    1: 'new customers',
    3: 'inactive',
}

print("\n--- Cluster Labels ---")
for c, name in cluster_names.items():
    print(f"  Cluster {c}: {name}  (n={profile.loc[c, 'count']})")

profile['name'] = profile.index.map(cluster_names)
profile['recency_months'] = profile['median_recency'] / 30

colors = {
    'platinum':       '#9b59b6',
    'loyal':          '#2ecc71',
    'new customers':  '#3498db',
    'inactive':       '#e74c3c',
}

print(profile)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(9, 16))

# --- Chart 1: Horizontal bar chart of customer counts per segment ---
segment_counts = (
    profile[['count', 'name']].sort_values('count', ascending=True)
)
bar_colors = [colors[name] for name in segment_counts['name']]

bars = ax1.barh(
    segment_counts['name'],
    segment_counts['count'],
    color=bar_colors,
    edgecolor='white',
)
ax1.bar_label(bars, padding=5, fontsize=11)
ax1.set_xlabel('number of customers')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)


# --- Chart 2: Bubble chart (business view) ---
ax2.scatter(
    x=profile['recency_months'],
    y=profile['median_frequency'],
    s=profile['count'] / 50,
    alpha=0.6,
    color=[colors[n] for n in profile['name']],
)
for cluster_idx, row in profile.iterrows():
    ax2.annotate(
        f'Average "{row["name"]}": {row["mean_monetary"]:.0f}₳',
        xy=(row['recency_months'], row['median_frequency']),
        xytext=(8, 0),
        textcoords='offset points',
        fontsize=9,
        ha='left',
        va='center',
    )
ax2.set_xlabel('Median Recency (month)')
ax2.set_ylabel('Median Frequency')
ax2.set_ylim(bottom=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# --- Chart 3: Cluster scatter (frequency vs monetary, with jitter) ---
draw_order = ['inactive', 'new customers', 'loyal', 'platinum']
name_to_cluster = {v: k for k, v in cluster_names.items()}

for name in draw_order:
    cluster_idx = name_to_cluster[name]
    cluster_data = features[features['cluster'] == cluster_idx]
    jitter = np.random.uniform(-0.3, 0.3, size=len(cluster_data))
    ax3.scatter(
        cluster_data['frequency'] + jitter,
        cluster_data['monetary'],
        label=name,
        alpha=0.4,
        s=60,
        color=colors[name],
    )

centroids_original = scaler.inverse_transform(km.cluster_centers_)
ax3.scatter(
    centroids_original[:, 1],
    centroids_original[:, 2],
    color='yellow',
    s=200,
    edgecolor='black',
    linewidth=1.5,
    label='Centroids',
    zorder=5,
)
ax3.set_xlabel('Frequency (orders)')
ax3.set_ylabel('Monetary (₳)')
ax3.set_xlim(-0.5, 30)
ax3.set_ylim(0, 1500)
ax3.set_title('Clusters of customers')
ax3.legend(loc='lower right', fontsize=9)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Clustering.png')
plt.show()

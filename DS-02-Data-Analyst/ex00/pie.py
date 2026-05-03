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
    SELECT event_type, COUNT(*) as event_count
    FROM customers
    GROUP BY event_type;
"""

try:
    df = pd.read_sql(query, engine)
except Exception as e:
    print(f"Error running query: {e}")
    sys.exit(1)

plt.pie(df['event_count'], labels=df['event_type'], autopct='%1.1f%%')
plt.savefig('pie.png')
plt.show()

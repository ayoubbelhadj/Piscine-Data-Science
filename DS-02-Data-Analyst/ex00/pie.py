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
    SELECT event_type, COUNT(*) as event_count
    FROM customers
    GROUP BY event_type;
"""

try:
    df = pd.read_sql(query, engine)
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

df.set_index('event_type', inplace=True)

colors = ['#4c72b0', '#55a868', '#c44e52', '#dd8452'] 


fig, ax = plt.subplots(figsize=(8, 8))

df.plot.pie(
    y='event_count', 
    ax=ax, 
    autopct='%1.1f%%',       # Format percentages to 1 decimal place
    startangle=0,            # Start the first slice at 0 degrees
    colors=colors,
    legend=False,            # Hide the default legend
    title=''                 # Remove the default title
)

# Remove the y-axis label for a cleaner look
ax.set_ylabel('')

# Display the chart
plt.tight_layout()
plt.show()
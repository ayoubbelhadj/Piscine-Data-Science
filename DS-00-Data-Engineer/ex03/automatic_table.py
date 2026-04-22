import os
import psycopg2

conn = psycopg2.connect(
    dbname="piscineds",
    user="abelhadj",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

customer_dir = "/customer"

for filename in os.listdir(customer_dir):
    if filename.endswith(".csv"):
        table_name = filename.replace(".csv", "")
        cur.execute(f"DROP TABLE IF EXISTS {table_name};")
        cur.execute(f"""
            CREATE TABLE {table_name} (
                event_time      TIMESTAMP,
                event_type      VARCHAR(50),
                product_id      INTEGER,
                price           NUMERIC(10,2),
                user_id         BIGINT,
                user_session    UUID
            );
        """)
        with open(os.path.join(customer_dir, filename), 'r') as f:
            cur.copy_expert(f"COPY {table_name} FROM STDIN DELIMITER ',' CSV HEADER", f)
        conn.commit()
        print(f"Table {table_name} created and loaded.")

cur.close()
conn.close()
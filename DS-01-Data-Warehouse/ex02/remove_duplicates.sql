CREATE TABLE tmp AS
SELECT event_time, event_type, product_id,
       price, user_id, user_session
FROM (
    SELECT *,
           LAG(event_time) OVER (
               PARTITION BY event_type, product_id, user_id,
                            user_session, price
               ORDER BY event_time
           ) AS prev_time
    FROM customers
) sub
WHERE prev_time IS NULL
   OR ABS(EXTRACT(EPOCH FROM (event_time - prev_time))) > 1;

DROP TABLE customers;
ALTER TABLE tmp RENAME TO customers;

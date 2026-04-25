CREATE TABLE tmp AS
WITH clean_items AS (
    SELECT 
        product_id, 
        MAX(category_id) AS category_id, 
        MAX(category_code) AS category_code, 
        MAX(brand) AS brand
    FROM items
    GROUP BY product_id
)
SELECT 
    c.event_time, 
    c.event_type, 
    c.product_id, 
    c.price, 
    c.user_id, 
    c.user_session,
    i.category_id, 
    i.category_code, 
    i.brand
FROM customers c
LEFT JOIN clean_items i 
    ON c.product_id = i.product_id;

DROP TABLE customers;
ALTER TABLE tmp RENAME TO customers;
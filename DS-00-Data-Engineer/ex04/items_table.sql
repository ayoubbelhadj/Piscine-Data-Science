CREATE TABLE IF NOT EXISTS items (
    product_id      INTEGER,
    category_id     BIGINT,
    category_code   VARCHAR(255),
    brand           VARCHAR(255)
);

COPY items FROM '/items/items.csv'
DELIMITER ',' CSV HEADER;
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    price FLOAT,
    user_id INTEGER
);


CREATE TABLE transactions_stats (
    total_count INTEGER,
    valid_count INTEGER,
    average_price FLOAT,
    min_price FLOAT,
    max_price FLOAT
);

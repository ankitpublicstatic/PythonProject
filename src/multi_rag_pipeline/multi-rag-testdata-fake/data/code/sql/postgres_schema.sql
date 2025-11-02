CREATE TABLE incidents(
    id SERIAL PRIMARY KEY,
    service VARCHAR(100),
    summary TEXT,
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
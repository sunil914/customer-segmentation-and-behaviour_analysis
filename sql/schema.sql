DROP TABLE IF EXISTS customer_sales;

CREATE TABLE customer_sales (
    invoice_no TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL,
    invoice_date TEXT NOT NULL,
    unit_price REAL NOT NULL,
    customer_id TEXT NOT NULL,
    country TEXT NOT NULL,
    revenue REAL NOT NULL
);

CREATE INDEX idx_customer_sales_customer ON customer_sales (customer_id);
CREATE INDEX idx_customer_sales_invoice ON customer_sales (invoice_no);
CREATE INDEX idx_customer_sales_date ON customer_sales (invoice_date);


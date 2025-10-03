CREATE TABLE IF NOT EXISTS products (
  product_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  category VARCHAR(50) NOT NULL,
  price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
  reorder_level INT NOT NULL CHECK (reorder_level >= 0)
);

CREATE TABLE IF NOT EXISTS inventory (
  product_id INT PRIMARY KEY REFERENCES products(product_id) ON DELETE CASCADE,
  quantity_in_stock INT NOT NULL CHECK (quantity_in_stock >= 0),
  warehouse_location VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
  customer_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
  sale_id SERIAL PRIMARY KEY,
  product_id INT NOT NULL REFERENCES products(product_id),
  customer_id INT REFERENCES customers(customer_id),
  quantity_sold INT NOT NULL CHECK (quantity_sold > 0),
  sale_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS suppliers (
  supplier_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  contact_info VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id SERIAL PRIMARY KEY,
  supplier_id INT NOT NULL REFERENCES suppliers(supplier_id),
  product_id INT NOT NULL REFERENCES products(product_id),
  order_date DATE NOT NULL,
  quantity_ordered INT NOT NULL CHECK (quantity_ordered > 0),
  status VARCHAR(20) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

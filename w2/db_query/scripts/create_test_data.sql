-- Create test tables and data for database query tool testing
-- This script creates sample tables with realistic data

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_address TEXT
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);

-- Insert sample users
INSERT INTO users (username, email, full_name, age, is_active) VALUES
('alice', 'alice@example.com', 'Alice Johnson', 28, true),
('bob', 'bob@example.com', 'Bob Smith', 35, true),
('charlie', 'charlie@example.com', 'Charlie Brown', 42, false),
('diana', 'diana@example.com', 'Diana Prince', 29, true),
('eve', 'eve@example.com', 'Eve Williams', 31, true),
('frank', 'frank@example.com', 'Frank Miller', 45, true),
('grace', 'grace@example.com', 'Grace Lee', 27, false),
('henry', 'henry@example.com', 'Henry Davis', 38, true)
ON CONFLICT (username) DO NOTHING;

-- Insert sample products
INSERT INTO products (name, category, price, stock_quantity, description) VALUES
('Laptop Pro 15"', 'Electronics', 1299.99, 50, 'High-performance laptop with 16GB RAM'),
('Wireless Mouse', 'Electronics', 29.99, 200, 'Ergonomic wireless mouse'),
('Mechanical Keyboard', 'Electronics', 89.99, 75, 'RGB backlit mechanical keyboard'),
('Office Chair', 'Furniture', 299.99, 30, 'Ergonomic office chair'),
('Standing Desk', 'Furniture', 599.99, 20, 'Adjustable height standing desk'),
('Coffee Maker', 'Appliances', 79.99, 100, 'Programmable coffee maker'),
('Bluetooth Speaker', 'Electronics', 49.99, 150, 'Portable Bluetooth speaker'),
('Desk Lamp', 'Furniture', 39.99, 80, 'LED desk lamp with adjustable brightness')
ON CONFLICT DO NOTHING;

-- Insert sample orders
INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES
((SELECT id FROM users WHERE username = 'alice'), 1329.98, 'completed', '123 Main St, New York, NY 10001'),
((SELECT id FROM users WHERE username = 'bob'), 419.97, 'shipped', '456 Oak Ave, Los Angeles, CA 90001'),
((SELECT id FROM users WHERE username = 'diana'), 599.99, 'pending', '789 Pine Rd, Chicago, IL 60601'),
((SELECT id FROM users WHERE username = 'eve'), 89.99, 'completed', '321 Elm St, Houston, TX 77001'),
((SELECT id FROM users WHERE username = 'frank'), 1299.99, 'processing', '654 Maple Dr, Phoenix, AZ 85001'),
((SELECT id FROM users WHERE username = 'henry'), 339.98, 'completed', '987 Cedar Ln, Philadelphia, PA 19101')
ON CONFLICT DO NOTHING;

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT 
    o.id as order_id,
    p.id as product_id,
    CASE 
        WHEN o.id = (SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'alice') LIMIT 1)
        THEN 1
        WHEN o.id = (SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'bob') LIMIT 1)
        THEN CASE WHEN p.name = 'Office Chair' THEN 1 WHEN p.name = 'Desk Lamp' THEN 1 ELSE 0 END
        ELSE 1
    END as quantity,
    p.price as unit_price
FROM orders o
CROSS JOIN products p
WHERE 
    (o.id = (SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'alice') LIMIT 1) AND p.name = 'Laptop Pro 15"')
    OR (o.id = (SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'bob') LIMIT 1) AND p.name IN ('Office Chair', 'Desk Lamp'))
    OR (o.id = (SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'diana') LIMIT 1) AND p.name = 'Standing Desk')
    OR (o.id = (SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'eve') LIMIT 1) AND p.name = 'Mechanical Keyboard')
    OR (o.id = (SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'frank') LIMIT 1) AND p.name = 'Laptop Pro 15"')
    OR (o.id = (SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'henry') LIMIT 1) AND p.name = 'Standing Desk')
ON CONFLICT DO NOTHING;

-- Create a view for active users
CREATE OR REPLACE VIEW active_users AS
SELECT id, username, email, full_name, age, created_at
FROM users
WHERE is_active = true;

-- Create a view for order summary
CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.id as order_id,
    u.username,
    u.email,
    o.total_amount,
    o.status,
    o.order_date,
    COUNT(oi.id) as item_count
FROM orders o
JOIN users u ON o.user_id = u.id
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, u.username, u.email, o.total_amount, o.status, o.order_date;

-- Display summary
SELECT 'Tables created and data inserted successfully!' as message;
SELECT COUNT(*) as user_count FROM users;
SELECT COUNT(*) as product_count FROM products;
SELECT COUNT(*) as order_count FROM orders;
SELECT COUNT(*) as order_item_count FROM order_items;


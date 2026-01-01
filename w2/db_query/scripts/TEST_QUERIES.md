# 测试查询示例

本文档包含一些示例 SQL 查询，可用于测试数据库查询工具的功能。

## 数据库说明

已为以下数据库创建了测试数据：
- **local-postgres** (连接到 `postgres` 数据库)
- **my-database** (连接到 `ronny` 数据库)

## 创建的表结构

### users (用户表)
- id (主键)
- username (用户名，唯一)
- email (邮箱，唯一)
- full_name (全名)
- age (年龄)
- created_at (创建时间)
- is_active (是否激活)

### products (产品表)
- id (主键)
- name (产品名称)
- category (类别)
- price (价格)
- stock_quantity (库存数量)
- description (描述)
- created_at (创建时间)

### orders (订单表)
- id (主键)
- user_id (用户ID，外键)
- total_amount (总金额)
- status (状态：pending, processing, shipped, completed)
- order_date (订单日期)
- shipping_address (配送地址)

### order_items (订单项表)
- id (主键)
- order_id (订单ID，外键)
- product_id (产品ID，外键)
- quantity (数量)
- unit_price (单价)

### Views (视图)
- **active_users**: 活跃用户视图
- **order_summary**: 订单摘要视图

## 示例查询

### 1. 基础查询

```sql
-- 查询所有用户
SELECT * FROM users;

-- 查询所有产品
SELECT * FROM products;

-- 查询前 5 个用户
SELECT id, username, email, full_name 
FROM users 
LIMIT 5;
```

### 2. 条件查询

```sql
-- 查询年龄大于 30 的用户
SELECT username, full_name, age 
FROM users 
WHERE age > 30;

-- 查询激活的用户
SELECT username, email, full_name 
FROM users 
WHERE is_active = true;

-- 查询电子产品
SELECT name, price, stock_quantity 
FROM products 
WHERE category = 'Electronics';
```

### 3. 排序查询

```sql
-- 按价格降序查询产品
SELECT name, category, price 
FROM products 
ORDER BY price DESC;

-- 按年龄升序查询用户
SELECT username, full_name, age 
FROM users 
ORDER BY age ASC;
```

### 4. 聚合查询

```sql
-- 统计用户数量
SELECT COUNT(*) as total_users FROM users;

-- 计算平均年龄
SELECT AVG(age) as average_age FROM users;

-- 按类别统计产品数量
SELECT category, COUNT(*) as product_count 
FROM products 
GROUP BY category;

-- 计算每个用户的订单总金额
SELECT u.username, SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.username;
```

### 5. JOIN 查询

```sql
-- 查询订单及用户信息
SELECT o.id, u.username, u.email, o.total_amount, o.status
FROM orders o
JOIN users u ON o.user_id = u.id;

-- 查询订单详情（包含产品和订单项）
SELECT 
    o.id as order_id,
    u.username,
    p.name as product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) as subtotal
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

### 6. 复杂查询

```sql
-- 查询每个类别最贵的产品
SELECT category, name, price
FROM products p1
WHERE price = (
    SELECT MAX(price) 
    FROM products p2 
    WHERE p2.category = p1.category
)
ORDER BY category;

-- 查询有订单的用户及其订单数量
SELECT 
    u.username,
    u.email,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.total_amount), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username, u.email
ORDER BY order_count DESC;
```

### 7. 视图查询

```sql
-- 查询活跃用户视图
SELECT * FROM active_users;

-- 查询订单摘要视图
SELECT * FROM order_summary 
WHERE status = 'completed';
```

### 8. 测试 LIMIT 功能

```sql
-- 测试自动添加 LIMIT（如果不指定，会自动添加 LIMIT 1000）
SELECT * FROM users;

-- 明确指定 LIMIT
SELECT * FROM products LIMIT 3;

-- 测试大结果集（会被限制在 1000 行）
SELECT * FROM order_items;
```

## 自然语言查询示例

可以使用以下自然语言查询来测试自然语言转 SQL 功能：

### 英文
- "Show me all active users"
- "List all products in the Electronics category"
- "Find orders with total amount greater than 500"
- "Show users who have placed orders"
- "Get the most expensive product in each category"

### 中文
- "查询所有激活的用户"
- "显示所有电子产品"
- "查找金额大于 500 的订单"
- "显示有订单的用户"
- "查询每个类别最贵的产品"

## 测试导出功能

执行以下查询来测试 CSV/JSON 导出：

```sql
-- 导出用户列表
SELECT id, username, email, full_name, age, is_active 
FROM users;

-- 导出产品列表
SELECT name, category, price, stock_quantity 
FROM products 
ORDER BY price DESC;

-- 导出订单详情
SELECT 
    o.id,
    u.username,
    o.total_amount,
    o.status,
    o.order_date
FROM orders o
JOIN users u ON o.user_id = u.id;
```

## 数据统计

当前测试数据包含：
- **8 个用户**（5 个激活，3 个未激活）
- **8 个产品**（Electronics, Furniture, Appliances 类别）
- **6 个订单**（不同状态）
- **7 个订单项**
- **2 个视图**（active_users, order_summary）

## 清理数据（如果需要）

如果需要清理测试数据，可以运行：

```sql
-- 删除视图
DROP VIEW IF EXISTS order_summary;
DROP VIEW IF EXISTS active_users;

-- 删除表（注意顺序，因为有外键约束）
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
```


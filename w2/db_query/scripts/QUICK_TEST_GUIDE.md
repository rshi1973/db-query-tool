# 快速测试指南

## ✅ 测试数据已创建

已成功为以下数据库创建了测试表和测试数据：

### 数据库连接

1. **local-postgres** → `postgresql://ronny@localhost:5432/postgres`
2. **my-database** → `postgresql://ronny@localhost:5432/ronny`

### 创建的表

- ✅ **users** - 8 个用户记录
- ✅ **products** - 8 个产品记录
- ✅ **orders** - 6 个订单记录
- ✅ **order_items** - 7 个订单项记录
- ✅ **active_users** - 视图（活跃用户）
- ✅ **order_summary** - 视图（订单摘要）

## 🧪 快速测试查询

### 1. 基础查询测试

```sql
-- 查询所有用户
SELECT * FROM users;

-- 查询所有产品
SELECT * FROM products;

-- 查询前 3 个用户
SELECT username, email, full_name FROM users LIMIT 3;
```

### 2. 条件查询测试

```sql
-- 查询激活的用户
SELECT username, email, full_name 
FROM users 
WHERE is_active = true;

-- 查询电子产品
SELECT name, price, category 
FROM products 
WHERE category = 'Electronics';

-- 查询价格大于 100 的产品
SELECT name, price 
FROM products 
WHERE price > 100 
ORDER BY price DESC;
```

### 3. JOIN 查询测试

```sql
-- 查询订单及用户信息
SELECT 
    o.id as order_id,
    u.username,
    u.email,
    o.total_amount,
    o.status
FROM orders o
JOIN users u ON o.user_id = u.id;

-- 查询订单详情（包含产品信息）
SELECT 
    o.id as order_id,
    u.username,
    p.name as product_name,
    oi.quantity,
    oi.unit_price
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

### 4. 聚合查询测试

```sql
-- 统计每个类别的产品数量
SELECT category, COUNT(*) as count 
FROM products 
GROUP BY category;

-- 计算平均年龄
SELECT AVG(age) as average_age FROM users;

-- 计算每个用户的订单总金额
SELECT 
    u.username,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.total_amount), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.username
ORDER BY total_spent DESC;
```

### 5. 视图查询测试

```sql
-- 查询活跃用户视图
SELECT * FROM active_users;

-- 查询订单摘要视图
SELECT * FROM order_summary 
WHERE status = 'completed';
```

## 🤖 自然语言查询测试

### 英文示例

- "Show me all active users"
- "List all products in the Electronics category"
- "Find orders with total amount greater than 500"
- "Show users who have placed orders"
- "Get products sorted by price"

### 中文示例

- "查询所有激活的用户"
- "显示所有电子产品"
- "查找金额大于 500 的订单"
- "显示有订单的用户"
- "按价格排序显示产品"

## 📊 测试数据概览

### Users (用户表)
- **8 个用户**：alice, bob, charlie, diana, eve, frank, grace, henry
- **字段**：id, username, email, full_name, age, created_at, is_active

### Products (产品表)
- **8 个产品**：Laptop, Mouse, Keyboard, Chair, Desk, Coffee Maker, Speaker, Lamp
- **类别**：Electronics, Furniture, Appliances
- **价格范围**：$29.99 - $1299.99

### Orders (订单表)
- **6 个订单**
- **状态**：pending, processing, shipped, completed
- **总金额范围**：$89.99 - $1329.98

### Order Items (订单项表)
- **7 个订单项**
- **关联**：订单和产品的关联关系

## 🔍 在前端测试

### 步骤 1: 查看数据库元数据

1. 访问前端：http://localhost:5173
2. 点击数据库列表中的 **local-postgres** 或 **my-database**
3. 应该看到以下表：
   - users
   - products
   - orders
   - order_items
4. 还有视图：
   - active_users
   - order_summary

### 步骤 2: 执行查询

在查询页面执行上述 SQL 查询示例。

### 步骤 3: 测试自然语言

1. 切换到 "NATURAL LANGUAGE" 标签页
2. 输入："查询所有激活的用户"
3. 点击 "GENERATE SQL"
4. 查看生成的 SQL 并执行

### 步骤 4: 测试导出

1. 执行一个查询（例如：`SELECT * FROM users`）
2. 点击 "EXPORT CSV" 或 "EXPORT JSON"
3. 验证文件是否正确下载

## 📝 数据验证查询

运行以下查询验证数据：

```sql
-- 验证用户数据
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(*) as active_users FROM users WHERE is_active = true;

-- 验证产品数据
SELECT COUNT(*) as total_products FROM products;
SELECT category, COUNT(*) as count FROM products GROUP BY category;

-- 验证订单数据
SELECT COUNT(*) as total_orders FROM orders;
SELECT status, COUNT(*) as count FROM orders GROUP BY status;
```

## 🎯 测试检查清单

- [ ] 查看数据库元数据（表和视图）
- [ ] 执行基础 SELECT 查询
- [ ] 执行带 WHERE 条件的查询
- [ ] 执行 JOIN 查询
- [ ] 执行聚合查询（GROUP BY, COUNT, SUM）
- [ ] 测试自然语言转 SQL（英文）
- [ ] 测试自然语言转 SQL（中文）
- [ ] 测试 CSV 导出
- [ ] 测试 JSON 导出
- [ ] 测试查询历史功能

---

**提示**：所有测试数据已创建完成，可以立即开始测试各种功能！


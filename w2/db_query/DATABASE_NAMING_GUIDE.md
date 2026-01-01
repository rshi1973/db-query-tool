# 数据库连接命名指南

本文档说明系统中可以添加的数据库连接名称和格式。

## 支持的数据库类型

系统目前支持以下两种数据库类型：

1. **PostgreSQL** (`postgresql`)
2. **MySQL** (`mysql`)

## 数据库连接名称规范

### 命名规则

- **长度限制**: 最大 50 个字符
- **唯一性**: 每个连接名称必须唯一（用作主键）
- **建议字符**: 字母、数字、连字符 (`-`)、下划线 (`_`)
- **大小写**: 区分大小写（`mydb` 和 `MyDB` 是不同的名称）

### 命名建议

使用有意义的、描述性的名称，便于识别和管理：

✅ **推荐的命名格式**：
- 使用小写字母和连字符：`production-db`, `staging-postgres`
- 使用描述性前缀：`pg-production`, `mysql-dev`, `pg-analytics`
- 包含环境信息：`dev-postgres`, `prod-mysql`, `test-db`

✅ **有效的名称示例**：
```
my-database
production-postgres
staging-mysql
test-db
pg-analytics
mysql-backup
local-postgres
remote-mysql
db_query_production
analytics-db-01
```

❌ **不推荐的命名**：
- 纯数字：`123`, `456`（可能混淆）
- 特殊字符：`my@db`, `test#db`（可能有问题）
- 空格：`my database`（应使用连字符或下划线）

## 数据库连接 URL 格式

### PostgreSQL 连接 URL

**格式**：
```
postgresql://[用户名]:[密码]@[主机]:[端口]/[数据库名]
```

**示例**：
```
# 本地 PostgreSQL
postgresql://postgres:password@localhost:5432/mydb

# 远程 PostgreSQL（带端口）
postgresql://user:pass@example.com:5432/production

# PostgreSQL（默认端口 5432）
postgresql://postgres:password@localhost/mydb

# 使用 postgres:// 前缀（也被支持）
postgres://postgres:password@localhost:5432/mydb
```

**支持的 URL 前缀**：
- `postgresql://`
- `postgres://`

### MySQL 连接 URL

**格式**：
```
mysql://[用户名]:[密码]@[主机]:[端口]/[数据库名]
```

**示例**：
```
# 本地 MySQL
mysql://root:password@localhost:3306/mydb

# 远程 MySQL
mysql://user:pass@mysql.example.com:3306/production

# MySQL（默认端口 3306）
mysql://root:password@localhost/mydb

# 使用 PyMySQL 驱动（自动处理）
mysql://root:password@localhost:3306/mydb
```

**支持的 URL 前缀**：
- `mysql://`
- `mysql+pymysql://`
- `mysql+aiomysql://`

## 完整的添加示例

### 示例 1: 本地 PostgreSQL 数据库

**连接名称**: `local-postgres`  
**数据库类型**: `postgresql`  
**连接 URL**: `postgresql://postgres:password@localhost:5432/mydb`  
**描述**: `本地开发 PostgreSQL 数据库`

### 示例 2: 生产环境 MySQL

**连接名称**: `prod-mysql`  
**数据库类型**: `mysql`  
**连接 URL**: `mysql://admin:securepass@prod-db.example.com:3306/production`  
**描述**: `生产环境 MySQL 数据库`

### 示例 3: 测试环境 PostgreSQL

**连接名称**: `test-pg`  
**数据库类型**: `postgresql`  
**连接 URL**: `postgresql://testuser:testpass@test.example.com:5432/testdb`  
**描述**: `测试环境数据库`

### 示例 4: 分析数据库

**连接名称**: `analytics-warehouse`  
**数据库类型**: `postgresql`  
**连接 URL**: `postgresql://analytics:readonly@warehouse.example.com:5432/analytics`  
**描述**: `数据分析仓库`

## 通过 API 添加数据库连接

### 使用 curl

```bash
# 添加 PostgreSQL 连接
curl -X PUT "http://localhost:8000/api/v1/dbs/local-postgres" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "postgresql://postgres:password@localhost:5432/mydb",
    "dbType": "postgresql",
    "description": "本地 PostgreSQL 数据库"
  }'

# 添加 MySQL 连接
curl -X PUT "http://localhost:8000/api/v1/dbs/prod-mysql" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "mysql://root:password@localhost:3306/production",
    "dbType": "mysql",
    "description": "生产环境 MySQL"
  }'
```

### 使用前端界面

1. 访问前端：http://localhost:5173
2. 点击 "Add Database" 或 "添加数据库"
3. 填写表单：
   - **Name**: 输入唯一名称（如 `local-postgres`）
   - **URL**: 输入连接 URL
   - **Database Type**: 选择 `postgresql` 或 `mysql`
   - **Description**: （可选）输入描述
4. 点击 "Save" 保存

## 数据库类型自动检测

如果不指定 `dbType`，系统会根据 URL 的前缀自动检测：

- `postgresql://` 或 `postgres://` → 自动识别为 PostgreSQL
- `mysql://` → 自动识别为 MySQL

**示例**：
```json
{
  "url": "postgresql://user:pass@host/db"
  // dbType 会自动设置为 "postgresql"
}
```

## 常见数据库连接示例

### 本地开发环境

```
名称: local-dev
类型: postgresql
URL: postgresql://postgres:postgres@localhost:5432/devdb
```

### Docker 容器中的数据库

```
名称: docker-postgres
类型: postgresql
URL: postgresql://postgres:postgres@localhost:5433/docker_db
```

### 云数据库（AWS RDS）

```
名称: aws-rds-prod
类型: postgresql
URL: postgresql://admin:password@prod-db.xxxxx.us-east-1.rds.amazonaws.com:5432/production
```

### 云数据库（MySQL）

```
名称: cloud-mysql
类型: mysql
URL: mysql://user:password@mysql.cloud.example.com:3306/clouddb
```

## 注意事项

1. **安全性**：URL 中包含密码，确保妥善保管 `.env` 文件和数据库连接信息
2. **连接测试**：添加连接时，系统会自动测试连接是否可用
3. **名称唯一性**：如果名称已存在，会更新现有连接（而不是创建新连接）
4. **URL 格式**：确保 URL 格式正确，否则连接会失败
5. **端口号**：如果不指定端口，使用数据库默认端口（PostgreSQL: 5432, MySQL: 3306）

## 查看已添加的数据库

### 通过 API

```bash
curl http://localhost:8000/api/v1/dbs
```

### 通过前端

访问数据库列表页面查看所有已添加的连接。

---

**提示**：选择一个清晰、描述性的名称可以让你的数据库连接更容易管理和识别！


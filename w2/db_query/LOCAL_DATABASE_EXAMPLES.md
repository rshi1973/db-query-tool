# 本地数据库连接示例（基于你的系统配置）

根据系统检测，你的 Mac 上运行着 **PostgreSQL 16.3**。以下是可以在前端界面使用的数据库连接配置。

## 🔍 系统检测结果

- ✅ **PostgreSQL**: 已安装并运行中（端口 5432）
- ✅ **版本**: PostgreSQL 16.3 (Homebrew)
- ❌ **MySQL**: 未安装/未运行

## 📝 推荐的数据库连接配置

### 示例 1: 连接到默认 PostgreSQL 数据库

**在 Add Database 界面填写：**

```
Name（名称）: local-postgres
URL: postgresql://ronny@localhost:5432/postgres
Database Type: postgresql
Description: 本地 PostgreSQL 默认数据库
```

**如果设置了密码，使用：**
```
URL: postgresql://ronny:your_password@localhost:5432/postgres
```

### 示例 2: 连接到你的用户数据库

**在 Add Database 界面填写：**

```
Name（名称）: my-postgres-db
URL: postgresql://ronny@localhost:5432/ronny
Database Type: postgresql
Description: 本地用户数据库
```

**如果设置了密码：**
```
URL: postgresql://ronny:your_password@localhost:5432/ronny
```

### 示例 3: 无密码连接（如果配置了信任认证）

**在 Add Database 界面填写：**

```
Name（名称）: local-dev
URL: postgresql://ronny@localhost:5432/postgres
Database Type: postgresql
Description: 本地开发数据库（无密码）
```

## 🔐 常见认证方式

### 方式 1: 信任认证（无需密码）

如果你的 `pg_hba.conf` 配置为信任认证，可以直接使用：

```
postgresql://ronny@localhost:5432/postgres
```

### 方式 2: 密码认证

如果设置了密码：

```
postgresql://ronny:your_password@localhost:5432/postgres
```

### 方式 3: 使用 postgres 用户

如果使用默认的 postgres 超级用户：

```
postgresql://postgres:your_password@localhost:5432/postgres
```

## 📋 完整表单填写示例

### 场景：连接到默认数据库

在 "Add Database" 表单中：

| 字段 | 值 |
|------|-----|
| **Name** | `local-postgres` |
| **URL** | `postgresql://ronny@localhost:5432/postgres` |
| **Database Type** | `postgresql` |
| **Description** | `本地 PostgreSQL 数据库` |

### 场景：连接到特定数据库

假设你有一个名为 `mydb` 的数据库：

| 字段 | 值 |
|------|-----|
| **Name** | `my-app-db` |
| **URL** | `postgresql://ronny@localhost:5432/mydb` |
| **Database Type** | `postgresql` |
| **Description** | `应用程序数据库` |

## 🔍 如何查找可用的数据库

### 方法 1: 使用 psql 命令行

```bash
# 列出所有数据库
psql -U ronny -l

# 或使用 postgres 用户
psql -U postgres -l
```

### 方法 2: 直接连接测试

```bash
# 测试连接
psql -U ronny -d postgres -c "SELECT current_database();"

# 如果成功，说明可以使用：
# postgresql://ronny@localhost:5432/postgres
```

## ⚠️ 如果连接失败

### 问题 1: 认证失败

**解决方案：**

1. **检查是否需要密码**：
   ```bash
   # 尝试连接，看是否需要密码
   psql -U ronny -d postgres
   ```

2. **如果提示密码**，在 URL 中包含密码：
   ```
   postgresql://ronny:your_password@localhost:5432/postgres
   ```

### 问题 2: 数据库不存在

**解决方案：**

1. **列出所有数据库**：
   ```bash
   psql -U ronny -l
   ```

2. **使用存在的数据库名称**替换 URL 中的数据库名

### 问题 3: 用户不存在

**解决方案：**

1. **使用 postgres 超级用户**：
   ```
   postgresql://postgres:password@localhost:5432/postgres
   ```

2. **或创建新用户**：
   ```sql
   CREATE USER ronny WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE postgres TO ronny;
   ```

## 🧪 快速测试连接

在添加数据库之前，可以先测试连接是否可用：

```bash
# 测试连接
psql "postgresql://ronny@localhost:5432/postgres" -c "SELECT version();"

# 如果成功，说明 URL 格式正确
```

## 📝 推荐的命名方案

根据你的使用场景，可以使用以下命名：

| 用途 | Name 示例 | URL 示例 |
|------|-----------|----------|
| 默认数据库 | `local-postgres` | `postgresql://ronny@localhost:5432/postgres` |
| 开发环境 | `dev-postgres` | `postgresql://ronny@localhost:5432/devdb` |
| 测试环境 | `test-postgres` | `postgresql://ronny@localhost:5432/testdb` |
| 用户数据库 | `my-db` | `postgresql://ronny@localhost:5432/ronny` |

## 🚀 立即尝试

**最简单的开始方式**：

1. 在前端界面打开 "Add Database"
2. 填写以下信息：

   ```
   Name: local-postgres
   URL: postgresql://ronny@localhost:5432/postgres
   Database Type: postgresql (会自动检测)
   Description: 本地 PostgreSQL (可选)
   ```

3. 点击 "Save"
4. 如果连接失败，根据错误信息调整 URL（可能需要添加密码）

## 💡 提示

- 如果本地 PostgreSQL 配置为信任认证，可以直接使用 `postgresql://ronny@localhost:5432/postgres`
- 如果设置了密码，记得在 URL 中包含：`postgresql://ronny:password@localhost:5432/postgres`
- 数据库类型会自动从 URL 检测，但建议明确选择 `postgresql`
- 名称（Name）可以是任何你喜欢的唯一标识符，建议使用描述性的名称

---

**注意**：URL 中的密码会以明文形式存储，请确保妥善保管你的数据库文件（位于 `~/.db_query/db_query.db`）


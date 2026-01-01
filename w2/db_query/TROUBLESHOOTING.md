# 故障排查指南

## 数据库字段缺失错误修复

### 问题：`no such column: databaseconnections.db_type`

如果遇到此错误，请按以下步骤操作：

### 步骤 1: 确认迁移已运行

```bash
cd /Users/ronny/geektime-bootcamp-ai/w2/db_query/backend
uv run alembic current
```

应该显示：`002 (head)`

### 步骤 2: 如果迁移未运行，执行迁移

```bash
cd /Users/ronny/geektime-bootcamp-ai/w2/db_query/backend
uv run alembic upgrade head
```

### 步骤 3: 验证数据库结构

```bash
sqlite3 ~/.db_query/db_query.db ".schema databaseconnections"
```

应该看到 `db_type VARCHAR(20) DEFAULT 'postgresql' NOT NULL` 在字段列表中。

### 步骤 4: 重启后端服务

**重要**：迁移后必须重启后端服务才能生效！

```bash
# 停止当前运行的后端（Ctrl+C）

# 然后重新启动
cd /Users/ronny/geektime-bootcamp-ai/w2/db_query
./start.sh

# 或
make dev

# 或手动启动
cd backend && uv run uvicorn app.main:app --reload --port 8000
```

### 步骤 5: 验证修复

```bash
# 检查 API 是否正常
curl http://localhost:8000/api/v1/dbs

# 应该返回空数组 [] 或数据库列表，而不是错误
```

## 如果问题仍然存在

### 方案 1: 清除数据库重新开始（会丢失所有数据）

```bash
# 备份现有数据（如果需要）
cp ~/.db_query/db_query.db ~/.db_query/db_query.db.backup

# 删除数据库文件
rm ~/.db_query/db_query.db

# 重新运行迁移
cd /Users/ronny/geektime-bootcamp-ai/w2/db_query/backend
uv run alembic upgrade head

# 重启服务
```

### 方案 2: 手动修复数据库（保留现有数据）

如果数据库中有重要数据，可以手动添加字段：

```bash
sqlite3 ~/.db_query/db_query.db << EOF
-- 添加 db_type 字段
ALTER TABLE databaseconnections ADD COLUMN db_type VARCHAR(20) DEFAULT 'postgresql' NOT NULL;

-- 验证
.schema databaseconnections
EOF
```

然后重启后端服务。

## 常见问题

### Q: 迁移运行了但还是报错？

A: 确保：
1. 后端服务已完全重启
2. 没有多个后端进程在运行
3. 数据库文件路径正确（检查 `~/.db_query/db_query.db`）

### Q: 如何检查数据库版本？

```bash
cd backend
uv run alembic current
sqlite3 ~/.db_query/db_query.db "SELECT * FROM alembic_version;"
```

### Q: 如何查看所有迁移历史？

```bash
cd backend
uv run alembic history
```


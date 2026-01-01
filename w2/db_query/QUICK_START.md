# 快速启动指南 - 人工测试验证

本文档介绍如何启动 Database Query Tool 项目并进行人工测试验证。

## 📋 前置准备

### 1. 系统要求

- **Python 3.12+** 
- **Node.js 18+** (LTS 推荐)
- **uv** 包管理器（推荐）或 pip
- **npm** 或 yarn
- **PostgreSQL 或 MySQL** 数据库（用于测试连接）

### 2. 检查环境

```bash
# 检查 Python 版本
python3 --version  # 需要 3.12+

# 检查 Node.js 版本
node --version  # 需要 18+

# 检查是否安装 uv（可选，推荐）
uv --version
```

## 🚀 快速启动（推荐方式）

### 方式一：使用启动脚本（最简单）

```bash
# 1. 进入项目目录
cd /Users/ronny/geektime-bootcamp-ai/w2/db_query

# 2. 首次运行需要配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，添加你的 GEMINI_API_KEY

# 3. 安装依赖（如果还没安装）
make install

# 4. 运行数据库迁移
make db-upgrade

# 5. 启动项目（同时启动前后端）
./start.sh
```

启动后会自动打开：
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **前端界面**: http://localhost:5173

### 方式二：使用 Makefile

```bash
# 1. 完整设置（首次运行）
make setup

# 2. 配置环境变量
# 编辑 backend/.env，添加 GEMINI_API_KEY

# 3. 启动开发服务器
make dev
```

### 方式三：分别启动前后端

**终端 1 - 启动后端：**
```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

**终端 2 - 启动前端：**
```bash
cd frontend
npm run dev
```

## ⚙️ 环境配置

### 后端配置（backend/.env）

```bash
# 复制示例文件
cp backend/.env.example backend/.env

# 编辑 .env 文件，添加以下内容：
GEMINI_API_KEY=your-gemini-api-key-here
DB_QUERY_DATA_DIR=~/.db_query
LOG_LEVEL=INFO
```

**必需配置：**
- `GEMINI_API_KEY`: Google Gemini API 密钥（自然语言转 SQL 功能必需，从 https://makersuite.google.com/app/apikey 获取）

**可选配置：**
- `DB_QUERY_DATA_DIR`: SQLite 数据库存储目录（默认：`~/.db_query`）
- `LOG_LEVEL`: 日志级别（默认：`INFO`）
- `LLM_RATE_LIMIT_MAX_REQUESTS`: 限流最大请求数（默认：10）
- `LLM_RATE_LIMIT_WINDOW_SECONDS`: 限流时间窗口（默认：60秒）

### 前端配置（可选）

前端默认使用 `http://localhost:8000` 作为 API 地址。如需修改：

```bash
cd frontend
cp .env.local.example .env.local
# 编辑 .env.local，设置 VITE_API_BASE_URL
```

## ✅ 验证启动成功

### 1. 检查后端服务

```bash
# 方式一：使用 Makefile
make health

# 方式二：使用 curl
curl http://localhost:8000/health

# 预期输出：
# {"status":"healthy","version":"1.0.0"}
```

### 2. 访问 API 文档

打开浏览器访问：http://localhost:8000/docs

应该看到 Swagger UI 界面，显示所有可用的 API 端点。

### 3. 检查前端服务

打开浏览器访问：http://localhost:5173

应该看到 Database Query Tool 的前端界面。

## 🧪 人工测试验证流程

### Phase 1: 基础功能测试（US1 + US2）

#### 测试 1.1: 添加数据库连接

1. 在前端点击 "Add Database" 或访问数据库列表页面
2. 填写连接信息：
   - **Name**: `test-postgres`（唯一标识）
   - **URL**: `postgresql://user:password@localhost:5432/mydb`
   - **Database Type**: PostgreSQL 或 MySQL
   - **Description**: 测试数据库（可选）
3. 点击 "Save"
4. 验证：连接出现在数据库列表中

**测试 PostgreSQL 连接：**
```
postgresql://postgres:password@localhost:5432/postgres
```

**测试 MySQL 连接：**
```
mysql://root:password@localhost:3306/testdb
```

#### 测试 1.2: 查看数据库元数据

1. 在数据库列表中点击已添加的数据库名称
2. 验证：
   - 显示数据库的 schema 树形结构
   - 可以看到表（Tables）和视图（Views）
   - 点击表名可以展开查看列信息
   - 显示列的数据类型、是否可空、是否主键等信息

#### 测试 1.3: 执行 SQL 查询

1. 在查询页面选择数据库
2. 在 SQL 编辑器中输入：
   ```sql
   SELECT * FROM users LIMIT 10
   ```
3. 点击 "EXECUTE" 按钮
4. 验证：
   - 显示查询结果表格
   - 显示执行时间（毫秒）
   - 显示返回行数
   - 查询历史面板显示本次查询记录

#### 测试 1.4: SQL 验证

测试 SQL 安全限制：

```sql
-- 应该被拒绝
INSERT INTO users (name) VALUES ('test');  -- ❌ 只允许 SELECT
UPDATE users SET name = 'test';            -- ❌ 只允许 SELECT
DELETE FROM users WHERE id = 1;            -- ❌ 只允许 SELECT
DROP TABLE users;                          -- ❌ 只允许 SELECT

-- 应该通过
SELECT * FROM users;                       -- ✅ 允许
SELECT id, name FROM users WHERE id = 1;  -- ✅ 允许
```

验证：非 SELECT 语句应该返回错误提示。

#### 测试 1.5: 自动 LIMIT 注入

```sql
-- 输入（没有 LIMIT）
SELECT * FROM users

-- 执行后应该自动添加 LIMIT 1000
-- 实际执行：SELECT * FROM users LIMIT 1000
```

### Phase 2: 自然语言功能测试（US3）

#### 测试 2.1: 自然语言转 SQL（英文）

1. 切换到 "NATURAL LANGUAGE" 标签页
2. 输入自然语言查询：
   ```
   Show me all users who signed up this month
   ```
3. 点击 "GENERATE SQL" 或按 Cmd/Ctrl + Enter
4. 验证：
   - 显示加载状态
   - 自动切换到 "MANUAL SQL" 标签页
   - SQL 编辑器显示生成的 SQL
   - 可以编辑生成的 SQL
   - 点击执行可以运行查询

#### 测试 2.2: 自然语言转 SQL（中文）

1. 在 "NATURAL LANGUAGE" 标签页输入：
   ```
   查询所有用户的信息
   ```
2. 点击 "GENERATE SQL"
3. 验证：生成正确的 SQL 查询语句

#### 测试 2.3: 限流测试

1. 快速连续发送 11 次自然语言请求（默认限制 10 次/分钟）
2. 验证：
   - 前 10 次请求成功
   - 第 11 次请求返回 429 错误
   - 错误信息显示 "Rate limit exceeded"
   - 显示重试时间（Retry-After）

#### 测试 2.4: 错误处理

1. 测试无效的自然语言输入
2. 测试 Gemini API 失败的情况（临时断网或 API key 无效）
3. 验证：显示友好的错误提示信息

### Phase 3: 导出功能测试（US4）

#### 测试 3.1: CSV 导出

1. 执行一个查询，获得结果
2. 点击 "EXPORT CSV" 按钮
3. 验证：
   - 文件自动下载
   - 文件名格式：`{数据库名}_{时间戳}.csv`
   - 打开 CSV 文件，数据格式正确
   - 包含逗号、引号的值被正确转义

#### 测试 3.2: JSON 导出

1. 执行一个查询，获得结果
2. 点击 "EXPORT JSON" 按钮
3. 验证：
   - 文件自动下载
   - 文件名格式：`{数据库名}_{时间戳}.json`
   - 打开 JSON 文件，格式正确（格式化输出）
   - 数据完整准确

#### 测试 3.3: 大数据集警告

1. 执行一个返回超过 10,000 行的查询（或模拟）
2. 点击导出按钮（CSV 或 JSON）
3. 验证：
   - 显示警告对话框
   - 显示准确的行数
   - 警告内存消耗和处理时间
   - 可以选择继续或取消

#### 测试 3.4: 空结果导出

1. 执行返回空结果的查询
2. 尝试点击导出按钮
3. 验证：
   - 导出按钮被禁用，或
   - 显示"没有数据可导出"的提示

### Phase 4: 界面和用户体验测试

#### 测试 4.1: Tab 切换

1. 在 "MANUAL SQL" 标签页输入一些 SQL
2. 切换到 "NATURAL LANGUAGE" 标签页
3. 再切换回 "MANUAL SQL"
4. 验证：SQL 内容被保留

#### 测试 4.2: 查询历史

1. 执行多个不同的查询
2. 查看查询历史面板
3. 验证：
   - 显示最近的查询（最多 50 条）
   - 显示执行时间、行数、成功/失败状态
   - 可以点击历史记录重新执行

#### 测试 4.3: 加载状态

1. 执行一个耗时查询
2. 验证：显示加载指示器
3. 执行自然语言生成
4. 验证：显示加载状态

#### 测试 4.4: 响应式设计

1. 调整浏览器窗口大小
2. 验证：界面布局适应不同屏幕尺寸

## 🔍 故障排查

### 后端无法启动

**问题**: `ModuleNotFoundError` 或 `Command not found: uvicorn`

**解决**:
```bash
# 确保依赖已安装
cd backend
uv sync --extra dev
# 或
pip install -e ".[dev]"
```

**问题**: `GEMINI_API_KEY` 未设置

**解决**:
```bash
# 检查 .env 文件
cat backend/.env
# 确保包含 GEMINI_API_KEY=your-gemini-api-key-here
```

**问题**: 端口 8000 已被占用

**解决**:
```bash
# 查找占用端口的进程
lsof -i :8000
# 终止进程或修改端口
```

### 前端无法启动

**问题**: `npm: command not found`

**解决**:
```bash
# 安装 Node.js 和 npm
# macOS: brew install node
# 或从 https://nodejs.org 下载安装
```

**问题**: `Cannot find module`

**解决**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**问题**: 无法连接到后端 API

**解决**:
1. 确认后端服务正在运行（`make health`）
2. 检查前端 `.env.local` 中的 `VITE_API_BASE_URL`
3. 检查浏览器控制台的错误信息
4. 检查后端 CORS 配置（应该允许所有来源）

### 数据库连接失败

**问题**: 无法连接到 PostgreSQL/MySQL

**解决**:
1. 验证数据库服务正在运行
2. 检查连接 URL 格式：
   - PostgreSQL: `postgresql://user:password@host:port/database`
   - MySQL: `mysql://user:password@host:port/database`
3. 验证用户名、密码、主机、端口是否正确
4. 检查防火墙和网络设置

### 自然语言功能不工作

**问题**: 生成 SQL 失败

**解决**:
1. 检查 `GEMINI_API_KEY` 是否有效（从 https://makersuite.google.com/app/apikey 获取）
2. 检查网络连接
3. 查看后端日志中的错误信息
4. 确认数据库元数据已刷新（点击 Refresh 按钮）

## 📊 测试检查清单

打印此清单并在测试时勾选：

### 基础功能（US1 + US2）
- [ ] 添加 PostgreSQL 数据库连接
- [ ] 添加 MySQL 数据库连接
- [ ] 查看数据库元数据（表、列）
- [ ] 执行 SELECT 查询
- [ ] SQL 验证（拒绝非 SELECT）
- [ ] 自动 LIMIT 注入
- [ ] 查询历史记录

### 自然语言功能（US3）
- [ ] 英文自然语言转 SQL
- [ ] 中文自然语言转 SQL
- [ ] 生成的 SQL 可以编辑
- [ ] 限流功能（429 错误）
- [ ] 错误处理

### 导出功能（US4）
- [ ] CSV 导出
- [ ] JSON 导出
- [ ] 大数据集警告
- [ ] 空结果处理

### 用户体验
- [ ] Tab 切换保留内容
- [ ] 加载状态显示
- [ ] 错误提示友好
- [ ] 响应式布局

## 📝 测试报告模板

完成测试后，可以记录以下信息：

```
测试日期: __________
测试人员: __________
测试环境: macOS/Windows/Linux (版本: _____)

后端版本: __________
前端版本: __________

测试结果:
✅ 通过的功能: __________
❌ 失败的功能: __________
⚠️ 发现的问题: __________

备注: __________
```

## 🎯 下一步

测试完成后，如有问题：
1. 查看浏览器控制台（F12）的错误信息
2. 查看后端日志输出
3. 检查 API 文档：http://localhost:8000/docs
4. 提交问题到项目 Issue 跟踪系统

---

**祝测试顺利！** 🚀


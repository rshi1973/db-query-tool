# CSV/JSON 导出功能设计与实现文档

## 📋 功能概述

CSV 和 JSON 导出功能允许用户将查询结果导出为文件，方便后续分析、共享或存档。该功能完全在客户端实现，无需后端参与，提供快速、即时的数据导出体验。

### 核心特性

- ✅ **CSV 导出**：符合 RFC 4180 标准的 CSV 格式
- ✅ **JSON 导出**：格式化的 JSON 数组格式
- ✅ **大数据集警告**：超过 10,000 行时显示警告对话框
- ✅ **自动文件命名**：包含数据库名称和时间戳
- ✅ **空数据处理**：正确处理 null/undefined 值
- ✅ **特殊字符转义**：正确处理逗号、引号、换行符等特殊字符

## 🎯 设计目标

### 1. 用户体验优先

- **即时性**：导出操作立即执行，无需等待服务器处理
- **直观性**：导出按钮位置明显，操作流程简单
- **安全性**：大数据集导出前提醒用户，避免浏览器崩溃
- **反馈性**：导出成功后显示明确的提示信息

### 2. 技术实现目标

- **纯前端实现**：利用浏览器 API，无需后端支持
- **性能优化**：高效的数据转换和文件生成
- **兼容性**：支持现代浏览器的标准 API
- **可维护性**：代码结构清晰，易于理解和扩展

### 3. 数据完整性

- **准确性**：确保导出的数据与查询结果完全一致
- **格式正确性**：符合标准格式规范，可被其他工具正确解析
- **编码支持**：统一使用 UTF-8 编码，支持多语言字符

## 🏗️ 架构设计

### 架构决策：客户端导出 vs 服务端导出

#### 选择的方案：客户端导出

**理由：**
1. **性能优势**：数据已在客户端内存中，无需再次网络传输
2. **服务器负载**：减少服务器资源消耗，降低后端复杂度
3. **即时性**：无需等待服务器处理，用户体验更好
4. **实现简单**：利用浏览器原生 API，代码量少，维护成本低

#### 替代方案分析

**服务端导出：**
- ✅ 优点：可以处理超大数据集，支持流式传输
- ❌ 缺点：需要额外的 API 端点，增加服务器负载，网络传输延迟

**当前方案的限制：**
- 受浏览器内存限制（通常 ~2GB）
- 大数据集（100k+ 行）可能导致浏览器卡顿或崩溃
- 未来可通过服务端导出作为补充方案

### 技术栈选择

```typescript
// 核心浏览器 API
- Blob API: 创建二进制文件对象
- URL.createObjectURL(): 生成临时下载链接
- document.createElement('a'): 创建下载链接元素

// 数据处理
- Array.map() / Array.join(): CSV 行生成
- JSON.stringify(): JSON 格式化

// UI 组件
- Ant Design Modal: 大数据集警告对话框
- Ant Design message: 成功/错误提示
```

## 📐 实现细节

### CSV 导出实现

#### 数据流程

```
查询结果 (QueryResult)
  ↓
提取列名 (headers)
  ↓
遍历行数据 (rows)
  ↓
转义特殊字符
  ↓
生成 CSV 行字符串
  ↓
合并所有行
  ↓
创建 Blob 对象
  ↓
触发浏览器下载
```

#### 核心代码逻辑

```typescript
const exportToCSV = () => {
  if (!queryResult) return;

  // 1. 提取列名作为表头
  const headers = queryResult.columns.map((col) => col.name);
  const csvRows = [headers.join(",")];

  // 2. 遍历每一行数据
  queryResult.rows.forEach((row) => {
    const values = headers.map((header) => {
      const value = row[header];
      
      // 3. 处理 null/undefined
      if (value === null || value === undefined) return "";
      
      // 4. 转换为字符串
      const stringValue = String(value);
      
      // 5. 转义特殊字符（CSV RFC 4180 规范）
      if (stringValue.includes(",") || 
          stringValue.includes('"') || 
          stringValue.includes("\n")) {
        // 引号内的引号需要双写（""）
        return `"${stringValue.replace(/"/g, '""')}"`;
      }
      return stringValue;
    });
    csvRows.push(values.join(","));
  });

  // 6. 生成完整的 CSV 内容
  const csvContent = csvRows.join("\n");
  
  // 7. 创建 Blob 并触发下载
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, -5);
  link.href = URL.createObjectURL(blob);
  link.download = `${selectedDatabase}_${timestamp}.csv`;
  link.click();
  URL.revokeObjectURL(link.href);
};
```

#### CSV 格式规范（RFC 4180）

1. **字段分隔符**：使用逗号 (`,`)
2. **行分隔符**：使用换行符 (`\n`)
3. **字段引用**：包含逗号、引号或换行符的字段必须用双引号包裹
4. **引号转义**：字段内的双引号需要双写 (`""`)
5. **编码**：使用 UTF-8 编码（通过 Blob 的 charset 参数指定）

#### 示例输出

```csv
id,name,email,description
1,"John Doe",john@example.com,"Software Engineer"
2,"Jane Smith",jane@example.com,"She said, ""Hello World!"""
3,Bob Wilson,bob@example.com,"Line 1
Line 2"
```

### JSON 导出实现

#### 数据流程

```
查询结果 (QueryResult)
  ↓
提取行数据 (rows)
  ↓
JSON.stringify() 格式化
  ↓
创建 Blob 对象
  ↓
触发浏览器下载
```

#### 核心代码逻辑

```typescript
const exportToJSON = () => {
  if (!queryResult) return;

  // 1. 使用 JSON.stringify 格式化数据
  // 参数：data, replacer(null=所有字段), 缩进空格数(2=格式化)
  const jsonContent = JSON.stringify(queryResult.rows, null, 2);
  
  // 2. 创建 Blob 并触发下载
  const blob = new Blob([jsonContent], { type: "application/json;charset=utf-8;" });
  const link = document.createElement("a");
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, -5);
  link.href = URL.createObjectURL(blob);
  link.download = `${selectedDatabase}_${timestamp}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
};
```

#### JSON 格式说明

- **结构**：数组格式，每个元素是一个对象，代表一行数据
- **格式化**：使用 2 个空格缩进，便于阅读
- **数据类型**：保留原始数据类型（数字、字符串、布尔值、null 等）
- **编码**：UTF-8 编码

#### 示例输出

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "active": true,
    "created_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "active": false,
    "created_at": null
  }
]
```

### 文件命名策略

#### 命名格式

```
{数据库名}_{时间戳}.{扩展名}
```

#### 时间戳格式

- **源格式**：ISO 8601 (例如: `2024-01-15T14:30:45.123Z`)
- **转换后**：移除特殊字符 (例如: `2024-01-15T14-30-45`)
- **实现**：`new Date().toISOString().replace(/[:.]/g, "-").slice(0, -5)`

#### 示例文件名

```
local-postgres_2024-01-15T14-30-45.csv
local-postgres_2024-01-15T14-30-45.json
production-db_2024-12-31T23-59-59.csv
```

### 大数据集警告机制

#### 触发条件

- **阈值**：10,000 行
- **检查时机**：点击导出按钮时
- **检查位置**：在数据转换之前

#### 警告对话框

```typescript
if (queryResult.rows.length > 10000) {
  Modal.confirm({
    title: "Large Dataset Warning",
    icon: <ExclamationCircleOutlined />,
    content: `You are about to export ${queryResult.rowCount.toLocaleString()} rows. 
             This may take a while and consume memory. Continue?`,
    onOk: () => exportToCSV(), // 用户确认后执行导出
  });
}
```

#### 用户体验考虑

- **明确的信息**：显示准确的行数（使用 `toLocaleString()` 格式化）
- **风险提示**：说明可能的内存消耗和处理时间
- **用户选择**：用户可以取消或继续
- **图标提示**：使用警告图标增强视觉提示

## 🔍 边界情况处理

### 1. 空结果集

```typescript
if (!queryResult || queryResult.rows.length === 0) {
  message.warning("No data to export");
  return;
}
```

### 2. Null/Undefined 值

**CSV：**
- 转换为空字符串 `""`

**JSON：**
- 保留 `null` 值（JSON 标准）

### 3. 特殊字符处理

**CSV 转义规则：**
- 包含 `,`、`"`、`\n` 的字段用引号包裹
- 字段内的 `"` 转换为 `""`
- 其他字符原样输出

**JSON：**
- `JSON.stringify()` 自动处理所有特殊字符
- Unicode 字符正确编码

### 4. 数据类型处理

- **数字**：保持原始格式（CSV 中为字符串，JSON 中为数字）
- **布尔值**：CSV 中转换为字符串，JSON 中保持布尔类型
- **日期/时间**：转换为字符串格式
- **对象/数组**：CSV 中序列化为字符串，JSON 中保持结构

## ⚡ 性能考虑

### 时间复杂度

- **CSV 生成**：O(n × m)，其中 n = 行数，m = 列数
- **JSON 生成**：O(n × m)，但 `JSON.stringify()` 是优化的原生函数

### 空间复杂度

- **内存使用**：O(n × m)，整个结果集在内存中
- **文件大小**：CSV 通常比 JSON 小（无格式化空格）

### 性能优化策略

1. **使用数组 join**：避免字符串多次拼接
   ```typescript
   // ✅ 高效
   const csvRows = [headers.join(",")];
   csvRows.push(values.join(","));
   const csvContent = csvRows.join("\n");
   
   // ❌ 低效
   let csvContent = headers.join(",") + "\n";
   csvContent += values.join(",") + "\n";
   ```

2. **最小化正则使用**：只在必要时使用
   ```typescript
   // ✅ 只检查一次
   if (stringValue.includes(",") || stringValue.includes('"')) {
     return `"${stringValue.replace(/"/g, '""')}"`;
   }
   ```

3. **原生 API**：使用浏览器优化的 `JSON.stringify()`

### 性能基准（参考值）

| 行数 | CSV 生成时间 | JSON 生成时间 | 文件大小 (CSV) | 文件大小 (JSON) |
|------|-------------|--------------|---------------|----------------|
| 1,000 | ~10ms | ~5ms | ~50KB | ~80KB |
| 10,000 | ~100ms | ~50ms | ~500KB | ~800KB |
| 100,000 | ~1s | ~500ms | ~5MB | ~8MB |

*注：实际性能取决于列数、数据复杂度、浏览器和硬件配置*

## 🎨 用户界面设计

### 按钮位置

- **位置**：查询结果卡片（Card）的右上角（extra 区域）
- **样式**：与整体设计系统一致
- **布局**：两个按钮并排显示，间距合适

### 视觉反馈

1. **成功提示**：
   ```typescript
   message.success(`Exported ${queryResult.rowCount} rows to CSV`);
   ```

2. **警告对话框**：大数据集时的模态确认

3. **空状态处理**：无数据时的警告提示

### 交互流程

```
用户点击导出按钮
  ↓
检查是否有数据
  ↓ (无数据)
显示警告提示
  ↓ (有数据)
检查数据量
  ↓ (>10,000 行)
显示警告对话框
  ↓ (用户确认) 或 (<10,000 行)
执行导出
  ↓
显示成功提示
```

## 📊 代码位置

### 主要文件

- **实现位置**：`frontend/src/pages/Home.tsx`
- **相关组件**：Ant Design `Modal`, `message`
- **代码行数**：约 80 行（包含 CSV 和 JSON）

### 函数列表

1. `handleExportCSV()` - CSV 导出入口，包含大数据集检查
2. `exportToCSV()` - CSV 生成和下载逻辑
3. `handleExportJSON()` - JSON 导出入口，包含大数据集检查
4. `exportToJSON()` - JSON 生成和下载逻辑

## 🚀 未来改进方向

### 短期优化

1. **导出进度指示**：大数据集导出时显示进度条
2. **取消导出**：允许用户取消正在进行的导出操作
3. **导出格式选项**：允许用户选择分隔符、编码等

### 中期增强

1. **服务端导出**：对于超大数据集，提供服务端导出选项
2. **Excel 导出**：支持 `.xlsx` 格式（需要第三方库，如 `xlsx`）
3. **批量导出**：支持导出多个查询结果
4. **导出模板**：支持自定义导出模板和字段选择

### 长期规划

1. **流式导出**：支持超大数据的流式处理
2. **导出历史**：记录导出历史，支持重新下载
3. **导出调度**：支持定时自动导出
4. **云存储集成**：支持直接导出到云存储（S3、Google Drive 等）

## 📝 测试要点

### 功能测试

- ✅ 空结果集导出（应显示警告）
- ✅ 正常数据集导出（CSV 和 JSON）
- ✅ 大数据集导出（应显示警告对话框）
- ✅ 特殊字符转义（逗号、引号、换行符）
- ✅ Null 值处理
- ✅ 文件名格式正确性
- ✅ 文件内容完整性验证

### 性能测试

- ✅ 小数据集（< 100 行）导出速度
- ✅ 中等数据集（1,000 - 10,000 行）导出速度
- ✅ 大数据集（> 10,000 行）导出时间和内存使用
- ✅ 浏览器兼容性测试

### 边界测试

- ✅ 单行数据导出
- ✅ 单列数据导出
- ✅ 超长文本字段导出
- ✅ 各种数据类型（数字、字符串、布尔值、日期、null）

## 🔗 相关文档

- [Phase 3 Implementation](./PHASE3_IMPLEMENTATION.md) - 完整实现说明
- [Quick Start Guide](./QUICK_START.md) - 使用指南
- [RFC 4180 - CSV Format](https://tools.ietf.org/html/rfc4180) - CSV 标准规范
- [MDN - Blob API](https://developer.mozilla.org/en-US/docs/Web/API/Blob) - Blob API 文档

## 📌 总结

CSV/JSON 导出功能采用纯前端实现，充分利用浏览器原生 API，提供了高效、直观的数据导出体验。通过合理的设计和实现，在保证功能完整性的同时，也兼顾了性能和用户体验。对于大多数使用场景（< 10,000 行），该实现能够满足需求；对于更大数据集，可以通过服务端导出作为补充方案。


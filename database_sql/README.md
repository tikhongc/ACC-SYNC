# 数据库SQL相关文件

## 📁 文件夹说明

这个文件夹包含所有与**Neon PostgreSQL**数据库相关的文件。

## 🗄️ 当前数据库

- **数据库类型**: PostgreSQL 17.5
- **服务提供商**: Neon (https://neon.tech)
- **连接方式**: 云端托管
- **特点**: 
  - 现代化PostgreSQL云服务
  - 自动扩缩容
  - 分支功能
  - 免费512MB存储

## 📋 文件清单

### 配置文件
- `neon_config.py` - Neon PostgreSQL连接配置
- `neon_env.py` - 环境变量配置
- `connection_test.py` - 连接测试脚本

### 数据访问层
- `neon_data_access.py` - Neon数据访问层
- `neon_sync_api.py` - 同步API接口

### SQL脚本
- `schema_create.sql` - 数据库表结构创建脚本
- `indexes_create.sql` - 索引创建脚本
- `sample_data.sql` - 示例数据插入脚本

### 迁移工具
- `mongodb_to_neon_migration.py` - MongoDB到Neon迁移工具
- `data_comparison.py` - 数据对比工具

### 测试文件
- `test_neon_operations.py` - 数据库操作测试
- `performance_test.py` - 性能测试

## 🔗 连接信息

```
Host: ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech
Port: 5432
Database: neondb
User: neondb_owner
SSL: Required
```

## 🚀 快速开始

1. **测试连接**:
   ```bash
   python database_sql/connection_test.py
   ```

2. **初始化数据库**:
   ```bash
   python database_sql/neon_data_access.py
   ```

3. **运行迁移**:
   ```bash
   python database_sql/mongodb_to_neon_migration.py
   ```

## 📊 与MongoDB对比

| 特性 | MongoDB | Neon PostgreSQL |
|------|---------|-----------------|
| 数据类型 | NoSQL文档 | 关系型+JSONB |
| 查询语言 | MongoDB查询 | SQL + JSON操作 |
| 扩展性 | 水平分片 | 垂直+云端扩展 |
| 事务支持 | 有限 | 完整ACID |
| JSON支持 | 原生 | JSONB优化 |
| 企业功能 | 基础 | 完整 |

## 🎯 迁移状态

- [x] 连接配置完成
- [x] 数据访问层完成
- [x] 基础测试通过
- [ ] 生产数据迁移
- [ ] 性能优化
- [ ] 监控配置

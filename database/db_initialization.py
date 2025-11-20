# -*- coding: utf-8 -*-
"""
数据库初始化和索引管理模块
用于创建优化的MongoDB集合和索引
"""

import logging
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.errors import CollectionInvalid, OperationFailure
from datetime import datetime
from .mongodb_config import MongoDBConfig
from .optimized_schema_design import OPTIMIZED_INDEXES, VALIDATION_RULES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseInitializer:
    """数据库初始化器"""
    
    def __init__(self, db_config: MongoDBConfig = None):
        self.db_config = db_config or MongoDBConfig()
        self.database = None
        
    def connect(self):
        """连接数据库"""
        if not self.db_config.connect():
            raise Exception("无法连接到MongoDB数据库")
        self.database = self.db_config.get_database()
        return True
    
    def initialize_database(self, drop_existing=False):
        """
        初始化数据库
        
        Args:
            drop_existing: 是否删除现有集合重新创建
        """
        try:
            if not self.database:
                self.connect()
            
            logger.info("开始初始化数据库...")
            
            # 创建集合
            self._create_collections(drop_existing)
            
            # 创建索引
            self._create_indexes()
            
            # 设置验证规则
            self._setup_validation_rules()
            
            # 创建初始数据
            self._create_initial_data()
            
            logger.info("数据库初始化完成!")
            return True
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            return False
    
    def _create_collections(self, drop_existing=False):
        """创建集合"""
        collections = [
            "projects",
            "folders", 
            "files",
            "file_versions",
            "sync_tasks"
        ]
        
        for collection_name in collections:
            try:
                if drop_existing and collection_name in self.database.list_collection_names():
                    logger.info(f"删除现有集合: {collection_name}")
                    self.database.drop_collection(collection_name)
                
                if collection_name not in self.database.list_collection_names():
                    logger.info(f"创建集合: {collection_name}")
                    self.database.create_collection(collection_name)
                else:
                    logger.info(f"集合已存在: {collection_name}")
                    
            except CollectionInvalid as e:
                logger.warning(f"集合 {collection_name} 创建警告: {str(e)}")
            except Exception as e:
                logger.error(f"创建集合 {collection_name} 失败: {str(e)}")
                raise
    
    def _create_indexes(self):
        """创建索引"""
        logger.info("开始创建索引...")
        
        for collection_name, indexes in OPTIMIZED_INDEXES.items():
            if collection_name not in self.database.list_collection_names():
                logger.warning(f"集合 {collection_name} 不存在，跳过索引创建")
                continue
                
            collection = self.database[collection_name]
            
            # 获取现有索引
            existing_indexes = list(collection.list_indexes())
            existing_index_names = {idx['name'] for idx in existing_indexes}
            
            logger.info(f"为集合 {collection_name} 创建索引...")
            
            for index_spec in indexes:
                try:
                    # 处理不同类型的索引
                    if isinstance(index_spec, dict):
                        # 检查是否是文本索引
                        if any(v == "text" for v in index_spec.values()):
                            index_name = f"{collection_name}_text_index"
                            if index_name not in existing_index_names:
                                result = collection.create_index(
                                    [(k, TEXT) for k, v in index_spec.items() if v == "text"],
                                    name=index_name
                                )
                                logger.info(f"  创建文本索引: {index_name} -> {result}")
                        else:
                            # 普通索引
                            index_fields = []
                            for field, direction in index_spec.items():
                                if direction == 1:
                                    index_fields.append((field, ASCENDING))
                                elif direction == -1:
                                    index_fields.append((field, DESCENDING))
                            
                            if index_fields:
                                index_name = f"{collection_name}_{'_'.join([f[0].replace('.', '_') for f in index_fields])}"
                                if index_name not in existing_index_names:
                                    result = collection.create_index(
                                        index_fields,
                                        name=index_name
                                    )
                                    logger.info(f"  创建索引: {index_name} -> {result}")
                                else:
                                    logger.info(f"  索引已存在: {index_name}")
                    
                except OperationFailure as e:
                    logger.warning(f"  创建索引失败: {str(e)}")
                except Exception as e:
                    logger.error(f"  创建索引时出错: {str(e)}")
        
        logger.info("索引创建完成")
    
    def _setup_validation_rules(self):
        """设置验证规则"""
        logger.info("设置集合验证规则...")
        
        for collection_name, rules in VALIDATION_RULES.items():
            if collection_name not in self.database.list_collection_names():
                continue
                
            try:
                # MongoDB的验证规则设置
                validator = {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": rules.get("required_fields", []),
                        "properties": {}
                    }
                }
                
                # 添加字段类型验证
                field_types = rules.get("field_types", {})
                for field_path, field_type in field_types.items():
                    # 简化的类型映射
                    bson_type = "string"
                    if field_type == int:
                        bson_type = "int"
                    elif field_type == float:
                        bson_type = "double"
                    elif field_type == bool:
                        bson_type = "bool"
                    
                    # 处理嵌套字段路径
                    if "." in field_path:
                        # 暂时跳过嵌套字段验证，MongoDB的jsonSchema比较复杂
                        continue
                    else:
                        validator["$jsonSchema"]["properties"][field_path] = {
                            "bsonType": bson_type
                        }
                
                # 应用验证规则
                self.database.command({
                    "collMod": collection_name,
                    "validator": validator,
                    "validationLevel": "moderate",  # 只对新文档和更新验证
                    "validationAction": "warn"      # 验证失败时警告而不是错误
                })
                
                logger.info(f"  为集合 {collection_name} 设置验证规则")
                
            except Exception as e:
                logger.warning(f"  设置集合 {collection_name} 验证规则失败: {str(e)}")
    
    def _create_initial_data(self):
        """创建初始数据"""
        logger.info("创建初始数据...")
        
        # 创建系统配置文档
        try:
            system_config = {
                "_id": "system_config",
                "version": "1.0.0",
                "schema_version": "1.0.0",
                "initialized_at": datetime.now(),
                "features": {
                    "file_sync": True,
                    "folder_sync": True,
                    "version_tracking": True,
                    "custom_attributes": True,
                    "review_states": True
                },
                "limits": {
                    "max_file_size_mb": 1000,
                    "max_versions_per_file": 100,
                    "max_depth": 20
                }
            }
            
            # 检查是否已存在
            if not self.database.system_config.find_one({"_id": "system_config"}):
                self.database.system_config.insert_one(system_config)
                logger.info("  创建系统配置文档")
            else:
                logger.info("  系统配置文档已存在")
                
        except Exception as e:
            logger.warning(f"创建初始数据失败: {str(e)}")
    
    def get_database_info(self):
        """获取数据库信息"""
        try:
            if not self.database:
                self.connect()
            
            info = {
                "database_name": self.database.name,
                "collections": [],
                "total_size_mb": 0,
                "total_documents": 0
            }
            
            # 获取集合信息
            for collection_name in self.database.list_collection_names():
                collection = self.database[collection_name]
                stats = self.database.command("collStats", collection_name)
                
                collection_info = {
                    "name": collection_name,
                    "document_count": collection.count_documents({}),
                    "size_mb": round(stats.get("size", 0) / (1024 * 1024), 2),
                    "indexes": len(list(collection.list_indexes())),
                    "avg_document_size": stats.get("avgObjSize", 0)
                }
                
                info["collections"].append(collection_info)
                info["total_documents"] += collection_info["document_count"]
                info["total_size_mb"] += collection_info["size_mb"]
            
            info["total_size_mb"] = round(info["total_size_mb"], 2)
            return info
            
        except Exception as e:
            logger.error(f"获取数据库信息失败: {str(e)}")
            return None
    
    def optimize_database(self):
        """优化数据库性能"""
        logger.info("开始数据库优化...")
        
        try:
            if not self.database:
                self.connect()
            
            # 重建索引
            for collection_name in ["folders", "files", "file_versions"]:
                if collection_name in self.database.list_collection_names():
                    logger.info(f"重建集合 {collection_name} 的索引...")
                    self.database[collection_name].reindex()
            
            # 压缩集合（如果支持）
            try:
                for collection_name in ["folders", "files", "file_versions"]:
                    if collection_name in self.database.list_collection_names():
                        logger.info(f"压缩集合 {collection_name}...")
                        self.database.command("compact", collection_name)
            except Exception as e:
                logger.warning(f"集合压缩失败（可能不支持）: {str(e)}")
            
            logger.info("数据库优化完成")
            return True
            
        except Exception as e:
            logger.error(f"数据库优化失败: {str(e)}")
            return False
    
    def cleanup_old_data(self, days_to_keep=30):
        """清理旧数据"""
        logger.info(f"清理 {days_to_keep} 天前的旧数据...")
        
        try:
            if not self.database:
                self.connect()
            
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # 清理旧的同步任务记录
            result = self.database.sync_tasks.delete_many({
                "start_time": {"$lt": cutoff_date},
                "task_status": {"$in": ["completed", "failed"]}
            })
            logger.info(f"  删除了 {result.deleted_count} 个旧同步任务记录")
            
            # 清理旧的系统日志（如果有的话）
            if "system_logs" in self.database.list_collection_names():
                result = self.database.system_logs.delete_many({
                    "created_at": {"$lt": cutoff_date}
                })
                logger.info(f"  删除了 {result.deleted_count} 个旧日志记录")
            
            logger.info("旧数据清理完成")
            return True
            
        except Exception as e:
            logger.error(f"清理旧数据失败: {str(e)}")
            return False

# 便利函数
def initialize_database(drop_existing=False):
    """初始化数据库的便利函数"""
    initializer = DatabaseInitializer()
    return initializer.initialize_database(drop_existing)

def get_database_info():
    """获取数据库信息的便利函数"""
    initializer = DatabaseInitializer()
    return initializer.get_database_info()

def optimize_database():
    """优化数据库的便利函数"""
    initializer = DatabaseInitializer()
    return initializer.optimize_database()

if __name__ == "__main__":
    # 测试数据库初始化
    print("开始数据库初始化测试...")
    
    initializer = DatabaseInitializer()
    
    # 初始化数据库
    if initializer.initialize_database():
        print("✅ 数据库初始化成功")
        
        # 获取数据库信息
        info = initializer.get_database_info()
        if info:
            print(f"📊 数据库信息:")
            print(f"  数据库名: {info['database_name']}")
            print(f"  集合数量: {len(info['collections'])}")
            print(f"  总文档数: {info['total_documents']}")
            print(f"  总大小: {info['total_size_mb']} MB")
            
            for collection in info['collections']:
                print(f"  - {collection['name']}: {collection['document_count']} 文档, {collection['size_mb']} MB, {collection['indexes']} 个索引")
    else:
        print("❌ 数据库初始化失败")

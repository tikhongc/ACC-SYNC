# ACC 同步系统通用优化策略

## 📋 文档概览

本文档提供了 ACC (Autodesk Construction Cloud) 项目同步系统的**通用优化策略**，涵盖了 MongoDB 和 PostgreSQL 两种数据库方案的共同优化原则、实施指南和最佳实践。

## 🎯 优化目标

### 核心性能指标

```
┌─────────────────────────────────────────────────────────────┐
│                      优化目标设定                             │
├─────────────────────────────────────────────────────────────┤
│ API调用减少:      90-95% (智能跳过 + 批量操作)               │
│ 同步速度提升:     300-500% (多层次优化)                      │
│ 数据库IO优化:     80-95% (批量操作 + 连接优化)               │
│ 内存使用优化:     50-70% (流式处理 + 及时清理)               │
│ 错误恢复能力:     显著提升 (多层回退机制)                     │
│ 系统可扩展性:     支持10倍以上数据量增长                      │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ 五层优化架构

### Layer 1: 智能分支跳过 (Smart Branch Skipping)

#### 核心原理

```python
class UniversalSmartBranchSkipping:
    """通用智能分支跳过策略"""
    
    def __init__(self, database_type='mongodb'):
        self.database_type = database_type
        self.skip_stats = {
            'total_folders_checked': 0,
            'folders_skipped': 0,
            'api_calls_saved': 0,
            'processing_time_saved': 0
        }
    
    def should_skip_folder_branch(self, folder_data, last_sync_time):
        """
        通用分支跳过逻辑
        
        核心判断：
        1. last_modified_time_rollup <= last_sync_time → 跳过整个分支
        2. 递归检查子文件夹的 rollup 时间
        3. 统计跳过效率
        """
        
        # 🔑 核心优化点：rollup 时间比较
        folder_rollup_time = self._parse_datetime(
            folder_data.get('attributes', {}).get('lastModifiedTimeRollup')
        )
        
        if not folder_rollup_time or not last_sync_time:
            return False  # 保守策略：无法确定时不跳过
        
        # 时间比较
        can_skip = folder_rollup_time <= last_sync_time
        
        if can_skip:
            self.skip_stats['folders_skipped'] += 1
            self.skip_stats['api_calls_saved'] += self._estimate_saved_api_calls(folder_data)
            
            logger.debug(f"Smart skip: {folder_data.get('name')} "
                        f"(rollup: {folder_rollup_time} <= sync: {last_sync_time})")
        
        self.skip_stats['total_folders_checked'] += 1
        return can_skip
    
    def calculate_skip_efficiency(self):
        """计算跳过效率"""
        if self.skip_stats['total_folders_checked'] == 0:
            return 0.0
        
        efficiency = (
            self.skip_stats['folders_skipped'] / 
            self.skip_stats['total_folders_checked']
        ) * 100
        
        return round(efficiency, 2)
    
    def _estimate_saved_api_calls(self, folder_data):
        """估算节省的API调用次数"""
        # 基于文件夹的 objectCount 估算
        object_count = folder_data.get('attributes', {}).get('objectCount', 1)
        
        # 估算：每个对象平均需要2-3次API调用（内容+版本+属性）
        estimated_calls = object_count * 2.5
        
        return int(estimated_calls)
```

#### 实施策略

```python
# 通用分支跳过实施流程
SMART_BRANCH_SKIPPING_FLOW = {
    "第1步": {
        "操作": "获取项目顶级文件夹",
        "优化": "并发获取多个项目的顶级结构"
    },
    
    "第2步": {
        "操作": "检查每个文件夹的 rollup 时间",
        "优化": "批量时间比较，避免逐个检查"
    },
    
    "第3步": {
        "操作": "递归遍历有变化的分支",
        "优化": "BFS遍历，层级并发处理"
    },
    
    "第4步": {
        "操作": "收集变化的文件和文件夹",
        "优化": "流式收集，避免内存积累"
    },
    
    "第5步": {
        "操作": "统计跳过效率",
        "优化": "实时监控，动态调整策略"
    }
}
```

### Layer 2: 批量API调用优化 (Batch API Operations)

#### 通用批量策略

```python
class UniversalBatchAPIOptimization:
    """通用批量API优化策略"""
    
    def __init__(self):
        self.batch_configs = {
            'list_items': {
                'max_size': 50,      # ListItems API限制
                'timeout': 30,
                'retry_count': 3
            },
            'custom_attributes': {
                'max_size': 50,      # Custom Attributes API限制
                'timeout': 25,
                'retry_count': 3
            },
            'folder_contents': {
                'max_size': 20,      # 文件夹内容批量
                'timeout': 20,
                'retry_count': 2
            }
        }
    
    async def execute_batch_operations(self, operation_type, items, project_id):
        """执行批量操作的通用流程"""
        
        config = self.batch_configs.get(operation_type)
        if not config:
            raise ValueError(f"Unsupported operation type: {operation_type}")
        
        # 分批处理
        batches = self._create_optimal_batches(items, config['max_size'])
        results = []
        
        # 并发执行批次
        semaphore = asyncio.Semaphore(5)  # 控制并发数
        
        async def process_batch(batch):
            async with semaphore:
                return await self._execute_single_batch(
                    operation_type, batch, project_id, config
                )
        
        # 创建并发任务
        tasks = [process_batch(batch) for batch in batches]
        
        # 执行并收集结果
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果和异常
        for i, result in enumerate(batch_results):
            if isinstance(result, Exception):
                logger.warning(f"Batch {i} failed: {result}")
                # 回退到单个处理
                fallback_result = await self._fallback_single_processing(
                    operation_type, batches[i], project_id
                )
                results.extend(fallback_result)
            else:
                results.extend(result)
        
        return results
    
    def _create_optimal_batches(self, items, max_batch_size):
        """创建优化的批次"""
        
        # 智能分批策略
        batches = []
        current_batch = []
        current_size = 0
        
        # 动态批次大小调整
        for item in items:
            item_complexity = self._calculate_item_complexity(item)
            
            # 如果添加当前项目会超过限制，创建新批次
            if (len(current_batch) >= max_batch_size or 
                current_size + item_complexity > max_batch_size * 1.2):
                
                if current_batch:
                    batches.append(current_batch)
                    current_batch = []
                    current_size = 0
            
            current_batch.append(item)
            current_size += item_complexity
        
        # 添加最后一个批次
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _calculate_item_complexity(self, item):
        """计算项目复杂度（用于批次大小调整）"""
        
        complexity = 1  # 基础复杂度
        
        # 根据项目类型调整
        if item.get('type') == 'folders':
            complexity += item.get('attributes', {}).get('objectCount', 0) * 0.1
        
        # 根据自定义属性数量调整
        custom_attrs = item.get('custom_attributes', [])
        complexity += len(custom_attrs) * 0.2
        
        # 根据文件大小调整
        file_size = item.get('attributes', {}).get('fileSize', 0)
        if file_size > 10 * 1024 * 1024:  # 10MB以上
            complexity += 2
        
        return complexity
```

#### API调用优化模式

```python
# 批量API调用模式
BATCH_API_PATTERNS = {
    "ListItems模式": {
        "适用场景": "批量获取文件元数据和版本信息",
        "优势": "单次调用获取50个文件的完整信息",
        "限制": "最多50个items，响应可能较大",
        "优化": "并发多个批次，流式处理结果"
    },
    
    "Custom Attributes模式": {
        "适用场景": "批量获取自定义属性",
        "优势": "避免逐个文件查询属性",
        "限制": "最多50个文档，需要version URN",
        "优化": "预收集URN，批量查询，增量对比"
    },
    
    "Folder Contents模式": {
        "适用场景": "批量获取文件夹内容",
        "优势": "减少文件夹遍历API调用",
        "限制": "每个文件夹单独调用",
        "优化": "并发获取多个文件夹，智能跳过"
    },
    
    "混合模式": {
        "适用场景": "复杂同步场景",
        "优势": "结合多种API的优势",
        "限制": "实现复杂度较高",
        "优化": "分阶段执行，错误隔离"
    }
}
```

### Layer 3: 数据库层优化 (Database Layer Optimization)

#### 通用数据库优化策略

```python
class UniversalDatabaseOptimization:
    """通用数据库优化策略"""
    
    def __init__(self, db_type, connection_pool):
        self.db_type = db_type  # 'mongodb' or 'postgresql'
        self.connection_pool = connection_pool
        self.optimization_strategies = self._init_strategies()
    
    def _init_strategies(self):
        """初始化数据库特定的优化策略"""
        
        if self.db_type == 'mongodb':
            return {
                'batch_operation': self._mongodb_batch_operation,
                'custom_attributes': self._mongodb_embedded_attributes,
                'indexing': self._mongodb_indexing_strategy,
                'aggregation': self._mongodb_aggregation_optimization
            }
        elif self.db_type == 'postgresql':
            return {
                'batch_operation': self._postgresql_batch_operation,
                'custom_attributes': self._postgresql_separated_attributes,
                'indexing': self._postgresql_indexing_strategy,
                'advanced_queries': self._postgresql_advanced_queries
            }
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
    
    async def execute_optimized_sync(self, sync_data):
        """执行优化的数据库同步"""
        
        # 通用同步流程
        results = {
            'files_synced': 0,
            'folders_synced': 0,
            'custom_attrs_synced': 0,
            'errors': []
        }
        
        try:
            # 第1阶段：文件夹同步
            if sync_data.get('folders'):
                folder_result = await self.optimization_strategies['batch_operation'](
                    'folders', sync_data['folders']
                )
                results['folders_synced'] = folder_result.get('count', 0)
            
            # 第2阶段：文件同步
            if sync_data.get('files'):
                file_result = await self.optimization_strategies['batch_operation'](
                    'files', sync_data['files']
                )
                results['files_synced'] = file_result.get('count', 0)
            
            # 第3阶段：自定义属性同步
            if sync_data.get('custom_attributes'):
                attr_result = await self.optimization_strategies['custom_attributes'](
                    sync_data['custom_attributes']
                )
                results['custom_attrs_synced'] = attr_result.get('count', 0)
            
            return results
            
        except Exception as e:
            logger.error(f"Database sync failed: {e}")
            results['errors'].append(str(e))
            
            # 执行回退策略
            return await self._execute_fallback_sync(sync_data, results)
    
    async def _execute_fallback_sync(self, sync_data, partial_results):
        """执行回退同步策略"""
        
        logger.info("Executing fallback sync strategy")
        
        # 回退到单个操作
        for data_type, items in sync_data.items():
            if not items:
                continue
                
            success_count = 0
            for item in items:
                try:
                    await self._single_item_sync(data_type, item)
                    success_count += 1
                except Exception as e:
                    partial_results['errors'].append(f"{data_type} item failed: {e}")
            
            # 更新成功计数
            if data_type == 'files':
                partial_results['files_synced'] += success_count
            elif data_type == 'folders':
                partial_results['folders_synced'] += success_count
            elif data_type == 'custom_attributes':
                partial_results['custom_attrs_synced'] += success_count
        
        return partial_results
```

#### 数据库特定优化

```python
# MongoDB 优化策略
MONGODB_OPTIMIZATION_STRATEGIES = {
    "嵌入式文档": {
        "优势": "单次查询获取完整数据，避免JOIN",
        "适用": "自定义属性、版本信息、扩展数据",
        "实现": "将相关数据嵌入到主文档中"
    },
    
    "聚合管道": {
        "优势": "数据库层面的复杂处理，减少网络传输",
        "适用": "智能分支跳过、数据统计、复杂查询",
        "实现": "使用 $lookup, $match, $group 等操作"
    },
    
    "批量写入": {
        "优势": "原生 bulk_write 支持，高性能",
        "适用": "大批量数据同步",
        "实现": "使用 UpdateOne, InsertOne 的批量操作"
    },
    
    "索引优化": {
        "优势": "复合索引、稀疏索引、部分索引",
        "适用": "查询性能优化",
        "实现": "针对查询模式设计专门索引"
    }
}

# PostgreSQL 优化策略
POSTGRESQL_OPTIMIZATION_STRATEGIES = {
    "分离表设计": {
        "优势": "数据规范化，避免冗余，更好的一致性",
        "适用": "自定义属性、版本历史、权限管理",
        "实现": "外键关联，事务保证一致性"
    },
    
    "CTE和窗口函数": {
        "优势": "复杂查询优化，递归处理",
        "适用": "文件夹层次遍历、增量查询",
        "实现": "WITH RECURSIVE, ROW_NUMBER() 等"
    },
    
    "UPSERT操作": {
        "优势": "原生 ON CONFLICT 支持",
        "适用": "批量同步，避免重复数据",
        "实现": "INSERT ... ON CONFLICT DO UPDATE"
    },
    
    "COPY批量导入": {
        "优势": "最高性能的批量数据导入",
        "适用": "大批量初始同步",
        "实现": "临时表 + COPY + 合并操作"
    },
    
    "JSONB支持": {
        "优势": "灵活存储 + 高效查询",
        "适用": "扩展属性、元数据、配置信息",
        "实现": "JSONB字段 + GIN索引"
    }
}
```

### Layer 4: 并发处理优化 (Concurrent Processing)

#### 通用并发架构

```python
class UniversalConcurrentProcessor:
    """通用并发处理器"""
    
    def __init__(self, max_workers=12, db_pool_size=20):
        self.max_workers = max_workers
        self.db_pool_size = db_pool_size
        
        # 不同类型任务的并发控制
        self.semaphores = {
            'api_calls': asyncio.Semaphore(8),      # API调用并发
            'db_operations': asyncio.Semaphore(15), # 数据库操作并发
            'data_processing': asyncio.Semaphore(10) # 数据处理并发
        }
        
        # 性能监控
        self.performance_stats = {
            'concurrent_batches': 0,
            'total_processing_time': 0,
            'average_batch_time': 0,
            'peak_concurrency': 0
        }
    
    async def execute_concurrent_sync(self, project_id, sync_items):
        """执行并发同步"""
        
        start_time = time.time()
        
        # 🔑 第1阶段：智能任务分组
        task_groups = self._create_intelligent_task_groups(sync_items)
        
        # 🔑 第2阶段：分阶段并发执行
        results = await self._execute_phased_concurrent_processing(
            project_id, task_groups
        )
        
        # 🔑 第3阶段：性能统计
        end_time = time.time()
        self.performance_stats['total_processing_time'] = end_time - start_time
        self.performance_stats['average_batch_time'] = (
            self.performance_stats['total_processing_time'] / 
            max(self.performance_stats['concurrent_batches'], 1)
        )
        
        return {
            'sync_results': results,
            'performance_stats': self.performance_stats
        }
    
    def _create_intelligent_task_groups(self, sync_items):
        """智能任务分组"""
        
        # 按类型和复杂度分组
        task_groups = {
            'high_priority': [],    # 高优先级：小文件、重要文件夹
            'medium_priority': [],  # 中优先级：普通文件
            'low_priority': [],     # 低优先级：大文件、复杂属性
            'background': []        # 后台任务：统计、清理等
        }
        
        for item in sync_items:
            priority = self._calculate_task_priority(item)
            task_groups[priority].append(item)
        
        return task_groups
    
    def _calculate_task_priority(self, item):
        """计算任务优先级"""
        
        # 基础优先级
        if item.get('type') == 'folders':
            base_priority = 'high_priority'
        else:
            base_priority = 'medium_priority'
        
        # 根据文件大小调整
        file_size = item.get('attributes', {}).get('fileSize', 0)
        if file_size > 50 * 1024 * 1024:  # 50MB以上
            return 'low_priority'
        
        # 根据自定义属性数量调整
        custom_attrs_count = len(item.get('custom_attributes', []))
        if custom_attrs_count > 10:
            return 'low_priority'
        
        # 根据修改时间调整（最近修改的优先）
        last_modified = item.get('attributes', {}).get('lastModifiedTime')
        if last_modified:
            modified_time = self._parse_datetime(last_modified)
            if modified_time and (datetime.utcnow() - modified_time).days < 1:
                return 'high_priority'
        
        return base_priority
    
    async def _execute_phased_concurrent_processing(self, project_id, task_groups):
        """分阶段并发处理"""
        
        results = {
            'high_priority': {'count': 0, 'errors': []},
            'medium_priority': {'count': 0, 'errors': []},
            'low_priority': {'count': 0, 'errors': []},
            'background': {'count': 0, 'errors': []}
        }
        
        # 阶段1：高优先级任务（最大并发）
        if task_groups['high_priority']:
            logger.info(f"Processing {len(task_groups['high_priority'])} high priority items")
            results['high_priority'] = await self._process_priority_group(
                project_id, task_groups['high_priority'], max_concurrency=self.max_workers
            )
        
        # 阶段2：中优先级任务（中等并发）
        if task_groups['medium_priority']:
            logger.info(f"Processing {len(task_groups['medium_priority'])} medium priority items")
            results['medium_priority'] = await self._process_priority_group(
                project_id, task_groups['medium_priority'], max_concurrency=self.max_workers // 2
            )
        
        # 阶段3：低优先级任务（低并发，避免资源竞争）
        if task_groups['low_priority']:
            logger.info(f"Processing {len(task_groups['low_priority'])} low priority items")
            results['low_priority'] = await self._process_priority_group(
                project_id, task_groups['low_priority'], max_concurrency=self.max_workers // 4
            )
        
        # 阶段4：后台任务（异步执行）
        if task_groups['background']:
            logger.info(f"Scheduling {len(task_groups['background'])} background tasks")
            asyncio.create_task(self._process_background_tasks(
                project_id, task_groups['background']
            ))
            results['background'] = {'count': len(task_groups['background']), 'errors': []}
        
        return results
    
    async def _process_priority_group(self, project_id, items, max_concurrency):
        """处理优先级组"""
        
        semaphore = asyncio.Semaphore(max_concurrency)
        
        async def process_item_with_semaphore(item):
            async with semaphore:
                return await self._process_single_item_concurrent(project_id, item)
        
        # 创建并发任务
        tasks = [process_item_with_semaphore(item) for item in items]
        
        # 执行并收集结果
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 统计结果
        success_count = 0
        errors = []
        
        for result in results:
            if isinstance(result, Exception):
                errors.append(str(result))
            else:
                success_count += 1
        
        self.performance_stats['concurrent_batches'] += 1
        self.performance_stats['peak_concurrency'] = max(
            self.performance_stats['peak_concurrency'], 
            len(tasks)
        )
        
        return {'count': success_count, 'errors': errors}
```

#### 并发优化模式

```python
# 并发优化模式
CONCURRENT_OPTIMIZATION_PATTERNS = {
    "分阶段并发": {
        "描述": "按优先级分阶段执行，避免资源竞争",
        "适用": "混合类型任务处理",
        "优势": "资源利用最优化，错误隔离",
        "实现": "优先级队列 + 动态并发度调整"
    },
    
    "资源池管理": {
        "描述": "分离不同类型的资源池",
        "适用": "API调用、数据库操作、数据处理",
        "优势": "避免资源竞争，提高吞吐量",
        "实现": "独立的信号量和连接池"
    },
    
    "智能批次调度": {
        "描述": "根据系统负载动态调整批次大小",
        "适用": "大批量数据处理",
        "优势": "适应系统资源变化",
        "实现": "监控系统资源 + 动态参数调整"
    },
    
    "错误隔离": {
        "描述": "单个任务失败不影响整体处理",
        "适用": "所有并发场景",
        "优势": "提高系统稳定性",
        "实现": "异常捕获 + 独立重试机制"
    }
}
```

### Layer 5: 内存管理与监控 (Memory Management & Monitoring)

#### 通用内存管理策略

```python
class UniversalMemoryManager:
    """通用内存管理器"""
    
    def __init__(self, max_memory_mb=1024):
        self.max_memory_mb = max_memory_mb
        self.current_memory_usage = 0
        self.memory_stats = {
            'peak_usage': 0,
            'gc_collections': 0,
            'memory_warnings': 0,
            'oom_preventions': 0
        }
        
        # 内存监控
        self.memory_monitor = MemoryMonitor(
            warning_threshold=max_memory_mb * 0.8,
            critical_threshold=max_memory_mb * 0.9
        )
    
    async def execute_memory_efficient_sync(self, sync_operation):
        """执行内存高效的同步操作"""
        
        # 预检查内存状态
        initial_memory = self._get_current_memory_usage()
        
        try:
            # 🔑 流式处理策略
            async for batch in self._streaming_batch_processor(sync_operation):
                
                # 内存检查
                current_memory = self._get_current_memory_usage()
                if current_memory > self.max_memory_mb * 0.8:
                    logger.warning(f"High memory usage: {current_memory}MB")
                    await self._emergency_memory_cleanup()
                
                # 处理批次
                batch_result = await self._process_batch_with_memory_control(batch)
                
                # 立即清理
                del batch
                del batch_result
                
                # 定期强制垃圾回收
                if self.memory_stats['gc_collections'] % 10 == 0:
                    gc.collect()
                    self.memory_stats['gc_collections'] += 1
            
            # 最终内存清理
            await self._final_memory_cleanup()
            
            return {
                'success': True,
                'memory_stats': self.memory_stats,
                'peak_memory_usage': self.memory_stats['peak_usage']
            }
            
        except MemoryError as e:
            logger.error(f"Memory error during sync: {e}")
            await self._emergency_memory_recovery()
            raise
        
        finally:
            # 确保内存清理
            gc.collect()
    
    async def _streaming_batch_processor(self, sync_operation):
        """流式批次处理器"""
        
        batch_size = self._calculate_optimal_batch_size()
        current_batch = []
        
        async for item in sync_operation.get_items_stream():
            
            # 估算项目内存使用
            item_memory = self._estimate_item_memory_usage(item)
            
            # 检查是否需要创建新批次
            if (len(current_batch) >= batch_size or 
                self._get_batch_memory_usage(current_batch) + item_memory > 
                self.max_memory_mb * 0.1):  # 单批次不超过10%内存
                
                if current_batch:
                    yield current_batch
                    current_batch = []
            
            current_batch.append(item)
        
        # 处理最后一个批次
        if current_batch:
            yield current_batch
    
    def _calculate_optimal_batch_size(self):
        """计算最优批次大小"""
        
        available_memory = self.max_memory_mb - self._get_current_memory_usage()
        
        # 基于可用内存动态调整
        if available_memory > 500:
            return 100  # 大批次
        elif available_memory > 200:
            return 50   # 中批次
        else:
            return 20   # 小批次
    
    def _estimate_item_memory_usage(self, item):
        """估算项目内存使用量（MB）"""
        
        base_size = 0.1  # 基础大小 100KB
        
        # 根据项目类型调整
        if item.get('type') == 'files':
            # 文件元数据
            base_size += 0.05
            
            # 版本信息
            versions = item.get('versions', [])
            base_size += len(versions) * 0.02
            
            # 自定义属性
            custom_attrs = item.get('custom_attributes', [])
            base_size += len(custom_attrs) * 0.01
            
            # 大文件额外开销
            file_size = item.get('attributes', {}).get('fileSize', 0)
            if file_size > 10 * 1024 * 1024:  # 10MB以上
                base_size += 0.1
        
        return base_size
    
    async def _emergency_memory_cleanup(self):
        """紧急内存清理"""
        
        logger.warning("Executing emergency memory cleanup")
        
        # 强制垃圾回收
        gc.collect()
        
        # 清理缓存
        if hasattr(self, 'cache'):
            self.cache.clear()
        
        # 等待内存释放
        await asyncio.sleep(0.1)
        
        self.memory_stats['memory_warnings'] += 1
        
        # 检查清理效果
        current_memory = self._get_current_memory_usage()
        if current_memory > self.max_memory_mb * 0.9:
            logger.error(f"Emergency cleanup failed, memory still high: {current_memory}MB")
            self.memory_stats['oom_preventions'] += 1
            raise MemoryError("Unable to free sufficient memory")
```

#### 性能监控系统

```python
class UniversalPerformanceMonitor:
    """通用性能监控系统"""
    
    def __init__(self):
        self.metrics = {
            'api_performance': {
                'total_calls': 0,
                'successful_calls': 0,
                'failed_calls': 0,
                'average_response_time': 0,
                'calls_saved_by_optimization': 0
            },
            
            'database_performance': {
                'total_operations': 0,
                'batch_operations': 0,
                'single_operations': 0,
                'average_operation_time': 0,
                'connection_pool_usage': 0
            },
            
            'sync_performance': {
                'total_items_processed': 0,
                'items_per_second': 0,
                'smart_skips': 0,
                'skip_efficiency_percentage': 0,
                'total_sync_time': 0
            },
            
            'resource_usage': {
                'peak_memory_usage_mb': 0,
                'average_cpu_usage': 0,
                'peak_concurrent_operations': 0,
                'network_bytes_transferred': 0
            },
            
            'error_statistics': {
                'total_errors': 0,
                'api_errors': 0,
                'database_errors': 0,
                'memory_errors': 0,
                'recovery_success_rate': 0
            }
        }
        
        self.start_time = None
        self.monitoring_active = False
    
    def start_monitoring(self):
        """开始性能监控"""
        self.start_time = time.time()
        self.monitoring_active = True
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """停止性能监控"""
        if self.start_time:
            total_time = time.time() - self.start_time
            self.metrics['sync_performance']['total_sync_time'] = total_time
            
            # 计算派生指标
            self._calculate_derived_metrics()
        
        self.monitoring_active = False
        logger.info("Performance monitoring stopped")
        
        return self.get_performance_report()
    
    def record_api_call(self, success=True, response_time=0):
        """记录API调用"""
        self.metrics['api_performance']['total_calls'] += 1
        
        if success:
            self.metrics['api_performance']['successful_calls'] += 1
        else:
            self.metrics['api_performance']['failed_calls'] += 1
        
        # 更新平均响应时间
        current_avg = self.metrics['api_performance']['average_response_time']
        total_calls = self.metrics['api_performance']['total_calls']
        
        new_avg = ((current_avg * (total_calls - 1)) + response_time) / total_calls
        self.metrics['api_performance']['average_response_time'] = new_avg
    
    def record_smart_skip(self, items_skipped=1):
        """记录智能跳过"""
        self.metrics['sync_performance']['smart_skips'] += items_skipped
        self.metrics['api_performance']['calls_saved_by_optimization'] += items_skipped * 2.5
    
    def record_database_operation(self, is_batch=False, operation_time=0):
        """记录数据库操作"""
        self.metrics['database_performance']['total_operations'] += 1
        
        if is_batch:
            self.metrics['database_performance']['batch_operations'] += 1
        else:
            self.metrics['database_performance']['single_operations'] += 1
        
        # 更新平均操作时间
        current_avg = self.metrics['database_performance']['average_operation_time']
        total_ops = self.metrics['database_performance']['total_operations']
        
        new_avg = ((current_avg * (total_ops - 1)) + operation_time) / total_ops
        self.metrics['database_performance']['average_operation_time'] = new_avg
    
    def _calculate_derived_metrics(self):
        """计算派生指标"""
        
        # 同步性能指标
        total_time = self.metrics['sync_performance']['total_sync_time']
        total_items = self.metrics['sync_performance']['total_items_processed']
        
        if total_time > 0:
            self.metrics['sync_performance']['items_per_second'] = total_items / total_time
        
        # 跳过效率
        total_potential_items = (
            total_items + self.metrics['sync_performance']['smart_skips']
        )
        if total_potential_items > 0:
            skip_efficiency = (
                self.metrics['sync_performance']['smart_skips'] / 
                total_potential_items * 100
            )
            self.metrics['sync_performance']['skip_efficiency_percentage'] = skip_efficiency
        
        # 错误恢复率
        total_errors = self.metrics['error_statistics']['total_errors']
        if total_errors > 0:
            # 假设成功处理的项目数反映了恢复成功率
            recovery_rate = (total_items / (total_items + total_errors)) * 100
            self.metrics['error_statistics']['recovery_success_rate'] = recovery_rate
    
    def get_performance_report(self):
        """生成性能报告"""
        
        return {
            'summary': {
                'total_sync_time': f"{self.metrics['sync_performance']['total_sync_time']:.2f}s",
                'items_processed': self.metrics['sync_performance']['total_items_processed'],
                'processing_speed': f"{self.metrics['sync_performance']['items_per_second']:.2f} items/s",
                'skip_efficiency': f"{self.metrics['sync_performance']['skip_efficiency_percentage']:.1f}%",
                'api_calls_saved': self.metrics['api_performance']['calls_saved_by_optimization']
            },
            
            'api_performance': {
                'total_calls': self.metrics['api_performance']['total_calls'],
                'success_rate': f"{(self.metrics['api_performance']['successful_calls'] / max(self.metrics['api_performance']['total_calls'], 1)) * 100:.1f}%",
                'average_response_time': f"{self.metrics['api_performance']['average_response_time']:.3f}s"
            },
            
            'database_performance': {
                'total_operations': self.metrics['database_performance']['total_operations'],
                'batch_ratio': f"{(self.metrics['database_performance']['batch_operations'] / max(self.metrics['database_performance']['total_operations'], 1)) * 100:.1f}%",
                'average_operation_time': f"{self.metrics['database_performance']['average_operation_time']:.3f}s"
            },
            
            'resource_usage': self.metrics['resource_usage'],
            'error_statistics': self.metrics['error_statistics'],
            'detailed_metrics': self.metrics
        }
```

## 🔧 实施指南

### 部署策略

```python
# 通用部署配置
DEPLOYMENT_STRATEGY = {
    "阶段1_基础优化": {
        "目标": "实施智能分支跳过和基础批量操作",
        "预期提升": "50-80%",
        "风险": "低",
        "实施时间": "1-2周",
        "回退方案": "保留原有同步方法"
    },
    
    "阶段2_数据库优化": {
        "目标": "实施数据库层批量操作和索引优化",
        "预期提升": "80-150%",
        "风险": "中",
        "实施时间": "2-3周",
        "回退方案": "数据库版本回滚"
    },
    
    "阶段3_并发优化": {
        "目标": "实施多层并发处理",
        "预期提升": "150-300%",
        "风险": "中高",
        "实施时间": "3-4周",
        "回退方案": "降级到单线程处理"
    },
    
    "阶段4_高级优化": {
        "目标": "内存管理和性能监控",
        "预期提升": "300-500%",
        "风险": "低",
        "实施时间": "2-3周",
        "回退方案": "禁用高级特性"
    }
}
```

### 配置管理

```python
class UniversalOptimizationConfig:
    """通用优化配置管理"""
    
    def __init__(self, environment='production'):
        self.environment = environment
        self.config = self._load_environment_config()
    
    def _load_environment_config(self):
        """加载环境特定配置"""
        
        base_config = {
            'api_optimization': {
                'batch_sizes': {
                    'list_items': 50,
                    'custom_attributes': 50,
                    'folder_contents': 20
                },
                'concurrent_limits': {
                    'max_api_concurrent': 8,
                    'api_timeout': 30,
                    'retry_count': 3
                }
            },
            
            'database_optimization': {
                'connection_pool': {
                    'min_connections': 5,
                    'max_connections': 20,
                    'connection_timeout': 30
                },
                'batch_sizes': {
                    'files': 100,
                    'folders': 150,
                    'custom_attributes': 200
                }
            },
            
            'concurrent_processing': {
                'max_workers': 12,
                'semaphore_limits': {
                    'api_calls': 8,
                    'db_operations': 15,
                    'data_processing': 10
                }
            },
            
            'memory_management': {
                'max_memory_mb': 1024,
                'gc_threshold': 0.8,
                'emergency_cleanup_threshold': 0.9
            }
        }
        
        # 环境特定调整
        if self.environment == 'development':
            # 开发环境：较小的并发度和批次大小
            base_config['concurrent_processing']['max_workers'] = 4
            base_config['database_optimization']['batch_sizes']['files'] = 20
            base_config['memory_management']['max_memory_mb'] = 512
            
        elif self.environment == 'testing':
            # 测试环境：中等配置
            base_config['concurrent_processing']['max_workers'] = 6
            base_config['database_optimization']['batch_sizes']['files'] = 50
            base_config['memory_management']['max_memory_mb'] = 768
            
        elif self.environment == 'production':
            # 生产环境：最大性能配置
            base_config['concurrent_processing']['max_workers'] = 16
            base_config['database_optimization']['batch_sizes']['files'] = 200
            base_config['memory_management']['max_memory_mb'] = 2048
        
        return base_config
    
    def get_config(self, section=None):
        """获取配置"""
        if section:
            return self.config.get(section, {})
        return self.config
    
    def update_config(self, section, updates):
        """更新配置"""
        if section in self.config:
            self.config[section].update(updates)
        else:
            self.config[section] = updates
```

## 📈 性能基准测试

### 测试场景设计

```python
PERFORMANCE_BENCHMARKS = {
    "小型项目": {
        "规模": "100个文件夹，1000个文件",
        "自定义属性": "平均每文件5个属性",
        "预期提升": {
            "智能跳过": "60-80%",
            "批量API": "200-300%",
            "数据库优化": "150-250%",
            "并发处理": "300-400%",
            "整体提升": "400-600%"
        }
    },
    
    "中型项目": {
        "规模": "500个文件夹，10000个文件",
        "自定义属性": "平均每文件8个属性",
        "预期提升": {
            "智能跳过": "70-85%",
            "批量API": "300-500%",
            "数据库优化": "200-350%",
            "并发处理": "400-600%",
            "整体提升": "500-800%"
        }
    },
    
    "大型项目": {
        "规模": "2000个文件夹，50000个文件",
        "自定义属性": "平均每文件12个属性",
        "预期提升": {
            "智能跳过": "80-90%",
            "批量API": "500-800%",
            "数据库优化": "300-500%",
            "并发处理": "600-1000%",
            "整体提升": "800-1500%"
        }
    },
    
    "超大型项目": {
        "规模": "10000个文件夹，200000个文件",
        "自定义属性": "平均每文件15个属性",
        "预期提升": {
            "智能跳过": "85-95%",
            "批量API": "800-1200%",
            "数据库优化": "500-800%",
            "并发处理": "1000-2000%",
            "整体提升": "1500-3000%"
        }
    }
}
```

## 🎯 最佳实践总结

### 关键成功因素

1. **🔑 智能分支跳过是核心**
   - `last_modified_time_rollup` 是最重要的优化字段
   - 正确实施可节省90%+的API调用
   - 必须处理时间解析异常和边界情况

2. **🚀 批量操作是基础**
   - API批量调用减少网络开销
   - 数据库批量操作提升IO性能
   - 必须实施完善的错误处理和回退机制

3. **⚡ 并发处理是倍增器**
   - 合理的并发度设计
   - 资源池管理避免竞争
   - 错误隔离保证稳定性

4. **💾 内存管理是保障**
   - 流式处理避免内存积累
   - 及时清理和垃圾回收
   - 监控和预警机制

5. **📊 监控是持续改进的基础**
   - 详细的性能指标收集
   - 实时监控和告警
   - 基于数据的优化调整

### 实施建议

1. **渐进式部署**: 分阶段实施，逐步验证效果
2. **完善监控**: 建立全面的性能监控体系
3. **错误处理**: 实施多层回退机制
4. **配置管理**: 支持不同环境的配置调整
5. **文档维护**: 保持技术文档的及时更新

这个通用优化策略为不同数据库方案提供了统一的优化框架，确保在任何技术栈下都能获得显著的性能提升。

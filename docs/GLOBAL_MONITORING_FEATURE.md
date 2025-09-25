# 全局监测面板功能说明

## 功能概述

为了解决 Data Connector 监测列表在退出页面时丢失的问题，我们实现了一个全局监测面板功能。该功能在所有页面的右下角显示一个浮动按钮，点击后可以查看和管理所有监测中的 Data Connector 请求。

## 实现的功能

### 1. 全局浮动按钮
- 位置：所有页面右下角
- 图标：眼睛图标（监测象征）
- 徽章：显示当前监测中的请求数量
- 交互：点击打开全局监测面板

### 2. 持久化存储
- 使用 `localStorage` 存储监测数据
- 数据包括：监测中的请求、已完成的请求
- 页面刷新或重新打开时数据不会丢失

### 3. 全局监测面板
- **监测中标签页**：显示正在监测的请求
- **已完成标签页**：显示已完成下载的请求
- **操作功能**：
  - 开始/停止自动监测
  - 刷新全部请求状态
  - 单个请求状态检查
  - 移除监测
  - 清除已完成请求

### 4. 自动监测功能
- 每30秒自动检查监测中的请求状态
- 自动下载完成的数据文件
- 完成后自动移动到已完成列表

### 5. 组件间通信
- 使用事件总线（Event Bus）实现组件间通信
- Data Connector 页面的操作会同步到全局面板
- 支持添加、移除监测请求的实时同步

## 技术实现

### 文件结构
```
frontend/src/
├── components/
│   └── GlobalMonitoringPanel.vue    # 全局监测面板组件
├── utils/
│   └── eventBus.js                  # 事件总线
├── views/
│   └── DataConnectorSync.vue        # 更新的 Data Connector 页面
├── App.vue                          # 集成全局组件
└── main.js                          # 注册事件总线
```

### 关键技术点

1. **事件总线**：实现跨组件通信
   ```javascript
   // 发送事件
   this.$eventBus.emit('add-to-global-monitoring', requestData)
   
   // 监听事件
   this.$eventBus.on('add-to-global-monitoring', this.addToMonitoring)
   ```

2. **持久化存储**：
   ```javascript
   const STORAGE_KEY = 'global_monitoring_data'
   localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
   ```

3. **自动监测**：
   ```javascript
   this.monitoringTimer = setInterval(() => {
     this.performAutoCheck()
   }, 30000)
   ```

## 使用方法

### 对用户
1. 在 Data Connector 页面创建数据请求后，请求会自动加入全局监测
2. 也可以手动点击"加入监测"按钮添加现有请求
3. 切换到其他页面时，监测数据不会丢失
4. 点击右下角浮动按钮查看所有监测状态
5. 在全局面板中管理所有监测请求

### 对开发者
1. 全局监测面板会自动显示在已认证用户的所有页面
2. 通过事件总线可以轻松扩展到其他模块
3. 存储格式标准化，便于维护和扩展

## 数据格式

### 监测请求数据结构
```javascript
{
  id: "request_id",
  description: "请求描述",
  projectName: "项目名称",
  addedAt: "2024-01-01T00:00:00.000Z",
  lastChecked: "2024-01-01T00:00:00.000Z",
  status: "monitoring", // monitoring | completed | error
  checking: false,
  downloadedFiles: 0
}
```

### 存储数据结构
```javascript
{
  monitoringRequests: [...],
  completedRequests: [...],
  isMonitoring: false,
  lastSaved: "2024-01-01T00:00:00.000Z"
}
```

## 优势

1. **数据持久化**：解决了页面切换时数据丢失的问题
2. **全局访问**：在任何页面都可以查看监测状态
3. **自动化**：无需手动检查，自动监测和下载
4. **用户友好**：直观的界面和实时状态更新
5. **可扩展**：架构支持未来功能扩展

## 注意事项

1. 监测数据存储在浏览器本地，清除浏览器数据会丢失监测列表
2. 自动监测需要用户手动启动（不会自动恢复上次的监测状态）
3. 文件下载依赖浏览器的下载功能
4. 建议定期清理已完成的请求以避免存储空间过大

## 未来扩展

1. 支持监测其他类型的异步任务
2. 添加更多的通知方式（邮件、桌面通知等）
3. 支持监测数据的导出和导入
4. 添加监测历史记录和统计功能

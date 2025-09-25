<template>
  <div>
    <!-- 右下角浮动按钮 -->
    <div class="floating-monitor-button" @click="togglePanel" v-if="!showPanel">
      <el-badge :value="monitoringCount" :hidden="monitoringCount === 0" type="primary">
        <el-button type="primary" circle size="large" class="monitor-btn">
          <IconEye />
        </el-button>
      </el-badge>
    </div>

    <!-- 监测面板弹窗 -->
    <el-dialog 
      v-model="showPanel" 
      width="900px"
      :close-on-click-modal="false"
      :before-close="handleClose">
      
      <template #header>
        <div class="dialog-header">
          <span class="dialog-title">🤖 Data Connector 监测中心</span>
          <!-- 帮助图标移到标题右侧 -->
          <div class="title-help-icon" v-if="monitoringRequests.length > 0">
            <el-tooltip placement="bottom" effect="light" popper-class="help-tooltip">
              <template #content>
                <div class="help-tooltip-content">
                  <h4>💡 Data Connector 执行说明</h4>
                  <div class="help-section">
                    <p><strong>⏰ 执行时间说明：</strong></p>
                    <ul>
                      <li><strong>0-30分钟：</strong>等待ACC系统调度，这是正常的等待期</li>
                      <li><strong>30分钟-2小时：</strong>系统可能开始创建执行作业</li>
                      <li><strong>作业执行：</strong>实际数据提取过程，通常5-15分钟</li>
                      <li><strong>完成下载：</strong>文件准备好后会自动下载</li>
                    </ul>
                  </div>
                  <div class="help-section">
                    <p><strong>📊 状态说明：</strong></p>
                    <ul>
                      <li><span class="status-demo waiting">等待调度</span> - 请求已创建，等待系统调度</li>
                      <li><span class="status-demo pending">等待执行</span> - 作业已创建，等待执行</li>
                      <li><span class="status-demo running">执行中</span> - 作业正在执行</li>
                      <li><span class="status-demo completed">已完成</span> - 执行完成并已下载</li>
                    </ul>
                  </div>
                  <p class="help-tip"><strong>💡 提示：</strong>如果超过24小时仍显示"等待调度"，可能需要检查请求配置</p>
                </div>
              </template>
              <el-icon class="help-icon" size="16">
                <IconQuestionCircle />
              </el-icon>
            </el-tooltip>
          </div>
        </div>
      </template>
      
      <div class="monitor-panel">
        <!-- 顶部统计信息 -->
        <div class="monitor-stats">
          <el-row :gutter="16">
            <el-col :span="8">
              <el-card class="stat-card">
                <el-statistic title="监测中" :value="monitoringCount" suffix="个请求" />
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="stat-card">
                <el-statistic title="已完成" :value="completedCount" suffix="个请求" />
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="stat-card">
                <el-statistic title="总计" :value="totalCount" suffix="个请求" />
              </el-card>
            </el-col>
          </el-row>
        </div>

        <!-- 操作按钮 -->
        <div class="monitor-actions">
          <el-button 
            :type="isMonitoring ? 'danger' : 'success'" 
            @click="toggleMonitoring"
            :loading="loading">
            <IconPlayArrowFill v-if="!isMonitoring" />
            <IconPause v-else />
            {{ isMonitoring ? '停止监测' : '开始监测' }}
          </el-button>
          <el-button @click="refreshAll" :loading="refreshing">
            <IconRefresh />
            刷新全部
          </el-button>
          <el-button @click="clearCompleted" type="warning">
            <IconDelete />
            清除已完成
          </el-button>
          <el-button @click="showRequestDetails" type="info" v-if="monitoringRequests.length > 0">
            📋 查看详情
          </el-button>
        </div>


        <!-- 监测列表 -->
        <div class="monitor-list">
          <el-tabs v-model="activeTab" type="card">
            <!-- 监测中的请求 -->
            <el-tab-pane label="监测中" name="monitoring">
              <div v-if="monitoringRequests.length > 0">
                <el-table :data="monitoringRequests" style="width: 100%" stripe>
                  <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
                  <el-table-column prop="projectName" label="项目" width="150" show-overflow-tooltip />
                  <el-table-column prop="createdAt" label="创建时间" width="160">
                    <template #default="scope">
                      {{ formatDate(scope.row.createdAt) }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="lastChecked" label="最后检查" width="160">
                    <template #default="scope">
                      {{ scope.row.lastChecked ? formatDate(scope.row.lastChecked) : '未检查' }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="status" label="状态" width="140">
                    <template #default="scope">
                      <el-tag 
                        :type="getStatusType(scope.row.status)" 
                        size="small">
                        {{ getStatusText(scope.row.status, scope.row.statusText) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="150" fixed="right">
                    <template #default="scope">
                      <el-button 
                        type="text" 
                        size="small" 
                        @click="checkSingleRequest(scope.row)"
                        :loading="scope.row.checking">
                        <IconRefresh />
                        检查
                      </el-button>
                      <el-button 
                        type="text" 
                        size="small" 
                        @click="removeFromMonitoring(scope.row.id)" 
                        style="color: #f56c6c;">
                        移除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
              <div v-else>
                <el-empty description="暂无监测中的请求">
                  <template #description>
                    <p>暂无监测中的请求</p>
                    <p>请前往 Data Connector 页面创建请求并加入监测</p>
                  </template>
                  <template #default>
                    <el-button type="primary" @click="goToDataConnector">
                      前往 Data Connector
                    </el-button>
                  </template>
                </el-empty>
              </div>
            </el-tab-pane>

            <!-- 已完成的请求 -->
            <el-tab-pane label="已完成" name="completed">
              <div v-if="completedRequests.length > 0">
                <el-table :data="completedRequests" style="width: 100%" stripe>
                  <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
                  <el-table-column prop="projectName" label="项目" width="150" show-overflow-tooltip />
                  <el-table-column prop="completedAt" label="完成时间" width="160">
                    <template #default="scope">
                      {{ formatDate(scope.row.completedAt) }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="downloadedFiles" label="下载文件" width="120">
                    <template #default="scope">
                      <el-tag type="success" size="small">
                        {{ scope.row.downloadedFiles || 0 }} 个文件
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="100" fixed="right">
                    <template #default="scope">
                      <el-button 
                        type="text" 
                        size="small" 
                        @click="removeCompleted(scope.row.id)" 
                        style="color: #f56c6c;">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
              <div v-else>
                <el-empty description="暂无已完成的请求" />
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClose">关闭</el-button>
          <el-button type="primary" @click="handleClose">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { 
  IconEye, 
  IconPlayArrowFill, 
  IconPause, 
  IconRefresh, 
  IconDelete,
  IconQuestionCircle
} from '@arco-design/web-vue/es/icon'
import axios from 'axios'

export default {
  name: 'GlobalMonitoringPanel',
  components: {
    IconEye,
    IconPlayArrowFill,
    IconPause,
    IconRefresh,
    IconDelete,
    IconQuestionCircle
  },
  data() {
    return {
      showPanel: false,
      activeTab: 'monitoring',
      loading: false,
      refreshing: false,
      
      // 监测数据
      monitoringRequests: [],
      completedRequests: [],
      
      // 自动监测
      isMonitoring: false,
      monitoringTimer: null,
      monitorInterval: 30000, // 默认30秒，从配置API获取
      
      // 项目信息缓存
      projectsCache: {},
      projectsCacheLoaded: false,
      
      // 存储键名
      STORAGE_KEY: 'global_monitoring_data',
      PROJECTS_CACHE_KEY: 'global_monitoring_projects_cache'
    }
  },
  
  computed: {
    monitoringCount() {
      return this.monitoringRequests.length
    },
    
    completedCount() {
      return this.completedRequests.length
    },
    
    totalCount() {
      return this.monitoringCount + this.completedCount
    }
  },
  
  async mounted() {
    // 首先加载监测配置
    await this.loadMonitoringConfig()
    
    // 从localStorage加载项目信息缓存
    this.loadProjectsCache()
    
    this.loadFromStorage()
    
    // 更新现有请求的项目名称
    this.updateExistingProjectNames()
    
    // 监听来自其他组件的事件
    this.$eventBus?.on('add-to-global-monitoring', this.addToMonitoring)
    this.$eventBus?.on('remove-from-global-monitoring', this.removeFromMonitoring)
    this.$eventBus?.on('projects-cache-updated', this.handleProjectsCacheUpdated)
    
    // 如果有监测中的请求，自动开始监测
    if (this.monitoringRequests.length > 0) {
      this.startMonitoring()
    }
  },
  
  beforeUnmount() {
    this.stopMonitoring()
    this.$eventBus?.off('add-to-global-monitoring', this.addToMonitoring)
    this.$eventBus?.off('remove-from-global-monitoring', this.removeFromMonitoring)
    this.$eventBus?.off('projects-cache-updated', this.handleProjectsCacheUpdated)
  },
  
  methods: {
    togglePanel() {
      this.showPanel = !this.showPanel
    },
    
    handleClose() {
      this.showPanel = false
    },
    
    // 加载监测配置
    async loadMonitoringConfig() {
      try {
        const response = await axios.get('/api/config/monitoring')
        if (response.data.status === 'success') {
          const config = response.data.data
          this.monitorInterval = (config.interval_seconds || 30) * 1000 // 转换为毫秒
          console.log(`📋 监测配置已加载: 间隔 ${config.interval_seconds} 秒`)
        }
      } catch (error) {
        console.error('加载监测配置失败，使用默认值:', error)
        // 保持默认值 30000ms (30秒)
      }
    },
    
    // 从localStorage加载项目缓存
    loadProjectsCache() {
      try {
        const cached = localStorage.getItem(this.PROJECTS_CACHE_KEY)
        
        if (cached) {
          const cacheData = JSON.parse(cached)
          
          if (cacheData.projects && typeof cacheData.projects === 'object') {
            this.projectsCache = { ...cacheData.projects }
            this.projectsCacheLoaded = true
          } else {
            this.projectsCache = {}
            this.projectsCacheLoaded = true
          }
        } else {
          this.projectsCache = {}
          this.projectsCacheLoaded = false
        }
      } catch (error) {
        console.error('加载项目缓存失败:', error)
        this.projectsCache = {}
        this.projectsCacheLoaded = true
      }
    },
    
    // 更新现有请求的项目名称
    updateExistingProjectNames() {
      if (!this.projectsCacheLoaded || Object.keys(this.projectsCache).length === 0) {
        return
      }
      
      let updated = false
      
      // 更新监测中的请求
      this.monitoringRequests.forEach((request) => {
        if (request.projectId && this.projectsCache[request.projectId]) {
          const newName = this.projectsCache[request.projectId]
          if (request.projectName !== newName) {
            request.projectName = newName
            updated = true
          }
        }
      })
      
      // 更新已完成的请求
      this.completedRequests.forEach(request => {
        if (request.projectId && this.projectsCache[request.projectId]) {
          const newName = this.projectsCache[request.projectId]
          if (request.projectName !== newName) {
            request.projectName = newName
            updated = true
          }
        }
      })
      
      if (updated) {
        this.saveToStorage()
      }
    },
    
    // 处理项目缓存更新事件
    handleProjectsCacheUpdated(newProjectsCache) {
      console.log('📡 监测中心收到项目缓存更新事件:', newProjectsCache)
      console.log('📋 项目缓存键值对:', Object.entries(newProjectsCache))
      
      if (newProjectsCache && typeof newProjectsCache === 'object') {
        // 更新本地缓存
        this.projectsCache = { ...newProjectsCache }
        this.projectsCacheLoaded = true
        
        const projectCount = Object.keys(newProjectsCache).length
 
        
        // 立即更新现有请求的项目名称
        this.updateExistingProjectNames()
        
      } else {
        console.warn('⚠️ 监测中心收到的项目缓存数据格式异常:', newProjectsCache)
        
        // 如果接收到的数据异常，重新从localStorage加载
        this.loadProjectsCache()
      }
    },
    
    // 存储管理
    saveToStorage() {
      const data = {
        monitoringRequests: this.monitoringRequests,
        completedRequests: this.completedRequests,
        isMonitoring: this.isMonitoring,
        lastSaved: new Date().toISOString()
      }
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data))
    },
    
    loadFromStorage() {
      try {
        const stored = localStorage.getItem(this.STORAGE_KEY)
        if (stored) {
          const data = JSON.parse(stored)
          this.monitoringRequests = (data.monitoringRequests || []).map(request => {
            // 兼容性处理：将旧的addedAt字段转换为createdAt
            if (request.addedAt && !request.createdAt) {
              request.createdAt = request.addedAt
              delete request.addedAt
            }
            
            // 修复可能存在的状态不一致问题
            if (!request.statusText && request.status) {
              switch (request.status) {
                case 'waiting':
                  const createdTime = new Date(request.createdAt)
                  const now = new Date()
                  const waitingMinutes = Math.floor((now - createdTime) / (1000 * 60))
                  if (waitingMinutes < 30) {
                    request.statusText = `等待调度 (${waitingMinutes}分钟)`
                  } else if (waitingMinutes < 120) {
                    request.statusText = `等待调度 (${Math.floor(waitingMinutes/60)}小时${waitingMinutes%60}分钟)`
                  } else {
                    request.statusText = `等待调度 (${Math.floor(waitingMinutes/60)}小时)`
                  }
                  break
                case 'pending':
                  request.statusText = '等待执行'
                  break
                case 'running':
                  request.statusText = '执行中'
                  break
                case 'error':
                  request.statusText = '检查失败'
                  break
                default:
                  request.statusText = '等待调度'
                  request.status = 'waiting'
              }
            }
            // 确保checking状态为false
            request.checking = false
            return request
          })
          this.completedRequests = data.completedRequests || []
          // 不自动恢复监测状态，需要用户手动启动
        }
      } catch (error) {
        console.error('加载监测数据失败:', error)
      }
    },
    
    // 监测管理
    toggleMonitoring() {
      if (this.isMonitoring) {
        this.stopMonitoring()
      } else {
        this.startMonitoring()
      }
    },
    
    startMonitoring() {
      if (this.monitoringRequests.length === 0) {
        this.$message.warning('没有需要监测的请求')
        return
      }
      
      if (this.monitoringTimer) {
        this.stopMonitoring()
      }
      
      this.isMonitoring = true
      this.monitoringTimer = setInterval(() => {
        this.performAutoCheck()
      }, this.monitorInterval)
      
      this.$message.success('🤖 自动监测已启动')
      this.saveToStorage()
    },
    
    stopMonitoring() {
      if (this.monitoringTimer) {
        clearInterval(this.monitoringTimer)
        this.monitoringTimer = null
      }
      this.isMonitoring = false
      this.$message.info('🤖 自动监测已停止')
      this.saveToStorage()
    },
    
    // 添加到监测
    addToMonitoring(requestData) {
      const existingIndex = this.monitoringRequests.findIndex(req => req.id === requestData.id)
      
      if (existingIndex !== -1) {
        // 更新现有记录，保持原有的状态和时间信息
        this.monitoringRequests[existingIndex] = {
          ...this.monitoringRequests[existingIndex],
          ...requestData,
          createdAt: this.monitoringRequests[existingIndex].createdAt, // 保持原有创建时间
          lastChecked: this.monitoringRequests[existingIndex].lastChecked, // 保持检查时间
          status: this.monitoringRequests[existingIndex].status || 'waiting', // 保持状态
          statusText: this.monitoringRequests[existingIndex].statusText // 保持状态文本
        }
      } else {
        // 尝试从缓存获取项目名称
        
        let projectName = requestData.projectName
        if (requestData.projectId && this.projectsCache[requestData.projectId]) {
          projectName = this.projectsCache[requestData.projectId]
        } else if (!projectName) {
          projectName = '获取中...'
        }
        
        // 添加新记录
        this.monitoringRequests.push({
          id: requestData.id,
          description: requestData.description,
          projectId: requestData.projectId,
          projectName: projectName,
          createdAt: requestData.createdAt || new Date().toISOString(),
          lastChecked: null,
          status: 'waiting',
          statusText: '等待调度 (0分钟)',
          checking: false
        })
        
        // 如果缓存中没有项目名称，异步获取
        if (requestData.projectId && !this.projectsCache[requestData.projectId]) {
          this.fetchProjectName(requestData.projectId, requestData.id)
        }
      }
      
      this.saveToStorage()
      this.$message.success(`已添加到全局监测: "${requestData.description}"`)
    },
    
    // 获取项目名称
    fetchProjectName(projectId, requestId) {
      if (!projectId) return
      
      console.log(`📋 尝试获取项目名称: ${projectId}`)
      
      // 如果缓存未加载，先加载缓存
      if (!this.projectsCacheLoaded) {
        console.log('📋 缓存未加载，重新加载')
        this.loadProjectsCache()
      }
      
      // 检查缓存中是否有该项目
      if (this.projectsCache[projectId]) {
        const projectName = this.projectsCache[projectId]
        console.log(`✅ 找到项目名称: ${projectId} -> ${projectName}`)
        
        const requestIndex = this.monitoringRequests.findIndex(req => req.id === requestId)
        if (requestIndex !== -1) {
          this.monitoringRequests[requestIndex].projectName = projectName
          this.saveToStorage()
          console.log(`✅ 已更新请求 ${requestId} 的项目名称为: ${projectName}`)
        }
      } else {
        console.log(`⚠️ 缓存中未找到项目ID ${projectId} 的名称`)
        console.log('📋 可用的项目ID:', Object.keys(this.projectsCache))
      }
    },
    
    // 从监测中移除
    removeFromMonitoring(requestId) {
      const index = this.monitoringRequests.findIndex(req => req.id === requestId)
      if (index !== -1) {
        this.monitoringRequests.splice(index, 1)
        this.saveToStorage()
        this.$message.success('已从监测列表中移除')
      }
    },
    
    // 移动到已完成
    moveToCompleted(request) {
      // 从监测中移除
      const index = this.monitoringRequests.findIndex(req => req.id === request.id)
      if (index !== -1) {
        this.monitoringRequests.splice(index, 1)
      }
      
      // 添加到已完成
      this.completedRequests.push({
        ...request,
        completedAt: new Date().toISOString(),
        status: 'completed'
      })
      
      this.saveToStorage()
    },
    
    // 单个请求检查
    async checkSingleRequest(request) {
      // 设置checking状态，确保响应式更新
      if (this.$set) {
        this.$set(request, 'checking', true)
      } else {
        request.checking = true
        this.$forceUpdate()
      }
      
      try {
        console.log(`🔍 检查请求 ${request.id}: ${request.description}`)
        const response = await axios.get(`/api/data-connector/requests/${request.id}/jobs`, {
          timeout: 10000 // 10秒超时
        })
        
        if (response.data.status === 'success') {
          const jobs = response.data.jobs.results || []
          console.log(`📋 请求 ${request.id} 找到 ${jobs.length} 个作业`)
          
          request.lastChecked = new Date().toISOString()
          
          if (jobs.length === 0) {
            // 没有作业，分析等待时间
            const createdTime = new Date(request.createdAt)
            const now = new Date()
            const waitingMinutes = Math.floor((now - createdTime) / (1000 * 60))
            
            request.status = 'waiting'
            if (waitingMinutes < 30) {
              request.statusText = `等待调度 (${waitingMinutes}分钟)`
            } else if (waitingMinutes < 120) {
              request.statusText = `等待调度 (${Math.floor(waitingMinutes/60)}小时${waitingMinutes%60}分钟)`
            } else {
              request.statusText = `等待调度 (${Math.floor(waitingMinutes/60)}小时)`
            }
            console.log(`⏰ 请求 ${request.id} 等待调度执行，已等待 ${waitingMinutes} 分钟`)
          } else {
            // 分析作业状态
            const pendingJobs = jobs.filter(job => job.status === 'pending')
            const runningJobs = jobs.filter(job => job.status === 'running')
            const completedJobs = jobs.filter(job => job.status === 'complete' && job.completionStatus === 'success')
            const failedJobs = jobs.filter(job => job.status === 'complete' && job.completionStatus !== 'success')
            
            console.log(`📊 请求 ${request.id} 作业状态: 待执行${pendingJobs.length}, 运行中${runningJobs.length}, 已完成${completedJobs.length}, 失败${failedJobs.length}`)
            
            if (completedJobs.length > 0) {
              // 有完成的作业，尝试下载
              let downloadCount = 0
              for (const job of completedJobs) {
                const downloaded = await this.downloadJobData(job, request)
                if (downloaded) downloadCount++
              }
              
              // 移动到已完成
              request.downloadedFiles = downloadCount
              this.moveToCompleted(request)
              this.$message.success(`🎉 请求 "${request.description}" 已完成并下载 ${downloadCount} 个文件`)
              console.log(`✅ 请求 ${request.id} 完成，下载了 ${downloadCount} 个文件`)
              return // 请求已完成，不需要继续
            } else if (runningJobs.length > 0) {
              request.status = 'running'
              request.statusText = `执行中 (${runningJobs.length}个作业)`
              console.log(`🏃 请求 ${request.id} 执行中`)
            } else if (pendingJobs.length > 0) {
              request.status = 'pending'
              request.statusText = `等待执行 (${pendingJobs.length}个作业)`
              console.log(`⏳ 请求 ${request.id} 等待执行`)
            } else if (failedJobs.length > 0) {
              request.status = 'error'
              request.statusText = `执行失败 (${failedJobs.length}个作业)`
              console.log(`❌ 请求 ${request.id} 执行失败`)
            } else {
              request.status = 'waiting'
              request.statusText = '等待调度'
            }
          }
        } else {
          request.status = 'error'
          request.statusText = '检查失败'
          console.error(`❌ 检查请求 ${request.id} 失败: ${response.data.error}`)
        }
        
        this.saveToStorage()
      } catch (error) {
        request.lastChecked = new Date().toISOString()
        
        // 根据不同的错误类型设置不同的状态
        if (error.response?.status === 400) {
          // 400错误通常表示请求ID无效或请求已过期
          request.status = 'invalid'
          request.statusText = '请求无效'
          console.warn(`⚠️ 请求 ${request.id} 可能已过期或无效 (400错误)`)
        } else if (error.response?.status === 404) {
          // 404错误表示请求不存在
          request.status = 'notfound'
          request.statusText = '请求不存在'
          console.warn(`⚠️ 请求 ${request.id} 未找到 (404错误)`)
        } else if (error.response?.status === 429) {
          // 429错误表示请求过于频繁
          request.status = 'ratelimit'
          request.statusText = '请求频率限制'
          console.warn(`⚠️ 请求 ${request.id} 触发频率限制，稍后重试`)
        } else if (error.code === 'ECONNABORTED') {
          // 超时错误
          request.status = 'timeout'
          request.statusText = '请求超时'
          console.warn(`⚠️ 检查请求 ${request.id} 超时`)
        } else {
          // 其他网络错误
          request.status = 'error'
          request.statusText = '网络错误'
          console.error(`❌ 检查请求 ${request.id} 失败:`, error.response?.data?.error || error.message)
        }
      } finally {
        // 确保checking状态被正确重置
        if (this.$set) {
          this.$set(request, 'checking', false)
        } else {
          request.checking = false
          this.$forceUpdate()
        }
      }
    },
    
    // 批量检查
    async performAutoCheck() {
      for (const request of this.monitoringRequests) {
        if (!request.checking) {
          await this.checkSingleRequest(request)
          // 添加延迟避免请求过于频繁
          await new Promise(resolve => setTimeout(resolve, 1000))
        }
      }
    },
    
    // 下载作业数据
    async downloadJobData(job, request) {
      try {
        // 首先获取文件列表
        const listingResponse = await axios.get(`/api/data-connector/jobs/${job.id}/data-listing`)
        
        if (listingResponse.data.status === 'success') {
          const files = listingResponse.data.files.results || []
          
          if (files.length > 0) {
            // 下载第一个文件（通常是ZIP文件）
            const file = files[0]
            const downloadResponse = await axios.get(`/api/data-connector/jobs/${job.id}/data/${file.fileName}`, {
              responseType: 'blob'
            })
            
            // 创建下载链接
            const url = window.URL.createObjectURL(new Blob([downloadResponse.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', `${request.description}_${job.id}_${file.fileName}`)
            document.body.appendChild(link)
            link.click()
            link.remove()
            window.URL.revokeObjectURL(url)
            
            return true
          }
        }
        
        return false
      } catch (error) {
        console.error('下载数据失败:', error)
        return false
      }
    },
    
    // 刷新所有
    async refreshAll() {
      if (this.monitoringRequests.length === 0) {
        this.$message.info('没有需要刷新的请求')
        return
      }
      
      this.refreshing = true
      try {
        await this.performAutoCheck()
        this.$message.success('已刷新所有监测请求')
      } catch (error) {
        this.$message.error('刷新失败: ' + error.message)
      } finally {
        this.refreshing = false
      }
    },
    
    // 清除已完成
    clearCompleted() {
      if (this.completedRequests.length === 0) {
        this.$message.info('没有已完成的请求需要清除')
        return
      }
      
      this.$confirm('确定要清除所有已完成的请求吗？', '确认清除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.completedRequests = []
        this.saveToStorage()
        this.$message.success('已清除所有已完成的请求')
      }).catch(() => {
        // 用户取消
      })
    },
    
    // 删除单个已完成请求
    removeCompleted(requestId) {
      const index = this.completedRequests.findIndex(req => req.id === requestId)
      if (index !== -1) {
        this.completedRequests.splice(index, 1)
        this.saveToStorage()
      }
    },
    
    // 前往 Data Connector 页面
    goToDataConnector() {
      this.$router.push('/data-connector/sync')
      this.handleClose()
    },

    // 显示请求详情
    async showRequestDetails() {
      try {
        // 构建HTML内容
        let htmlContent = '<div class="request-details-container">'
        
        for (let i = 0; i < this.monitoringRequests.length; i++) {
          const request = this.monitoringRequests[i]
          const createdTime = new Date(request.createdAt)
          const now = new Date()
          const waitingMinutes = Math.floor((now - createdTime) / (1000 * 60))
          
          // 获取实时作业信息
          let jobInfo = '正在获取...'
          let analysis = ''
          
          try {
            const response = await axios.get(`/api/data-connector/requests/${request.id}/jobs`)
            if (response.data.status === 'success') {
              const jobs = response.data.jobs.results || []
              
              if (jobs.length === 0) {
                jobInfo = '暂无作业'
                if (waitingMinutes < 30) {
                  analysis = '✅ 正常等待期，ACC通常需要30分钟以上才开始调度'
                } else if (waitingMinutes < 120) {
                  analysis = '⏳ 仍在等待调度，这可能需要更长时间'
                } else {
                  analysis = '⚠️ 等待时间较长，建议检查请求配置'
                }
              } else {
                const statusCounts = {}
                jobs.forEach(job => {
                  const key = `${job.status}${job.completionStatus ? `(${job.completionStatus})` : ''}`
                  statusCounts[key] = (statusCounts[key] || 0) + 1
                })
                jobInfo = Object.entries(statusCounts).map(([status, count]) => `${status}: ${count}个`).join(', ')
                analysis = '📊 作业已创建，正在执行中'
              }
            } else {
              jobInfo = '获取失败'
              analysis = '❌ 无法获取作业信息'
            }
          } catch (error) {
            jobInfo = '网络错误'
            analysis = '🔌 网络连接异常，请检查网络状态'
          }
          
          htmlContent += `
            <div class="request-detail-card">
              <h4 class="detail-title">
                <span class="detail-index">${i + 1}. </span>
                <span>${request.description || 'Data Extract Request'}</span>
              </h4>
              <div class="detail-grid">
                <div class="detail-item">
                  <span class="detail-label">请求ID:</span>
                  <code class="detail-value">${request.id}</code>
                </div>
                <div class="detail-item">
                  <span class="detail-label">项目:</span>
                  <span class="detail-value">${request.projectName || '未知项目'}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">当前状态:</span>
                  <span class="detail-status ${request.status || 'waiting'}">${request.statusText || '等待调度'}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">等待时间:</span>
                  <span class="detail-value">${waitingMinutes} 分钟</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">作业信息:</span>
                  <span class="detail-value">${jobInfo}</span>
                </div>
                <div class="detail-item full-width">
                  <span class="detail-label">状态分析:</span>
                  <span class="detail-analysis">${analysis}</span>
                </div>
              </div>
            </div>
          `
        }
        
        // 添加系统信息
        htmlContent += `
          <div class="system-info">
            <h4>🤖 系统状态</h4>
            <div class="system-grid">
              <div class="system-item">
                <span class="system-label">自动监测:</span>
                <span class="system-value ${this.isMonitoring ? 'active' : 'inactive'}">${this.isMonitoring ? '运行中' : '已停止'}</span>
              </div>
              <div class="system-item">
                <span class="system-label">检查间隔:</span>
                <span class="system-value">${this.monitorInterval / 1000}秒</span>
              </div>
              <div class="system-item">
                <span class="system-label">监测请求:</span>
                <span class="system-value">${this.monitoringRequests.length}个</span>
              </div>
            </div>
          </div>
        `
        
        htmlContent += '</div>'
        
        this.$msgbox({
          title: '📋 监测详情',
          dangerouslyUseHTMLString: true,
          message: htmlContent,
          confirmButtonText: '关闭',
          type: 'info',
          customClass: 'request-details-dialog'
        })
      } catch (error) {
        console.error('显示详情失败:', error)
        this.$message.error('无法显示详情信息')
      }
    },
    
    // 工具方法
    formatDate(dateStr) {
      if (!dateStr) return '未知'
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN')
    },
    
    getStatusType(status) {
      switch (status) {
        case 'monitoring': return 'primary'
        case 'waiting': return 'warning'
        case 'pending': return 'warning'
        case 'running': return 'primary'
        case 'completed': return 'success'
        case 'error': return 'danger'
        case 'invalid': return 'warning'
        case 'notfound': return 'info'
        case 'ratelimit': return 'warning'
        case 'timeout': return 'danger'
        default: return 'info'
      }
    },
    
    getStatusText(status, statusText) {
      // 如果有自定义状态文本，使用它
      if (statusText) {
        return statusText
      }
      
      // 否则使用默认状态文本
      switch (status) {
        case 'monitoring': return '监测中'
        case 'waiting': return '等待调度'
        case 'pending': return '等待执行'
        case 'running': return '执行中'
        case 'completed': return '已完成'
        case 'error': return '错误'
        case 'invalid': return '请求无效'
        case 'notfound': return '请求不存在'
        case 'ratelimit': return '请求频率限制'
        case 'timeout': return '请求超时'
        default: return '未知'
      }
    }
  }
}
</script>

<style scoped>
.floating-monitor-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
  cursor: pointer;
}

.monitor-btn {
  width: 60px !important;
  height: 60px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.monitor-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.monitor-panel {
  padding: 0;
}

.monitor-stats {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.monitor-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

/* 对话框标题头部样式 */
.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.dialog-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.title-help-icon {
  margin-left: 12px;
}

.help-icon {
  color: #909399;
  cursor: help;
  transition: color 0.3s;
}

.help-icon:hover {
  color: #409eff;
}

/* 帮助提示框样式 */
:deep(.help-tooltip) {
  max-width: 400px !important;
}

.help-tooltip-content {
  padding: 12px;
}

.help-tooltip-content h4 {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 14px;
}

.help-section {
  margin: 12px 0;
}

.help-section p {
  margin: 8px 0;
  font-weight: 600;
  color: #606266;
}

.help-section ul {
  margin: 8px 0;
  padding-left: 16px;
}

.help-section li {
  margin: 4px 0;
  line-height: 1.4;
  font-size: 13px;
}

.help-tip {
  margin-top: 12px;
  padding: 8px;
  background: #f0f9ff;
  border-radius: 4px;
  font-size: 12px;
  color: #0369a1;
}

.status-demo {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  margin-right: 8px;
}

.status-demo.waiting {
  background: #fef3c7;
  color: #92400e;
}

.status-demo.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-demo.running {
  background: #dbeafe;
  color: #1e40af;
}

.status-demo.completed {
  background: #d1fae5;
  color: #065f46;
}

/* 详情对话框样式 */
:deep(.request-details-dialog) {
  width: 80% !important;
  max-width: 800px !important;
}

:deep(.request-details-dialog .el-message-box__message) {
  padding: 0 !important;
}

.request-details-container {
  max-height: 60vh;
  overflow-y: auto;
}

.request-detail-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background: #fafafa;
}

.detail-title {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 16px;
}

.detail-index {
  color: #409eff;
  font-weight: 700;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-label {
  font-size: 12px;
  color: #909399;
  font-weight: 600;
}

.detail-value {
  font-size: 13px;
  color: #303133;
}

.detail-value code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
}

.detail-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.detail-status.waiting {
  background: #fef3c7;
  color: #92400e;
}

.detail-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.detail-status.running {
  background: #dbeafe;
  color: #1e40af;
}

.detail-status.error {
  background: #fee2e2;
  color: #dc2626;
}

.detail-status.invalid {
  background: #fef3c7;
  color: #b45309;
}

.detail-status.notfound {
  background: #f3f4f6;
  color: #6b7280;
}

.detail-status.ratelimit {
  background: #fef3c7;
  color: #d97706;
}

.detail-status.timeout {
  background: #fee2e2;
  color: #dc2626;
}

.detail-analysis {
  font-size: 13px;
  line-height: 1.4;
  color: #606266;
  padding: 8px;
  background: #f0f9ff;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}

.system-info {
  border-top: 2px solid #e4e7ed;
  padding-top: 16px;
  margin-top: 16px;
}

.system-info h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

.system-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.system-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.system-label {
  font-size: 12px;
  color: #909399;
  font-weight: 600;
}

.system-value {
  font-size: 13px;
  color: #303133;
}

.system-value.active {
  color: #67c23a;
  font-weight: 600;
}

.system-value.inactive {
  color: #f56c6c;
}

.monitor-list {
  min-height: 400px;
}

.dialog-footer {
  text-align: right;
}

/* 表格样式优化 */
:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background: #f8f9fa;
}

/* 标签页样式 */
:deep(.el-tabs__header) {
  margin-bottom: 20px;
}

/* 空状态样式 */
:deep(.el-empty) {
  padding: 40px 20px;
}
</style>

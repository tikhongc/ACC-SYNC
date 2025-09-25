<template>
  <el-dialog
    v-model="visible"
    title="选择项目"
    width="800px"
    :before-close="handleClose"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    class="project-selector-dialog"
  >
    <!-- 对话框头部 -->
    <template #header>
      <div class="dialog-header">
        <div class="header-title">
          <el-icon class="header-icon"><Folder /></el-icon>
          <span>选择项目</span>
        </div>
        <div class="header-actions">
          <el-button 
            type="primary" 
            size="small" 
            :icon="Refresh"
            :loading="refreshing"
            @click="refreshProjects">
            刷新项目
          </el-button>
        </div>
      </div>
    </template>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
      <div class="loading-text">正在获取项目列表...</div>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-container">
      <el-result
        icon="error"
        title="获取项目失败"
        :sub-title="error"
      >
        <template #extra>
          <el-button type="primary" @click="refreshProjects">重试</el-button>
        </template>
      </el-result>
    </div>

    <!-- 项目列表 -->
    <div v-else class="project-list-container">
      <!-- 统计信息 -->
      <div class="stats-bar">
        <el-statistic 
          title="总项目数" 
          :value="projects.length" 
          class="stat-item" />
        <el-statistic 
          title="活跃项目" 
          :value="activeProjectCount" 
          class="stat-item" />
        <el-statistic 
          title="缓存时间" 
          :value="cacheTimeDisplay" 
          class="stat-item" />
      </div>

      <!-- 搜索和筛选 -->
      <div class="filter-bar">
        <el-input
          v-model="searchText"
          placeholder="搜索项目名称..."
          :prefix-icon="Search"
          clearable
          class="search-input"
        />
        <el-select
          v-model="statusFilter"
          placeholder="状态筛选"
          clearable
          class="status-filter"
        >
          <el-option label="全部状态" value="" />
          <el-option label="活跃" value="active" />
          <el-option label="非活跃" value="inactive" />
        </el-select>
      </div>

      <!-- 项目表格 -->
      <el-table
        :data="filteredProjects"
        @selection-change="handleSelectionChange"
        @row-click="handleRowClick"
        highlight-current-row
        class="project-table"
        max-height="400px"
      >
        <el-table-column 
          type="selection" 
          width="55"
          v-if="multiple" />
        
        <el-table-column 
          type="radio" 
          width="55"
          v-if="!multiple">
          <template #default="{ row }">
            <el-radio 
              v-model="selectedProjectId" 
              :label="row.id" 
              @change="handleSingleSelection(row)">
              &nbsp;
            </el-radio>
          </template>
        </el-table-column>

        <el-table-column prop="name" label="项目名称" min-width="200" max-width="300" align="left" header-align="left">
          <template #default="{ row }">
            <div class="project-name">
              <el-tooltip 
                :content="row.name" 
                placement="top" 
                :disabled="row.name.length <= 30"
                effect="dark">
                <el-text class="name-text" truncated>{{ row.name }}</el-text>
              </el-tooltip>
              <el-tooltip 
                v-if="row.type" 
                :content="`项目类型: ${row.type}`" 
                placement="top"
                effect="dark">
                <el-tag 
                  size="small" 
                  class="type-tag">
                  {{ row.type }}
                </el-tag>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="id" label="项目ID" width="120" align="left" header-align="left">
          <template #default="{ row }">
            <el-tooltip 
              :content="row.id" 
              placement="top" 
              effect="dark">
              <el-text class="project-id" size="small" truncated>{{ row.id }}</el-text>
            </el-tooltip>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" width="100" align="left" header-align="left">
          <template #default="{ row }">
            <StatusTag 
              :status="getProjectStatusForTag(row.status)"
              :text="getStatusText(row.status)"
              size="small"
              :show-icon="false" />
          </template>
        </el-table-column>

        <el-table-column prop="permissions" label="权限范围" width="150" align="left" header-align="left">
          <template #default="{ row }">
            <div class="permissions-cell">
              <StatusTag 
                :status="getPermissionStatusForTag(row.attributes?.permissions?.level)"
                :text="row.attributes?.permissions?.scope || '基础访问'"
                size="small"
                :show-icon="false" />
              <el-tooltip 
                :content="row.attributes?.permissions?.description || '标准项目访问权限'"
                placement="top">
                <el-icon class="info-icon"><InfoFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 选择信息 -->
      <div v-if="selectedProjects.length > 0" class="selection-info">
        <el-alert
          :title="`已选择 ${selectedProjects.length} 个项目`"
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            <div class="selected-projects">
              <el-tag
                v-for="project in selectedProjects.slice(0, 3)"
                :key="project.id"
                size="small"
                class="selected-tag"
              >
                {{ project.name }}
              </el-tag>
              <el-text v-if="selectedProjects.length > 3" size="small">
                等 {{ selectedProjects.length }} 个项目
              </el-text>
            </div>
          </template>
        </el-alert>
      </div>
    </div>

    <!-- 对话框底部 -->
    <template #footer>
      <div class="dialog-footer">
        <div class="footer-info">
          <el-text size="small" type="info">
            {{ multiple ? '可选择多个项目' : '请选择一个项目' }}
          </el-text>
        </div>
        <div class="footer-actions">
          <el-button @click="handleClose">取消</el-button>
          <el-button 
            type="primary" 
            :disabled="selectedProjects.length === 0"
            @click="confirmSelection">
            确认选择 ({{ selectedProjects.length }})
          </el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Folder, 
  Refresh, 
  Search, 
  InfoFilled 
} from '@element-plus/icons-vue'
import axios from 'axios'
import StatusTag from './StatusTag.vue'

export default {
  name: 'ProjectSelector',
  components: {
    Folder,
    Refresh,
    Search,
    InfoFilled,
    StatusTag
  },
  props: {
    // 是否显示对话框
    modelValue: {
      type: Boolean,
      default: false
    },
    // 是否支持多选
    multiple: {
      type: Boolean,
      default: false
    },
    // 预选中的项目ID（单选）或ID数组（多选）
    defaultSelected: {
      type: [String, Array],
      default: null
    },
    // 是否在打开时自动刷新项目列表
    autoRefresh: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'confirm', 'cancel'],
  setup(props, { emit }) {
    // 响应式数据
    const visible = ref(false)
    const loading = ref(false)
    const refreshing = ref(false)
    const error = ref('')
    const projects = ref([])
    const selectedProjects = ref([])
    const selectedProjectId = ref('')
    const searchText = ref('')
    const statusFilter = ref('')
    const cacheInfo = ref(null)

    // 计算属性
    const activeProjectCount = computed(() => {
      return projects.value.filter(p => p.isActive).length
    })

    const cacheTimeDisplay = computed(() => {
      if (!cacheInfo.value?.timestamp) return '未知'
      const cacheTime = new Date(cacheInfo.value.timestamp * 1000)
      return cacheTime.toLocaleTimeString('zh-CN')
    })

    const filteredProjects = computed(() => {
      let filtered = projects.value

      // 按名称搜索
      if (searchText.value) {
        const search = searchText.value.toLowerCase()
        filtered = filtered.filter(p => 
          p.name.toLowerCase().includes(search) ||
          p.id.toLowerCase().includes(search)
        )
      }

      // 按状态筛选
      if (statusFilter.value) {
        if (statusFilter.value === 'active') {
          filtered = filtered.filter(p => p.isActive)
        } else if (statusFilter.value === 'inactive') {
          filtered = filtered.filter(p => !p.isActive)
        }
      }

      return filtered
    })

    // 监听 modelValue 变化
    watch(() => props.modelValue, (newVal) => {
      visible.value = newVal
      if (newVal) {
        initializeSelection()
        loadProjectsFromCache()
        if (props.autoRefresh) {
          refreshProjects()
        }
      }
    })

    // 监听 visible 变化
    watch(visible, (newVal) => {
      emit('update:modelValue', newVal)
    })

    // 初始化选择状态
    const initializeSelection = () => {
      if (props.defaultSelected) {
        if (props.multiple && Array.isArray(props.defaultSelected)) {
          // 多选模式
          selectedProjects.value = projects.value.filter(p => 
            props.defaultSelected.includes(p.id)
          )
        } else if (!props.multiple && typeof props.defaultSelected === 'string') {
          // 单选模式
          selectedProjectId.value = props.defaultSelected
          const project = projects.value.find(p => p.id === props.defaultSelected)
          if (project) {
            selectedProjects.value = [project]
          }
        }
      }
    }

    // 从缓存加载项目列表
    const loadProjectsFromCache = () => {
      try {
        const cachedData = localStorage.getItem('acc_projects')
        if (cachedData) {
          const parsedData = JSON.parse(cachedData)
          
          // 检查缓存是否过期（24小时）
          const now = Date.now()
          const cacheAge = now - (parsedData.cache_info?.timestamp * 1000 || 0)
          const maxAge = 24 * 60 * 60 * 1000 // 24小时

          if (cacheAge < maxAge && parsedData.projects?.list) {
            projects.value = parsedData.projects.list
            cacheInfo.value = parsedData.cache_info
            console.log('从缓存加载项目列表:', projects.value.length, '个项目')
            return true
          } else {
            console.log('缓存已过期，需要刷新')
          }
        }
      } catch (error) {
        console.error('加载缓存项目列表失败:', error)
      }
      return false
    }

    // 刷新项目列表
    const refreshProjects = async () => {
      const isInitialLoad = !refreshing.value && !projects.value.length
      if (isInitialLoad) {
        loading.value = true
      } else {
        refreshing.value = true
      }
      
      error.value = ''

      try {
        console.log('开始获取项目列表...')
        const response = await axios.get('/api/auth/projects', {
          timeout: 30000
        })

        if (response.data.status === 'success') {
          projects.value = response.data.projects.list || []
          cacheInfo.value = response.data.cache_info

          // 保存到 localStorage
          localStorage.setItem('acc_projects', JSON.stringify(response.data))
          
          console.log('项目列表获取成功:', projects.value.length, '个项目')
        } else {
          throw new Error(response.data.error || '获取项目列表失败')
        }
      } catch (err) {
        console.error('获取项目列表失败:', err)
        error.value = err.response?.data?.error || err.message
        ElMessage.error('获取项目列表失败: ' + error.value)
      } finally {
        loading.value = false
        refreshing.value = false
      }
    }

    // 处理选择变化（多选）
    const handleSelectionChange = (selection) => {
      selectedProjects.value = selection
    }

    // 处理单选
    const handleSingleSelection = (row) => {
      selectedProjects.value = [row]
    }

    // 处理行点击
    const handleRowClick = (row) => {
      if (!props.multiple) {
        selectedProjectId.value = row.id
        selectedProjects.value = [row]
      }
    }

    // 确认选择
    const confirmSelection = () => {
      if (selectedProjects.value.length === 0) {
        ElMessage.warning('请选择至少一个项目')
        return
      }

      const result = props.multiple ? selectedProjects.value : selectedProjects.value[0]
      emit('confirm', result)
      handleClose()
    }

    // 关闭对话框
    const handleClose = () => {
      visible.value = false
      emit('cancel')
    }

    // 获取状态类型
    const getStatusType = (status) => {
      const statusMap = {
        'active': 'success',
        'inactive': 'info',
        'suspended': 'warning',
        'archived': 'info'
      }
      return statusMap[status] || 'info'
    }

    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'active': '活跃',
        'inactive': '非活跃',
        'suspended': '暂停',
        'archived': '已归档'
      }
      return statusMap[status] || status || '未知'
    }

    // 获取权限类型
    const getPermissionType = (level) => {
      const levelMap = {
        'admin': 'danger',
        'member': 'primary',
        'viewer': 'info',
        'unknown': 'warning'
      }
      return levelMap[level] || 'info'
    }

    // StatusTag适配方法
    const getProjectStatusForTag = (status) => {
      const statusMap = {
        'active': 'active',
        'inactive': 'inactive',
        'suspended': 'warning',
        'archived': 'archived'
      }
      return statusMap[status] || 'unknown'
    }

    const getPermissionStatusForTag = (level) => {
      const levelMap = {
        'admin': 'warning',
        'member': 'success',
        'viewer': 'info',
        'unknown': 'warning'
      }
      return levelMap[level] || 'info'
    }

    return {
      visible,
      loading,
      refreshing,
      error,
      projects,
      selectedProjects,
      selectedProjectId,
      searchText,
      statusFilter,
      activeProjectCount,
      cacheTimeDisplay,
      filteredProjects,
      refreshProjects,
      handleSelectionChange,
      handleSingleSelection,
      handleRowClick,
      confirmSelection,
      handleClose,
      getStatusType,
      getStatusText,
      getPermissionType,
      getProjectStatusForTag,
      getPermissionStatusForTag
    }
  }
}
</script>

<style scoped>
.project-selector-dialog :deep(.el-dialog) {
  border-radius: 12px;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.header-icon {
  color: #409eff;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.loading-container {
  padding: 20px;
  text-align: center;
}

.loading-text {
  margin-top: 16px;
  color: #909399;
  font-size: 14px;
}

.error-container {
  padding: 20px;
}

.project-list-container {
  max-height: 600px;
  overflow: hidden;
}

.stats-bar {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-item {
  flex: 1;
  text-align: center;
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-input {
  flex: 1;
}

.status-filter {
  width: 120px;
}

.project-table {
  border-radius: 8px;
  overflow: hidden;
}

.project-table :deep(.el-table__cell) {
  text-align: left !important;
}

.project-name {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 100%;
}

.name-text {
  font-weight: 500;
  max-width: 100%;
  cursor: help;
}

.type-tag {
  align-self: flex-start;
  cursor: help;
}

.project-id {
  font-family: 'Consolas', 'Monaco', monospace;
  color: #606266;
  max-width: 100%;
  cursor: help;
}

.permissions-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.info-icon {
  color: #909399;
  cursor: help;
}

.selection-info {
  margin-top: 16px;
}

.selected-projects {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}

.selected-tag {
  max-width: 120px;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-info {
  flex: 1;
}

.footer-actions {
  display: flex;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .project-selector-dialog :deep(.el-dialog) {
    width: 95vw !important;
    margin: 5vh auto !important;
  }
  
  .stats-bar {
    flex-direction: column;
    gap: 12px;
  }
  
  .filter-bar {
    flex-direction: column;
  }
  
  .dialog-footer {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .footer-actions {
    justify-content: center;
  }
}
</style>

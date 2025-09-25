<template>
  <div class="reviews">
    <!-- 面包屑导航 -->
    <Breadcrumb />
    
    <!-- 页面头部 -->
    <PageHeader
      title="项目评审管理"
      description="查看和管理 Autodesk Construction Cloud 项目中的所有评审数据"
      tag="评审数据"
      tag-type="success"
      :action-buttons="headerButtons"
      @action="handleHeaderAction" />

    <!-- 统计信息区域 -->
    <StatsSection 
      v-if="reviewsData && !loading && !error"
      :stats="headerStats" 
      @stat-click="handleStatClick" />

    <!-- 加载状态 -->
    <LoadingState 
      v-if="loading"
      type="card"
      title="正在获取评审数据"
      text="请稍候，正在从服务器获取最新的评审数据..."
      :show-progress="false"
      :show-cancel="true"
      @cancel="cancelLoading" />

    <!-- 错误状态 -->
    <ErrorState
      v-if="error"
      type="card"
      severity="error"
      title="获取评审数据失败"
      :message="error"
      :suggestions="errorSuggestions"
      :action-buttons="errorButtons"
      @action="handleErrorAction" />

    <!-- 成功状态指示器 -->
    <StatusIndicator
      v-if="reviewsData && !loading && !error"
      status="success"
      :title="`数据获取成功！`"
      :description="`成功获取 ${reviewsData.reviews?.length || 0} 个项目评审`"
      :details="`最后更新时间: ${new Date().toLocaleString('zh-CN')}`"
      size="default"
      style="margin-bottom: 24px;" />

    <!-- 查询信息卡片 -->
    <QueryInfoCard
      v-if="reviewsData && !loading && !error"
      title="项目评审查询"
      api-endpoint="/api/reviews/jarvis"
      description="获取 isBIM JARVIS 2025 Dev 项目的所有评审数据"
      :result-count="reviewsData.reviews?.length || 0"
      result-unit="个评审"
      :custom-fields="getReviewsQueryFields()" />

    <!-- 评审详情弹窗 -->
    <el-dialog
      v-if="showReviewDialog && selectedReview"
      v-model="showReviewDialog"
      :title="`评审详情 - ${selectedReview?.name || ''}`"
      width="80%"
      :before-close="handleCloseDialog"
      draggable
      destroy-on-close
      class="review-dialog"
      :key="`dialog-${dialogKey}`">
      <div class="dialog-content">
        <ReviewDetail 
          :review="selectedReview" 
          :key="`detail-${dialogKey}`" />
      </div>
    </el-dialog>

    <!-- 评审数据内容 -->
    <div v-if="reviewsData && !loading && !error">

      <!-- 评审数据表格 -->
      <DataTable
        :key="`reviews-table-${reviewsData?.timestamp || 'default'}`"
        :data="reviewsData.reviews || []"
        :columns="tableColumns"
        :loading="loading"
        title="📋 项目评审列表"
        description="点击查看详情按钮查看评审的详细信息和参与者"
        :action-buttons="tableActions"
        :operations="rowOperations"
        :show-index="true"
        row-key="sequence_id"
        @action="handleTableAction"
        @row-operation="handleRowOperation">
        
        <!-- 评审状态列 -->
        <template #status="{ row }">
          <StatusTag
            :status="row.status || 'unknown'"
            size="small"
            :show-icon="false" />
        </template>
        
        <!-- 序列ID列 -->
        <template #sequence-id="{ row }">
          <StatusTag 
            status="info" 
            :text="`#${row.sequence_id}`"
            size="small" 
            :show-icon="false" />
        </template>
        
        <!-- 归档状态列 -->
        <template #archived="{ row }">
          <StatusTag
            :status="row.archived ? 'archived' : 'active'"
            size="small"
            :show-icon="false" />
        </template>
        
        <!-- 创建者列 -->
        <template #created-by="{ row }">
          <div class="user-info">
            <span class="user-name">{{ row.created_by?.name || 'N/A' }}</span>
            <span class="user-id">{{ row.created_by?.autodeskId || '' }}</span>
          </div>
        </template>
        
        <!-- 下一步操作者列 -->
        <template #next-action="{ row }">
          <div class="next-action-info">
            <div v-if="row.has_claimed_users" class="claimed-users">
              <StatusTag status="success" text="已认领" size="small" :show-icon="false" />
            </div>
            <div class="candidates-summary">
              <StatusTag 
                v-if="row.candidates_count.users > 0" 
                status="info" 
                :text="`👤 ${row.candidates_count.users}`"
                size="small" 
                :show-icon="false" />
              <StatusTag 
                v-if="row.candidates_count.roles > 0" 
                status="success" 
                :text="`🏷️ ${row.candidates_count.roles}`"
                size="small" 
                :show-icon="false"
                style="margin-left: 4px;" />
              <StatusTag 
                v-if="row.candidates_count.companies > 0" 
                status="warning" 
                :text="`🏢 ${row.candidates_count.companies}`"
                size="small" 
                :show-icon="false"
                style="margin-left: 4px;" />
            </div>
          </div>
        </template>
        
        <!-- 到期时间列 -->
        <template #due-date="{ row }">
          <span class="timestamp">{{ row.current_step_due_date || 'N/A' }}</span>
        </template>
        
        <!-- 创建时间列 -->
        <template #created-at="{ row }">
          <span class="timestamp">{{ row.created_at }}</span>
        </template>
        
        <!-- 更新时间列 -->
        <template #updated-at="{ row }">
          <span class="timestamp">{{ row.updated_at }}</span>
        </template>
        
      </DataTable>
      
      <!-- 详细分析数据 -->
      <BaseCard 
        v-if="reviewsData.detailed_analysis && reviewsData.detailed_analysis.length > 0"
        title="📋 详细评审分析"
        :show-header="true"
        :collapsible="true"
        :default-collapsed="true"
        style="margin-top: 24px;">
        <JsonViewer 
          :data="reviewsData.detailed_analysis"
          title="评审详细分析数据"
          :max-height="600" />
      </BaseCard>
      
      <!-- 原始数据 -->
      <BaseCard 
        title="🔍 原始 API 数据"
        :show-header="true"
        :collapsible="true"
        :default-collapsed="true"
        style="margin-top: 24px;">
        <JsonViewer 
          :data="reviewsData.raw_data"
          title="Autodesk Construction Cloud API 原始响应"
          :max-height="600" />
      </BaseCard>
    </div>

    <!-- 项目选择对话框 -->
    <ProjectSelector
      v-model="showProjectSelector"
      :multiple="false"
      :auto-refresh="false"
      @confirm="handleProjectSelected"
      @cancel="handleProjectSelectionCancel" />
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick, getCurrentInstance } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import Breadcrumb from '../components/Breadcrumb.vue'
import PageHeader from '../components/PageHeader.vue'
import LoadingState from '../components/LoadingState.vue'
import ErrorState from '../components/ErrorState.vue'
import StatusIndicator from '../components/StatusIndicator.vue'
import QueryInfoCard from '../components/QueryInfoCard.vue'
import DataTable from '../components/DataTable.vue'
import BaseCard from '../components/BaseCard.vue'
import JsonViewer from '../components/JsonViewer.vue'
import ReviewDetail from '../components/ReviewDetail.vue'
import StatsSection from '../components/StatsSection.vue'
import ProjectSelector from '../components/ProjectSelector.vue'
import StatusTag from '../components/StatusTag.vue'
import projectStore from '../utils/projectStore.js'

// 图标导入
import { 
  DocumentChecked as IconReview,
  Refresh,
  Download,
  Setting,
  View,
  Search,
  Filter
} from '@element-plus/icons-vue'

export default {
  name: 'Reviews',
  components: {
    Breadcrumb,
    PageHeader,
    LoadingState,
    ErrorState,
    StatusIndicator,
    QueryInfoCard,
    DataTable,
    BaseCard,
    JsonViewer,
    ReviewDetail,
    StatsSection,
    ProjectSelector,
    StatusTag
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const error = ref('')
    const reviewsData = ref(null)
    const showReviewDialog = ref(false)
    const selectedReview = ref(null)
    const dialogKey = ref(0) // Force dialog recreation
    
    // 项目相关
    const currentProject = ref(null)
    const showProjectSelector = ref(false)
    
    // 页面头部配置
    const headerButtons = reactive([
      {
        text: '刷新数据',
        type: 'primary',
        icon: Refresh,
        action: 'refresh'
      },
      {
        text: '导出数据',
        type: 'default',
        icon: Download,
        action: 'export'
      },
      {
        text: '配置',
        type: 'default',
        icon: Setting,
        action: 'settings'
      }
    ])
    
    // 计算属性：头部统计
    const headerStats = computed(() => {
      if (!reviewsData.value?.stats) return []
      
      const stats = reviewsData.value.stats
      const headerStatsArray = [
        {
          label: '总评审数',
          value: stats.total_reviews || 0,
          type: 'primary',
          icon: '📋',
          description: '项目中的总评审数量',
          clickable: false
        },
        {
          label: '活跃评审',
          value: stats.active_count || 0,
          type: 'success',
          icon: '✅',
          description: '当前正在进行的评审',
          clickable: true
        },
        {
          label: '已归档',
          value: stats.archived_count || 0,
          type: 'info',
          icon: '📦',
          description: '已完成并归档的评审',
          clickable: true
        },
        {
          label: '开放状态',
          value: stats.status_counts?.OPEN || 0,
          type: 'warning',
          icon: '🔓',
          description: '状态为开放的评审数量',
          clickable: true
        }
      ]
      
      // 如果有重复数据，添加去重信息
      if (stats.duplicate_count && stats.duplicate_count > 0) {
        headerStatsArray.push({
          label: '已去重',
          value: stats.duplicate_count,
          type: 'danger',
          icon: '🔄',
          description: '检测到并去除的重复数据',
          clickable: false
        })
      }
      
      return headerStatsArray
    })
    
    // 表格配置
    const tableColumns = [
      {
        prop: 'name',
        label: '评审名称',
        minWidth: 200,
        sortable: true
      },
      {
        prop: 'sequence_id',
        label: '序列ID',
        width: 100,
        slot: 'sequence-id'
      },
      {
        prop: 'status',
        label: '状态',
        width: 100,
        slot: 'status'
      },
      {
        prop: 'archived',
        label: '归档状态',
        width: 100,
        slot: 'archived'
      },
      {
        prop: 'created_by',
        label: '创建者',
        width: 150,
        slot: 'created-by'
      },
      {
        prop: 'next_action_by',
        label: '下一步操作',
        width: 180,
        slot: 'next-action'
      },
      {
        prop: 'current_step_due_date',
        label: '到期时间',
        width: 160,
        slot: 'due-date',
        sortable: true
      },
      {
        prop: 'created_at',
        label: '创建时间',
        width: 160,
        slot: 'created-at',
        sortable: true
      },
      {
        prop: 'updated_at',
        label: '更新时间',
        width: 160,
        slot: 'updated-at',
        sortable: true
      }
    ]
    
    const tableActions = [
      {
        text: '搜索',
        type: 'primary',
        icon: Search,
        action: 'search'
      },
      {
        text: '筛选',
        type: 'default',
        icon: Filter,
        action: 'filter'
      }
    ]
    
    const rowOperations = [
      {
        text: '查看详情',
        type: 'primary',
        icon: View,
        action: 'check'
      }
    ]
    
    // 错误处理配置
    const errorSuggestions = [
      '检查网络连接是否正常',
      '确认已完成 Autodesk 账户认证',
      '验证项目访问权限',
      '检查 API 服务状态'
    ]
    
    const errorButtons = [
      {
        text: '重新认证',
        type: 'primary',
        action: 'reauth'
      },
      {
        text: '重试',
        type: 'default',
        action: 'retry'
      }
    ]
    
    // 获取评审数据
    const fetchReviewsData = async () => {
      if (!currentProject.value) {
        error.value = '未选择项目，无法获取评审数据'
        return
      }

      loading.value = true
      error.value = ''
      
      console.log('开始获取评审数据...', '项目:', currentProject.value.name)
      
      try {
        // 添加时间戳防止缓存
        const response = await axios.get('/api/reviews/jarvis', {
          timeout: 30000,
          params: {
            _t: Date.now(), // 防止缓存
            projectId: currentProject.value.id
          }
        })
        
        if (response.data.success) {
          // Force clear the data first to ensure reactivity
          reviewsData.value = null
          await new Promise(resolve => setTimeout(resolve, 10)) // Small delay
          reviewsData.value = response.data
          
          // 输出调试信息
          console.log('API响应统计:', response.data.stats)
          console.log('表格数据数量:', response.data.reviews?.length)
          console.log('原始数据数量:', response.data.raw_data?.length)
          console.log('详细分析数量:', response.data.detailed_analysis?.length)
          
          // 检查前端是否还有重复数据
          const reviewIds = response.data.reviews?.map(r => r.id) || []
          const uniqueIds = new Set(reviewIds)
          console.log('前端检查 - 总ID数:', reviewIds.length)
          console.log('前端检查 - 唯一ID数:', uniqueIds.size)
          if (reviewIds.length !== uniqueIds.size) {
            console.warn('⚠️ 前端仍然检测到重复ID!')
            const duplicates = reviewIds.filter((id, index) => reviewIds.indexOf(id) !== index)
            console.warn('重复的ID:', [...new Set(duplicates)])
          } else {
            console.log('✅ 前端数据无重复')
          }
          
          if (response.data.stats?.duplicate_count > 0) {
            ElMessage.success(`评审数据获取成功，已去重 ${response.data.stats.duplicate_count} 条重复数据`)
          } else {
            ElMessage.success('评审数据获取成功')
          }
        } else {
          throw new Error(response.data.error || '获取数据失败')
        }
      } catch (err) {
        console.error('获取评审数据失败:', err)
        error.value = err.response?.data?.error || err.message || '获取评审数据失败'
        ElMessage.error(error.value)
      } finally {
        loading.value = false
      }
    }
    
    // 取消加载
    const cancelLoading = () => {
      loading.value = false
      ElMessage.info('已取消数据获取')
    }
    
    // 处理头部操作
    const handleHeaderAction = (action) => {
      switch (action) {
        case 'refresh':
          fetchReviewsData()
          break
        case 'export':
          exportReviewsData()
          break
        case 'settings':
          ElMessage.info('配置功能开发中')
          break
      }
    }
    
    // 处理错误操作
    const handleErrorAction = (action) => {
      switch (action) {
        case 'reauth':
          window.location.href = '/login'
          break
        case 'retry':
          fetchReviewsData()
          break
      }
    }
    
    // 处理表格操作
    const handleTableAction = (action) => {
      switch (action) {
        case 'search':
          ElMessage.info('搜索功能开发中')
          break
        case 'filter':
          ElMessage.info('筛选功能开发中')
          break
      }
    }
    
    // 处理行操作
    const handleRowOperation = (action, button, index) => {
      console.log('Row operation triggered:', action, button, index)
      console.log('Button object:', button)
      
      // 从action中提取实际的操作类型（去掉索引）
      const actualAction = action.split(':')[0]
      
      // 获取对应行的数据 - 使用button中传递的实际行数据
      const row = button.row
      
      if (!row) {
        ElMessage.error('无法获取行数据')
        return
      }
      
      console.log('Using row data:', {
        id: row.id,
        name: row.name,
        sequence_id: row.sequence_id
      })
      
      switch (actualAction) {
        case 'check':
        case 'view':
          // 打开评审详情弹窗
          const reviewForDetail = getReviewForDetail(row)
          console.log('Opening review detail for:', {
            rowId: row.id,
            rowSequenceId: row.sequence_id,
            rowName: row.name,
            reviewForDetailId: reviewForDetail.id,
            reviewForDetailSequenceId: reviewForDetail.sequenceId,
            reviewForDetailName: reviewForDetail.name
          })
          
          // Force clear and set with small delay to ensure reactivity
          selectedReview.value = null
          showReviewDialog.value = false
          dialogKey.value += 1 // Force new dialog instance
          
          nextTick(() => {
            selectedReview.value = reviewForDetail
            showReviewDialog.value = true
            ElMessage.success(`正在查看评审: ${row.name}`)
          })
          break
        default:
          ElMessage.info(`操作: ${actualAction}`)
          break
      }
    }
    
    // 导出数据
    const exportReviewsData = () => {
      if (!reviewsData.value) {
        ElMessage.warning('没有数据可以导出')
        return
      }
      
      try {
        const dataStr = JSON.stringify(reviewsData.value, null, 2)
        const dataBlob = new Blob([dataStr], { type: 'application/json' })
        const url = URL.createObjectURL(dataBlob)
        const link = document.createElement('a')
        link.href = url
        link.download = `project-reviews-${new Date().toISOString().split('T')[0]}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
        ElMessage.success('数据导出成功')
      } catch (err) {
        console.error('导出失败:', err)
        ElMessage.error('导出失败')
      }
    }
    
    // 获取查询字段信息
    const getReviewsQueryFields = () => {
      if (!reviewsData.value) return []
      
      return [
        {
          label: '项目ID',
          value: reviewsData.value.project_id || 'N/A',
          type: 'code'
        },
        {
          label: '查询参数',
          value: JSON.stringify(reviewsData.value.query_params || {}),
          type: 'json'
        },
        {
          label: '分页信息',
          value: JSON.stringify(reviewsData.value.pagination || {}),
          type: 'json'
        },
        {
          label: '查询时间',
          value: reviewsData.value.timestamp || 'N/A',
          type: 'timestamp'
        }
      ]
    }
    
    // 为详情组件准备评审数据
    const getReviewForDetail = (row) => {
      console.log('getReviewForDetail called with row:', {
        id: row.id,
        name: row.name,
        sequence_id: row.sequence_id
      })
      
      // 从原始数据中找到对应的完整评审数据
      // 首先尝试用sequenceId匹配，然后fallback到id匹配
      let rawReview = reviewsData.value?.raw_data?.find(r => r.sequenceId === row.sequence_id)
      if (!rawReview) {
        rawReview = reviewsData.value?.raw_data?.find(r => r.id === row.id)
      }
      console.log('Found rawReview:', rawReview ? {
        id: rawReview.id,
        name: rawReview.name,
        sequenceId: rawReview.sequenceId
      } : 'null')
      
      if (rawReview) {
        return rawReview
      }
      
      // 如果找不到原始数据，使用处理过的数据构造
      const constructedReview = {
        id: row.id,
        sequenceId: row.sequence_id,
        name: row.name,
        status: row.status,
        currentStepId: row.current_step_id,
        currentStepDueDate: row.current_step_due_date,
        createdBy: row.created_by,
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        finishedAt: row.finished_at,
        archived: row.archived,
        archivedBy: row.archived_by,
        archivedAt: row.archived_at,
        workflowId: row.workflow_id,
        nextActionBy: row.next_action_by
      }
      
      console.log('Constructed review:', {
        id: constructedReview.id,
        name: constructedReview.name,
        sequenceId: constructedReview.sequenceId
      })
      
      return constructedReview
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      const statusMap = {
        'OPEN': 'success',
        'CLOSED': 'info',
        'VOID': 'warning',
        'FAILED': 'danger'
      }
      return statusMap[status] || 'info'
    }
    
    // 关闭弹窗处理
    const handleCloseDialog = () => {
      showReviewDialog.value = false
      selectedReview.value = null
      dialogKey.value += 1 // Ensure fresh dialog next time
    }
    
    // 处理统计卡片点击
    const handleStatClick = (stat, index) => {
      console.log('Stat clicked:', stat, index)
      
      switch (stat.label) {
        case '活跃评审':
          ElMessage.info('筛选显示活跃评审功能开发中')
          break
        case '已归档':
          ElMessage.info('筛选显示已归档评审功能开发中')
          break
        case '开放状态':
          ElMessage.info('筛选显示开放状态评审功能开发中')
          break
        default:
          ElMessage.info(`点击了统计项: ${stat.label}`)
      }
    }
    
    // 项目初始化方法
    const initializeProject = async () => {
      // 检查URL参数中是否有项目ID
      const route = getCurrentInstance().appContext.config.globalProperties.$route
      const projectId = route.query.projectId
      const projectName = route.query.projectName
      
      if (projectId) {
        // 从URL参数获取项目信息
        currentProject.value = {
          id: projectId,
          name: projectName || projectId
        }
        console.log('从URL获取项目信息:', currentProject.value)
      } else {
        // 尝试从localStorage获取之前选择的项目
        const savedProject = projectStore.getSelectedProject()
        if (savedProject) {
          currentProject.value = savedProject
          console.log('从localStorage获取项目信息:', currentProject.value)
        }
      }

      if (currentProject.value) {
        // 有项目信息，开始获取数据
        fetchReviewsData()
      } else {
        // 没有项目信息，显示项目选择对话框
        showProjectSelector.value = true
      }
    }

    // 处理项目选择确认
    const handleProjectSelected = (selectedProject) => {
      currentProject.value = selectedProject
      projectStore.saveSelectedProject(selectedProject)
      ElMessage.success(`已选择项目: ${selectedProject.name}`)
      fetchReviewsData()
    }

    // 处理项目选择取消
    const handleProjectSelectionCancel = () => {
      // 如果取消选择且没有当前项目，返回首页
      if (!currentProject.value) {
        const router = getCurrentInstance().appContext.config.globalProperties.$router
        router.push('/')
      }
    }

    // 组件挂载时初始化项目
    onMounted(() => {
      initializeProject()
    })
    
    return {
      // 响应式数据
      loading,
      error,
      reviewsData,
      showReviewDialog,
      selectedReview,
      dialogKey,
      
      // 项目相关
      currentProject,
      showProjectSelector,
      
      // 配置
      headerButtons,
      headerStats,
      tableColumns,
      tableActions,
      rowOperations,
      errorSuggestions,
      errorButtons,
      
      // 图标
      IconReview,
      
      // 方法
      fetchReviewsData,
      cancelLoading,
      handleHeaderAction,
      handleErrorAction,
      handleTableAction,
      handleRowOperation,
      exportReviewsData,
      getReviewsQueryFields,
      getReviewForDetail,
      getStatusType,
      handleCloseDialog,
      handleStatClick,
      initializeProject,
      handleProjectSelected,
      handleProjectSelectionCancel
    }
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.reviews {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.stats-grid {
  display: grid;
  gap: 20px;
}

.stats-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  padding: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  line-height: 1;
}

.stat-value.primary { color: #409eff; }
.stat-value.success { color: #67c23a; }
.stat-value.warning { color: #e6a23c; }
.stat-value.info { color: #909399; }

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 500;
  color: #303133;
  font-size: 13px;
}

.user-id {
  font-size: 11px;
  color: #909399;
  font-family: 'Consolas', 'Monaco', monospace;
}

.next-action-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.claimed-users {
  margin-bottom: 4px;
}

.candidates-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
}

.timestamp {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  color: #666;
}

/* 弹窗样式 */
.review-dialog {
  --el-dialog-border-radius: 12px;
}

.review-dialog :deep(.el-dialog) {
  border-radius: 12px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

.review-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  color: white;
  border-radius: 12px 12px 0 0;
  padding: 20px 24px;
}

.review-dialog :deep(.el-dialog__title) {
  color: white;
  font-weight: 600;
  font-size: 18px;
}

.review-dialog :deep(.el-dialog__headerbtn) {
  top: 20px;
  right: 20px;
}

.review-dialog :deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
  font-size: 20px;
}

.review-dialog :deep(.el-dialog__headerbtn .el-dialog__close):hover {
  color: #f0f0f0;
}

.review-dialog :deep(.el-dialog__body) {
  padding: 0;
  background: #f8fafc;
  border-radius: 0 0 12px 12px;
  max-height: 80vh;
  overflow-y: auto;
}

.dialog-content {
  padding: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .reviews {
    padding: 10px;
  }
  
  .stats-content {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .user-info {
    align-items: flex-start;
  }
  
  .candidates-summary {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

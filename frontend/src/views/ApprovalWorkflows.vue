<template>
  <div class="approval-workflows">
    <!-- 面包屑导航 -->
    <Breadcrumb />
    
    <!-- 页面头部 -->
    <PageHeader
      title="审批工作流管理"
      description="查看和管理 Autodesk Construction Cloud 项目中的审批工作流配置"
      tag="工作流"
      tag-type="primary"
      :action-buttons="headerButtons"
      @action="handleHeaderAction" />

    <!-- 加载状态 -->
    <LoadingState 
      v-if="loading"
      type="card"
      title="正在获取工作流数据"
      text="请稍候，正在从服务器获取最新的审批工作流数据..."
      :show-progress="false"
      :show-cancel="true"
      @cancel="cancelLoading" />

    <!-- 错误状态 -->
    <ErrorState
      v-if="error"
      type="card"
      severity="error"
      title="获取工作流数据失败"
      :message="error"
      :suggestions="errorSuggestions"
      :action-buttons="errorButtons"
      @action="handleErrorAction" />

    <!-- 成功状态指示器 -->
    <StatusIndicator
      v-if="workflowsData && !loading && !error"
      status="success"
      :title="`数据获取成功！`"
      :description="`成功获取 ${workflowsData.workflows?.length || 0} 个审批工作流`"
      :details="`最后更新时间: ${new Date().toLocaleString('zh-CN')}`"
      size="default"
      style="margin-bottom: 24px;" />

    <!-- 查询信息卡片 -->
    <QueryInfoCard
      v-if="workflowsData && !loading && !error"
      title="审批工作流查询"
      api-endpoint="/api/reviews/workflows/jarvis"
      description="获取 isBIM JARVIS 2025 Dev 项目的所有审批工作流配置"
      :result-count="workflowsData.workflows?.length || 0"
      result-unit="个工作流"
      :custom-fields="getWorkflowsQueryFields()" />

    <!-- 工作流详情弹窗 -->
    <el-dialog
      v-model="showWorkflowDialog"
      :title="`工作流详情 - ${selectedWorkflow?.name || ''}`"
      width="90%"
      :before-close="handleCloseDialog"
      draggable
      destroy-on-close
      class="workflow-dialog">
      <div v-if="selectedWorkflow" class="dialog-content">
        <WorkflowDiagram :workflow="selectedWorkflow" />
      </div>
    </el-dialog>

    <!-- 工作流数据内容 -->
    <div v-if="workflowsData && !loading && !error">
      <!-- 工作流统计卡片 -->
      <div class="stats-grid" style="margin-bottom: 24px;">
        <BaseCard 
          title="📊 工作流统计"
          :show-header="true"
          :collapsible="true"
          :default-collapsed="false">
          <div class="stats-content">
            <div class="stat-item">
              <div class="stat-label">总工作流数</div>
              <div class="stat-value primary">{{ workflowsData.stats?.total_workflows || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">活跃工作流</div>
              <div class="stat-value success">{{ workflowsData.stats?.active_workflows || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">非活跃工作流</div>
              <div class="stat-value warning">{{ workflowsData.stats?.inactive_workflows || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">平均步骤数</div>
              <div class="stat-value info">{{ workflowsData.stats?.avg_steps_per_workflow || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">支持文件复制</div>
              <div class="stat-value primary">{{ workflowsData.stats?.workflows_with_copy_files || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">附加属性</div>
              <div class="stat-value info">{{ workflowsData.stats?.workflows_with_attributes || 0 }}</div>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- 工作流数据表格 -->
      <DataTable
        :data="workflowsData.workflows || []"
        :columns="tableColumns"
        :loading="loading"
        title="🔄 审批工作流详情"
        description="展开每一行查看工作流的详细配置和步骤信息"
        :action-buttons="tableActions"
        :operations="rowOperations"
        :show-index="true"
        @action="handleTableAction"
        @row-operation="handleRowOperation">
        
        <!-- 工作流状态列 -->
        <template #status="{ row }">
          <StatusTag
            :status="row.status === 'ACTIVE' ? 'active' : 'inactive'"
            :text="row.status"
            size="small"
            :show-icon="false" />
        </template>
        
        <!-- 步骤数量列 -->
        <template #steps-count="{ row }">
          <StatusTag 
            status="info" 
            :text="`${row.steps_count} 步骤`"
            size="small" 
            :show-icon="false" />
        </template>
        
        <!-- 功能特性列 -->
        <template #features="{ row }">
          <div class="features-tags">
            <StatusTag 
              v-if="row.has_copy_files" 
              status="success" 
              text="📁 文件复制"
              size="small" 
              :show-icon="false" />
            <StatusTag 
              v-if="row.has_attached_attributes" 
              status="info" 
              text="🏷️ 附加属性"
              size="small" 
              :show-icon="false"
              style="margin-left: 4px;" />
            <StatusTag 
              v-if="row.additional_options?.allowInitiatorToEdit" 
              status="warning" 
              text="✏️ 允许编辑"
              size="small" 
              :show-icon="false"
              style="margin-left: 4px;" />
          </div>
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
        v-if="workflowsData.detailed_analysis && workflowsData.detailed_analysis.length > 0"
        title="📋 详细工作流分析"
        :show-header="true"
        :collapsible="true"
        :default-collapsed="true"
        style="margin-top: 24px;">
        <JsonViewer 
          :data="workflowsData.detailed_analysis"
          title="工作流详细分析数据"
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
          :data="workflowsData.raw_data"
          title="Autodesk Construction Cloud API 原始响应"
          :max-height="600" />
      </BaseCard>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
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
import WorkflowDiagram from '../components/WorkflowDiagram.vue'
import StatusTag from '../components/StatusTag.vue'

// 图标导入
import { 
  Document as IconWorkflow,
  Refresh,
  Download,
  Setting,
  View,
  Search,
  Filter
} from '@element-plus/icons-vue'

export default {
  name: 'ApprovalWorkflows',
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
    WorkflowDiagram,
    StatusTag
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const error = ref('')
    const workflowsData = ref(null)
    const showWorkflowDialog = ref(false)
    const selectedWorkflow = ref(null)
    
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
      if (!workflowsData.value?.stats) return []
      
      const stats = workflowsData.value.stats
      return [
        {
          label: '总工作流',
          value: stats.total_workflows || 0,
          type: 'primary'
        },
        {
          label: '活跃工作流',
          value: stats.active_workflows || 0,
          type: 'success'
        },
        {
          label: '平均步骤',
          value: stats.avg_steps_per_workflow || 0,
          type: 'info'
        }
      ]
    })
    
    // 表格配置
    const tableColumns = [
      {
        prop: 'name',
        label: '工作流名称',
        minWidth: 200,
        sortable: true
      },
      {
        prop: 'status',
        label: '状态',
        width: 100,
        slot: 'status'
      },
      {
        prop: 'steps_count',
        label: '步骤数',
        width: 100,
        slot: 'steps-count'
      },
      {
        prop: 'approval_options_count',
        label: '审批选项',
        width: 100
      },
      {
        prop: 'features',
        label: '功能特性',
        width: 200,
        slot: 'features'
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
    
    // 获取工作流数据
    const fetchWorkflowsData = async () => {
      loading.value = true
      error.value = ''
      
      try {
         const response = await axios.get('/api/reviews/workflows/jarvis', {
          timeout: 30000
        })
        
        if (response.data.success) {
          workflowsData.value = response.data
          ElMessage.success('工作流数据获取成功')
        } else {
          throw new Error(response.data.error || '获取数据失败')
        }
      } catch (err) {
        console.error('获取工作流数据失败:', err)
        error.value = err.response?.data?.error || err.message || '获取工作流数据失败'
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
          fetchWorkflowsData()
          break
        case 'export':
          exportWorkflowsData()
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
          fetchWorkflowsData()
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
      
      // 从action中提取实际的操作类型（去掉索引）
      const actualAction = action.split(':')[0]
      
      // 获取对应行的数据
      const row = workflowsData.value?.workflows?.[index]
      
      if (!row) {
        ElMessage.error('无法获取行数据')
        return
      }
      
      switch (actualAction) {
        case 'check':
        case 'view':
          // 打开工作流详情弹窗
          selectedWorkflow.value = getWorkflowForDiagram(row)
          showWorkflowDialog.value = true
          ElMessage.success(`正在查看工作流: ${row.name}`)
          break
        default:
          ElMessage.info(`操作: ${actualAction}`)
          break
      }
    }
    
    // 导出数据
    const exportWorkflowsData = () => {
      if (!workflowsData.value) {
        ElMessage.warning('没有数据可以导出')
        return
      }
      
      try {
        const dataStr = JSON.stringify(workflowsData.value, null, 2)
        const dataBlob = new Blob([dataStr], { type: 'application/json' })
        const url = URL.createObjectURL(dataBlob)
        const link = document.createElement('a')
        link.href = url
        link.download = `approval-workflows-${new Date().toISOString().split('T')[0]}.json`
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
    const getWorkflowsQueryFields = () => {
      if (!workflowsData.value) return []
      
      return [
        {
          label: '项目ID',
          value: workflowsData.value.project_id || 'N/A',
          type: 'code'
        },
        {
          label: '查询参数',
          value: JSON.stringify(workflowsData.value.query_params || {}),
          type: 'json'
        },
        {
          label: '分页信息',
          value: JSON.stringify(workflowsData.value.pagination || {}),
          type: 'json'
        },
        {
          label: '查询时间',
          value: workflowsData.value.timestamp || 'N/A',
          type: 'timestamp'
        }
      ]
    }
    
    // 为图表组件准备工作流数据
    const getWorkflowForDiagram = (row) => {
      // 从原始数据中找到对应的完整工作流数据
      const rawWorkflow = workflowsData.value?.raw_data?.find(w => w.id === row.id)
      if (rawWorkflow) {
        return rawWorkflow
      }
      
      // 如果找不到原始数据，使用处理过的数据构造
      return {
        id: row.id,
        name: row.name,
        description: row.description || '',
        notes: row.notes || '',
        status: row.status,
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        steps: row.steps || [],
        approvalStatusOptions: row.approval_status_options || [],
        copyFilesOptions: row.copy_files_options || {},
        additionalOptions: row.additional_options || {},
        attachedAttributes: row.attached_attributes || [],
        updateAttributesOptions: row.update_attributes_options || {}
      }
    }
    
    // 关闭弹窗处理
    const handleCloseDialog = () => {
      showWorkflowDialog.value = false
      selectedWorkflow.value = null
    }
    
    // 组件挂载时获取数据
    onMounted(() => {
      fetchWorkflowsData()
    })
    
    return {
      // 响应式数据
      loading,
      error,
      workflowsData,
      showWorkflowDialog,
      selectedWorkflow,
      
      // 配置
      headerButtons,
      headerStats,
      tableColumns,
      tableActions,
      rowOperations,
      errorSuggestions,
      errorButtons,
      
      // 图标
      IconWorkflow,
      
      // 方法
      fetchWorkflowsData,
      cancelLoading,
      handleHeaderAction,
      handleErrorAction,
      handleTableAction,
      handleRowOperation,
      exportWorkflowsData,
      getWorkflowsQueryFields,
      getWorkflowForDiagram,
      handleCloseDialog
    }
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.approval-workflows {
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

.features-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.timestamp {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  color: #666;
}

.workflow-expand-content {
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  margin: 8px 0;
}

/* 弹窗样式 */
.workflow-dialog {
  --el-dialog-border-radius: 12px;
}

.workflow-dialog :deep(.el-dialog) {
  border-radius: 12px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

.workflow-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
  padding: 20px 24px;
}

.workflow-dialog :deep(.el-dialog__title) {
  color: white;
  font-weight: 600;
  font-size: 18px;
}

.workflow-dialog :deep(.el-dialog__headerbtn) {
  top: 20px;
  right: 20px;
}

.workflow-dialog :deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
  font-size: 20px;
}

.workflow-dialog :deep(.el-dialog__headerbtn .el-dialog__close):hover {
  color: #f0f0f0;
}

.workflow-dialog :deep(.el-dialog__body) {
  padding: 0;
  background: #f8fafc;
  border-radius: 0 0 12px 12px;
  max-height: 80vh;
  overflow-y: auto;
}

.dialog-content {
  padding: 20px;
}

.workflow-details {
  background: #fafafa;
  border-radius: 8px;
  padding: 20px;
  margin: 10px 0;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  color: #333;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e4e7ed;
  font-size: 14px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: white;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.detail-item strong {
  min-width: 80px;
  color: #606266;
  font-size: 12px;
}

.detail-item code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 11px;
  color: #e74c3c;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.step-header strong {
  flex: 1;
  color: #303133;
}

.step-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-info {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  font-size: 13px;
  color: #606266;
}

.candidates-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.candidates-info > div {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.candidates-info strong {
  min-width: 50px;
  font-size: 12px;
  color: #909399;
}

.approval-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.copy-files-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  font-size: 13px;
}

.copy-files-info > div {
  padding: 8px;
  background: white;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.copy-files-info strong {
  color: #606266;
  margin-right: 8px;
}

.copy-files-info code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 11px;
  color: #e74c3c;
  word-break: break-all;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .approval-workflows {
    padding: 10px;
  }
  
  .stats-content {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .step-info {
    flex-direction: column;
    gap: 8px;
  }
  
  .candidates-info > div {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

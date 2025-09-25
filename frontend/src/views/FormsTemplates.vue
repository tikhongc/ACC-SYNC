<template>
  <div class="forms-templates">
    <!-- 面包屑导航 -->
    <Breadcrumb />
    
    <!-- 页面头部 -->
    <PageHeader
      title="表单模板管理"
      description="查看和管理项目中的表单模板，支持分页、筛选和工作流分析"
      :icon="IconFile"
      tag="模板管理"
      tag-type="primary"
      :action-buttons="headerButtons"
      :show-breadcrumb="false"
      :show-stats="false"
      @action="handleHeaderAction" />

    <!-- 加载状态 -->
    <LoadingState 
      v-if="loading"
      type="card"
      title="正在获取模板数据"
      text="请稍候，正在从服务器获取最新的表单模板数据..."
      :show-progress="false"
      :show-cancel="true"
      @cancel="cancelLoading" />

    <!-- 错误状态 -->
    <ErrorState
      v-if="error"
      type="card"
      severity="error"
      title="获取模板数据失败"
      :message="error"
      :suggestions="errorSuggestions"
      :action-buttons="errorButtons"
      @action="handleErrorAction" />

    <!-- 成功状态指示器 -->
    <StatusIndicator
      v-if="templatesData && !loading && !error"
      status="success"
      :title="`数据获取成功！`"
      :description="`成功获取 ${templatesData.templates?.data?.length || 0} 个表单模板`"
      :details="`查询时间: ${new Date().toLocaleString('zh-CN')}`"
      size="default"
      style="margin-bottom: 24px;" />

    <!-- 查询信息卡片 -->
    <QueryInfoCard
      v-if="templatesData && !loading && !error"
      title="查询信息"
      :api-endpoint="getApiEndpoint()"
      :description="getQueryDescription()"
      :query-params="getFormattedQueryParams()"
      :result-count="templatesData.templates?.data?.length || 0"
      result-unit="个模板"
      :response-time="getResponseTime()"
      :query-time="queryTime"
      :custom-fields="getCustomQueryFields()"
      :actions="getQueryActions()"
      @refresh="refreshWithParams"
      @reset="resetParams" />

    <!-- 查询控制面板 -->
    <el-card v-if="templatesData && !loading && !error" class="query-control-card" shadow="never">
      <template #header>
        <div class="card-header">
          <h3>🎛️ 查询控制</h3>
        </div>
      </template>
      
      <div class="query-controls">
        <div class="control-row">
          <div class="control-item">
            <label>每页显示:</label>
            <el-select v-model="queryParams.limit" @change="refreshWithParams" style="width: 100px;">
              <el-option label="10" :value="10" />
              <el-option label="20" :value="20" />
              <el-option label="50" :value="50" />
            </el-select>
          </div>
          
          <div class="control-item">
            <label>排序:</label>
            <el-select v-model="queryParams.sortOrder" @change="refreshWithParams" style="width: 120px;">
              <el-option label="最新优先" value="desc" />
              <el-option label="最旧优先" value="asc" />
            </el-select>
          </div>
          
          <div class="control-item">
            <label>更新时间筛选:</label>
            <el-date-picker
              v-model="dateRange"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              @change="handleDateRangeChange"
              style="width: 300px;" />
          </div>
        </div>
        
        <div class="control-row">
          <el-button type="primary" @click="refreshWithParams" :loading="loading">
            <Refresh />
            应用筛选
          </el-button>
          <el-button @click="resetParams">重置</el-button>
        </div>
      </div>
    </el-card>

    <!-- 模板数据内容 -->
    <div v-if="templatesData && !loading && !error">
      <!-- 模板数据表格 -->
      <DataTable
        :data="templatesData.templates?.data || []"
        :columns="tableColumns"
        :loading="loading"
        title="📋 表单模板列表"
        description="项目中的所有表单模板，包含工作流和权限信息"
        :action-buttons="tableActions"
        :operations="rowOperations"
        :show-index="true"
        :show-pagination="false"
        @action="handleTableAction"
        @row-operation="handleRowOperation">
        
        <!-- 状态列 -->
        <template #status="{ row }">
          <StatusTag
            v-if="row"
            :status="getTemplateStatus(row.status)"
            :text="row.status || 'Unknown'"
            size="small"
            :show-icon="false" />
          <span v-else>N/A</span>
        </template>
        
        <!-- 更新时间列 -->
        <template #updated-at="{ row }">
          <div v-if="row" class="update-info">
            <div class="update-time">{{ formatDate(row.updatedAt) }}</div>
            <div class="update-ago">{{ getTimeAgo(row.updatedAt) }}</div>
          </div>
          <span v-else>N/A</span>
        </template>

        <!-- 工作流信息列 -->
        <template #workflow-info="{ row }">
          <div v-if="row" class="workflow-preview">
            <StatusTag 
              v-if="hasWorkflowInfo(row)" 
              status="available" 
              text="有工作流"
              size="small" 
              :show-icon="false" />
            <StatusTag 
              v-else 
              status="unavailable" 
              text="无工作流"
              size="small" 
              :show-icon="false" />
          </div>
          <div v-else class="workflow-preview">
            <StatusTag 
              status="unknown" 
              text="N/A"
              size="small" 
              :show-icon="false" />
          </div>
        </template>
      </DataTable>

      <!-- 分页控制 -->
      <div class="pagination-container" v-if="templatesData && getTotalCount() > 0">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="queryParams.limit"
          :total="getTotalCount()"
          layout="prev, pager, next, jumper"
          @current-change="handlePageChange" />
      </div>


      <!-- JSON 数据查看器 -->
      <div style="margin-top: 32px;">
        <JsonViewer
          :data="templatesData"
          title="完整模板数据"
          :collapsible="true"
          :show-controls="true"
          max-height="500px"
          theme="light" />
      </div>
    </div>

    <!-- 模板详情对话框 -->
    <el-dialog
      v-model="showTemplateDetailsDialog"
      :title="selectedTemplate ? `📋 模板详情 - ${selectedTemplate.name}` : '模板详情'"
      width="90%"
      :max-width="1200"
      top="5vh"
      :close-on-click-modal="false"
      :close-on-press-escape="true"
      class="template-details-dialog">
      
      <div v-if="selectedTemplate" class="template-details-content">
        <!-- 基本信息 -->
        <el-card class="details-section" shadow="never">
          <template #header>
            <div class="section-header">
              <h3>📝 基本信息</h3>
            </div>
            </template>
          
          <el-descriptions :column="2" border>
            <el-descriptions-item label="模板名称">
              <StatusTag 
                status="info" 
                :text="selectedTemplate.name"
                size="default" 
                :show-icon="false" />
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <StatusIndicator
                :status="getTemplateStatus(selectedTemplate.status)"
                :title="selectedTemplate.status"
                size="small" />
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ formatDate(selectedTemplate.createdAt) }}
            </el-descriptions-item>
            <el-descriptions-item label="更新时间">
              {{ formatDate(selectedTemplate.updatedAt) }}
            </el-descriptions-item>
            <el-descriptions-item label="创建者">
              <StatusTag 
                status="info" 
                :text="selectedTemplate.createdBy || 'N/A'"
                size="small" 
                :show-icon="false" />
            </el-descriptions-item>
            <el-descriptions-item label="模板ID">
              <StatusTag 
                status="info" 
                :text="selectedTemplate.id"
                size="small" 
                :show-icon="false" />
            </el-descriptions-item>
          </el-descriptions>
      </el-card>

        <!-- 工作流架构信息 -->
        <WorkflowArchitecture
          v-if="selectedTemplate && getTemplateWorkflowInfo(selectedTemplate)"
          :workflow-info="getTemplateWorkflowInfo(selectedTemplate)"
          :default-active-items="['architecture-summary', 'template-details', 'roles', 'resources']"
          class="details-section" />

        <!-- 原始数据查看 -->
        <el-card class="details-section" shadow="never">
        <template #header>
            <div class="section-header">
              <h3>🔍 原始数据</h3>
            </div>
        </template>
          
          <JsonViewer
            :data="selectedTemplate"
            title=""
            :collapsible="true"
            :show-controls="true"
            max-height="400px"
            theme="light" />
      </el-card>
    </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showTemplateDetailsDialog = false">关闭</el-button>
          <el-button type="primary" @click="downloadTemplateData" :icon="Download">
            导出模板数据
          </el-button>
      </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import Breadcrumb from '../components/Breadcrumb.vue'
import PageHeader from '../components/PageHeader.vue'
import LoadingState from '../components/LoadingState.vue'
import ErrorState from '../components/ErrorState.vue'
import StatusIndicator from '../components/StatusIndicator.vue'
import DataTable from '../components/DataTable.vue'
import JsonViewer from '../components/JsonViewer.vue'
import QueryInfoCard from '../components/QueryInfoCard.vue'
import WorkflowArchitecture from '../components/WorkflowArchitecture.vue'
import StatusTag from '../components/StatusTag.vue'
import { IconFile } from '@arco-design/web-vue/es/icon'
import { Refresh, Download, View, DocumentCopy } from '@element-plus/icons-vue'

export default {
  name: 'FormsTemplates',
  components: {
    Breadcrumb,
    PageHeader,
    LoadingState,
    ErrorState,
    StatusIndicator,
    DataTable,
    JsonViewer,
    QueryInfoCard,
    WorkflowArchitecture,
    StatusTag,
    IconFile
  },
  data() {
    return {
      loading: false,
      error: null,
      templatesData: null,
      // 查询参数
      queryParams: {
        offset: 0,
        limit: 20,
        sortOrder: 'desc',
        updatedAfter: null,
        updatedBefore: null
      },
      dateRange: null,
      currentPage: 1,
      // 查询相关
      queryTime: null,
      responseTime: null,
      // 模板详情对话框相关
      showTemplateDetailsDialog: false,
      selectedTemplate: null
    }
  },
  computed: {
    headerButtons() {
      return [
        {
          text: '返回首页',
          type: 'default',
          icon: 'ArrowLeft',
          action: 'home'
        },
        {
          text: '刷新数据',
          type: 'primary',
          icon: Refresh,
          loading: this.loading,
          action: 'refresh'
        },
        {
          text: '最近模板',
          type: 'success',
          icon: View,
          action: 'recent-templates'
        }
      ]
    },
    
    errorSuggestions() {
      return [
        '检查网络连接是否正常',
        '确认已完成 Autodesk 认证',
        '验证项目权限设置',
        '联系管理员检查 API 配置'
      ]
    },
    
    errorButtons() {
      return [
        {
          text: '重新认证',
          type: 'primary',
          action: 'auth'
        },
        {
          text: '重试',
          type: 'default',
          action: 'retry'
        }
      ]
    },
    
    tableColumns() {
      return [
        {
          prop: 'name',
          label: '模板名称',
          minWidth: 200,
          showOverflowTooltip: true
        },
        {
          prop: 'status',
          label: '状态',
          width: 100,
          slot: 'status'
        },
        {
          prop: 'createdAt',
          label: '创建时间',
          width: 180,
          type: 'datetime'
        },
        {
          prop: 'updatedAt',
          label: '更新时间',
          width: 200,
          slot: 'updated-at'
        },
        {
          prop: 'createdBy',
          label: '创建者',
          width: 120
        },
        {
          label: '工作流',
          width: 100,
          slot: 'workflow-info'
        }
      ]
    },

    formFieldColumns() {
      return [
        {
          prop: 'name',
          label: '字段名称',
          minWidth: 150
        },
        {
          prop: 'type',
          label: '字段类型',
          width: 120
        },
        {
          prop: 'required',
          label: '必填',
          width: 80,
          type: 'tag',
          tagMap: {
            true: { type: 'danger', text: '是' },
            false: { type: 'success', text: '否' }
          }
        },
        {
          prop: 'label',
          label: '标签',
          minWidth: 150
        }
      ]
    },
    
    tableActions() {
      return [
        {
          text: '导出数据',
          type: 'success',
          icon: Download,
          action: 'export'
        },
        {
          text: '刷新',
          type: 'primary',
          icon: Refresh,
          action: 'refresh'
        }
      ]
    },
    
    rowOperations() {
      return [
        {
          text: '查看详情',
          type: 'primary',
          icon: View,
          action: 'view'
        }
      ]
    }
  },
  mounted() {
    this.fetchTemplatesData()
  },
  methods: {
    async fetchTemplatesData() {
      this.loading = true
      this.error = null
      
      // 记录查询开始时间
      const startTime = Date.now()
      this.queryTime = new Date()
      
      console.log('开始获取模板数据...', this.queryParams)
      
      try {
        const response = await axios.get('/api/forms/templates', {
          params: this.queryParams,
          timeout: 30000 // 30秒超时
        })
        
        // 计算响应时间
        const endTime = Date.now()
        this.responseTime = `${endTime - startTime}ms`
        
        console.log('API响应:', response)
        
        if (response.headers['content-type']?.includes('application/json')) {
          this.templatesData = response.data
          console.log('模板数据获取成功:', this.templatesData)
        } else {
          console.log('响应不是JSON格式，可能需要重新认证')
          throw new Error('需要重新认证')
        }
      } catch (error) {
        console.error('获取模板数据失败:', error)
        
        if (error.code === 'ECONNABORTED') {
          this.error = '请求超时，请检查网络连接或稍后重试'
        } else if (error.response?.status === 401) {
          this.error = '未找到 Access Token，请先进行认证'
        } else if (error.response?.status === 403) {
          this.error = '权限不足，请检查账户权限设置'
        } else if (error.response?.status === 404) {
          this.error = 'API 端点不存在，请检查服务器配置'
        } else if (error.response?.status >= 500) {
          this.error = '服务器内部错误，请稍后重试或联系管理员'
        } else {
          this.error = `获取模板数据时发生错误: ${error.response?.data?.message || error.message}`
        }
      } finally {
        this.loading = false
        console.log('模板数据获取完成，loading状态:', this.loading)
      }
    },

    refreshWithParams() {
      this.currentPage = 1
      this.queryParams.offset = 0
      this.fetchTemplatesData()
    },

    resetParams() {
      this.queryParams = {
        offset: 0,
        limit: 20,
        sortOrder: 'desc',
        updatedAfter: null,
        updatedBefore: null
      }
      this.dateRange = null
      this.currentPage = 1
      this.fetchTemplatesData()
    },

    handleDateRangeChange(dates) {
      if (dates && dates.length === 2) {
        this.queryParams.updatedAfter = dates[0].toISOString()
        this.queryParams.updatedBefore = dates[1].toISOString()
      } else {
        this.queryParams.updatedAfter = null
        this.queryParams.updatedBefore = null
      }
    },

    handlePageChange(page) {
      this.currentPage = page
      this.queryParams.offset = (page - 1) * this.queryParams.limit
      this.fetchTemplatesData()
    },

    getTotalCount() {
      // 优先使用分页信息中的总数，否则使用当前数据长度
      if (this.templatesData?.pagination?.total) {
        return this.templatesData.pagination.total
      }
      if (this.templatesData?.templates?.pagination?.total) {
        return this.templatesData.templates.pagination.total
      }
      // 如果没有分页信息，使用当前数据长度作为估算
      return this.templatesData?.templates?.data?.length || 0
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      try {
        return new Date(dateString).toLocaleString('zh-CN')
      } catch {
        return dateString
      }
    },

    getTimeAgo(dateString) {
      if (!dateString) return ''
      try {
        const date = new Date(dateString)
        const now = new Date()
        const diffMs = now - date
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
        const diffMinutes = Math.floor(diffMs / (1000 * 60))

        if (diffDays > 0) {
          return `${diffDays}天前`
        } else if (diffHours > 0) {
          return `${diffHours}小时前`
        } else if (diffMinutes > 0) {
          return `${diffMinutes}分钟前`
        } else {
          return '刚刚'
        }
      } catch {
        return ''
      }
    },

    getTemplateStatus(status) {
      switch(status) {
        case 'active': return 'success'
        case 'draft': return 'warning'
        case 'archived': return 'info'
        default: return 'info'
      }
    },

    hasWorkflowInfo(template) {
      const workflowInfo = this.getTemplateWorkflowInfo(template)
      return workflowInfo && (
        this.hasRolesAndPermissions(template) ||
        this.hasStatuses(template) ||
        this.hasWorkflowRules(template) ||
        this.hasParticipants(template)
      )
    },

    getTemplateWorkflowInfo(template) {
      if (!this.templatesData?.workflow_architecture) return null
      const workflowInfo = this.templatesData.workflow_architecture.find(arch => arch.template_id === template.id)
      
      // Enhance workflow info with architecture summary and template data
      if (workflowInfo) {
        return {
          ...workflowInfo,
          architecture_summary: this.templatesData.architecture_summary,
          templatesData: this.templatesData
        }
      }
      
      return workflowInfo
    },

    // Helper functions for workflow info checking
    hasRolesAndPermissions(template) {
      const workflowInfo = this.getTemplateWorkflowInfo(template)
      return workflowInfo && workflowInfo.roles_and_permissions && 
             Object.keys(workflowInfo.roles_and_permissions).length > 0
    },

    hasStatuses(template) {
      const workflowInfo = this.getTemplateWorkflowInfo(template)
      return workflowInfo && workflowInfo.statuses && workflowInfo.statuses.length > 0
    },

    hasWorkflowRules(template) {
      const workflowInfo = this.getTemplateWorkflowInfo(template)
      return workflowInfo && workflowInfo.workflow_rules && 
             Object.keys(workflowInfo.workflow_rules).length > 0
    },

    hasParticipants(template) {
      const workflowInfo = this.getTemplateWorkflowInfo(template)
      return workflowInfo && workflowInfo.participants && workflowInfo.participants.length > 0
    },

    async downloadTemplateData() {
      if (!this.selectedTemplate) return
      
      try {
        const dataStr = JSON.stringify(this.selectedTemplate, null, 2)
        const dataBlob = new Blob([dataStr], { type: 'application/json' })
        
        const url = window.URL.createObjectURL(dataBlob)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `template_${this.selectedTemplate.name || 'data'}_${Date.now()}.json`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        this.$message.success('模板数据导出成功')
      } catch (error) {
        console.error('导出模板数据失败:', error)
        this.$message.error('导出失败')
      }
    },

    async exportData() {
      try {
        const dataStr = JSON.stringify(this.templatesData, null, 2)
        const dataBlob = new Blob([dataStr], { type: 'application/json' })
        
        const url = window.URL.createObjectURL(dataBlob)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `templates_${Date.now()}.json`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        this.$message.success('数据导出成功')
      } catch (error) {
        console.error('导出失败:', error)
        this.$message.error(`导出失败: ${error.message}`)
      }
    },
    
    startAuth() {
      window.location.href = '/auth/start'
    },
    
    refreshData() {
      this.fetchTemplatesData()
    },
    
    cancelLoading() {
      this.loading = false
      this.error = '加载已取消'
      console.log('用户取消了加载操作')
    },
    
    // 显示模板详情
    showTemplateDetails(template) {
      this.selectedTemplate = template
      this.showTemplateDetailsDialog = true
    },
    
    // 事件处理方法
    handleHeaderAction(action) {
      switch(action) {
        case 'home':
          this.$router.push('/')
          break
        case 'refresh':
          this.refreshData()
          break
        case 'recent-templates':
          this.$router.push('/forms/templates/recent')
          break
      }
    },
    
    handleErrorAction(action) {
      switch(action) {
        case 'auth':
          this.startAuth()
          break
        case 'retry':
          this.refreshData()
          break
      }
    },
    
    handleTableAction(action) {
      switch(action) {
        case 'export':
          this.exportData()
          break
        case 'refresh':
          this.refreshData()
          break
      }
    },
    
    handleRowOperation(action, button, index) {
      const [operation, rowIndex] = action.split(':')
      const template = this.templatesData.templates?.data[parseInt(rowIndex)]
      
      switch(operation) {
        case 'view':
          this.showTemplateDetails(template)
          break
      }
    },

    // QueryInfoCard 相关方法
    getApiEndpoint() {
      const baseUrl = window.location.origin
      return `${baseUrl}/api/forms/templates`
    },

    getQueryDescription() {
      const params = this.queryParams
      let description = `获取表单模板列表`
      
      if (params.updatedAfter || params.updatedBefore) {
        description += '，按更新时间筛选'
      }
      
      description += `，每页${params.limit}条，${params.sortOrder === 'desc' ? '最新优先' : '最旧优先'}排序`
      
      return description
    },

    getFormattedQueryParams() {
      const formatted = {}
      Object.keys(this.queryParams).forEach(key => {
        const value = this.queryParams[key]
        if (value !== null && value !== undefined) {
          formatted[key] = value
        }
      })
      return formatted
    },

    getResponseTime() {
      return this.responseTime
    },

    getCustomQueryFields() {
      const fields = []
      
      // 当前页码
      fields.push({
        label: '当前页码',
        value: Math.floor(this.queryParams.offset / this.queryParams.limit) + 1,
        component: 'StatusTag',
        props: { status: 'info', size: 'small', showIcon: false }
      })
      
      // 分页信息
      if (this.templatesData?.pagination) {
        const pagination = this.templatesData.pagination
        if (pagination.total) {
          fields.push({
            label: '总记录数',
            value: pagination.total,
            component: 'StatusTag',
            props: { status: 'success', size: 'small', showIcon: false }
          })
        }
      }
      
      // 架构统计
      if (this.templatesData?.architecture_summary) {
        const summary = this.templatesData.architecture_summary
        fields.push({
          label: '包含工作流',
          value: `${summary.templates_with_workflow_rules || 0}个`,
          component: 'StatusTag',
          props: { status: 'warning', size: 'small', showIcon: false }
        })
      }
      
      return fields
    },

    getQueryActions() {
      return [
        {
          text: '刷新查询',
          type: 'primary',
          icon: Refresh,
          event: 'refresh'
        },
        {
          text: '重置参数',
          type: 'default',
          event: 'reset'
        },
        {
          text: '复制API',
          type: 'info',
          icon: DocumentCopy,
          handler: () => this.copyApiEndpoint()
        }
      ]
    },

    async copyApiEndpoint() {
      try {
        const endpoint = this.getApiEndpoint()
        await navigator.clipboard.writeText(endpoint)
        this.$message.success('API端点已复制到剪贴板')
      } catch (error) {
        console.error('复制失败:', error)
        this.$message.error('复制失败')
      }
    }
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.forms-templates {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.query-control-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.query-controls {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.control-row {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.control-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-item label {
  font-size: 14px;
  color: var(--color-text-primary);
  white-space: nowrap;
}

.update-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.update-time {
  font-size: 13px;
  color: var(--color-text-primary);
}

.update-ago {
  font-size: 11px;
  color: var(--color-text-secondary);
  font-style: italic;
}

.workflow-preview {
  display: flex;
  align-items: center;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin: 24px 0;
}

.summary-card {
  margin-top: 24px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.summary-item {
  text-align: center;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
}

.summary-number {
  font-size: 24px;
  font-weight: bold;
  color: var(--color-primary);
  margin-bottom: 8px;
}

.summary-label {
  font-size: 12px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

/* 模板详情对话框样式 */
.template-details-dialog {
  --el-dialog-padding-primary: 0;
}

.template-details-content {
  max-height: 80vh;
  overflow-y: auto;
  padding: 0 24px;
}

.details-section {
  margin-bottom: 20px;
}

.details-section:last-child {
  margin-bottom: 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}


.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--color-border-light);
  background: var(--color-bg-secondary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .forms-templates {
    padding: var(--spacing-md);
  }
  
  .control-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
  
  .roles-grid {
    grid-template-columns: 1fr;
  }
  
  .template-details-content {
    padding: 0 12px;
  }
}
</style>
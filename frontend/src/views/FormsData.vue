<template>
  <div class="forms-data">
    <!-- 面包屑导航 -->
    <Breadcrumb />
    
    <!-- 页面头部 -->
    <PageHeader
      title="项目表单数据中心"
      description="查看和管理 Autodesk Construction Cloud 项目中的所有表单数据"
      :icon="IconDashboard"
      tag="实时数据"
      tag-type="success"
      :action-buttons="headerButtons"
      :show-breadcrumb="false"
      :show-stats="false"
      @action="handleHeaderAction" />

    <!-- 加载状态 -->
    <LoadingState 
      v-if="loading"
      type="card"
      title="正在获取表单数据"
      text="请稍候，正在从服务器获取最新的表单数据..."
      :show-progress="false"
      :show-cancel="true"
      @cancel="cancelLoading" />

    <!-- 错误状态 -->
    <ErrorState
      v-if="error"
      type="card"
      severity="error"
      title="获取表单数据失败"
      :message="error"
      :suggestions="errorSuggestions"
      :action-buttons="errorButtons"
      @action="handleErrorAction" />

    <!-- 成功状态指示器 -->
    <StatusIndicator
      v-if="formsData && !loading && !error"
      status="success"
      :title="`数据获取成功！`"
      :description="`成功获取 ${formsData.forms?.length || 0} 个表单数据`"
      :details="`最后更新时间: ${new Date().toLocaleString('zh-CN')}`"
      size="default"
      style="margin-bottom: 24px;" />

    <!-- 查询信息卡片 -->
    <QueryInfoCard
      v-if="formsData && !loading && !error"
      title="表单数据查询"
      api-endpoint="/api/forms/jarvis"
      description="获取 isBIM JARVIS 2025 Dev 项目的所有表单数据"
      :result-count="formsData.forms?.length || 0"
      result-unit="个表单"
      :custom-fields="getFormsQueryFields()" />

    <!-- 表单数据内容 -->
    <div v-if="formsData && !loading && !error">
      <!-- 表单数据表格 -->
      <DataTable
        :data="formsData.forms || []"
        :columns="tableColumns"
        :loading="loading"
        title="📋 表单详细信息"
        description="展开每一行查看表单的详细内容和工作记录"
        :action-buttons="tableActions"
        :operations="rowOperations"
        :show-index="true"
        @action="handleTableAction"
        @row-operation="handleRowOperation">
        
        <!-- 表单状态列 -->
        <template #status="{ row }">
          <StatusTag
            :status="row.status || 'unknown'"
            size="small"
            :show-icon="false" />
        </template>
        
        <!-- PDF可用状态列 -->
        <template #pdf-status="{ row }">
          <StatusTag
            :status="row.pdfUrl ? 'available' : 'unavailable'"
            :text="row.pdfUrl ? '✓ 可用' : '✗ 不可用'"
            size="small"
            :show-icon="false" />
        </template>
        
        <!-- 工作记录统计列 -->
        <template #work-stats="{ row }">
          <div class="work-stats">
            <StatusTag 
              status="info" 
              :text="`日志: ${row.tabularValues?.worklogEntries?.length || 0}`"
              size="small" 
              :show-icon="false" />
            <StatusTag 
              status="success" 
              :text="`材料: ${row.tabularValues?.materialsEntries?.length || 0}`"
              size="small" 
              :show-icon="false"
              style="margin-left: 4px;" />
            <StatusTag 
              status="warning" 
              :text="`设备: ${row.tabularValues?.equipmentEntries?.length || 0}`"
              size="small" 
              :show-icon="false"
              style="margin-left: 4px;" />
          </div>
        </template>
        
      </DataTable>

      <!-- JSON 数据查看器 -->
      <div style="margin-top: 32px;">
        <JsonViewer
          :data="formsData"
          title="表单原始数据"
          :collapsible="true"
          :show-controls="true"
          max-height="500px"
          theme="light" />
      </div>
    </div>

    <!-- 表单详情对话框 -->
    <el-dialog
      v-model="showFormDetailsDialog"
      :title="selectedForm ? `📋 表单详情 - ${selectedForm.name}` : '表单详情'"
      width="90%"
      :max-width="1200"
      top="5vh"
      :close-on-click-modal="false"
      :close-on-press-escape="true"
      class="form-details-dialog">
      
      <div v-if="selectedForm" class="form-details-content">
        <!-- 基本信息 -->
        <el-card class="details-section" shadow="never">
          <template #header>
            <div class="section-header">
              <h3>📝 基本信息</h3>
            </div>
          </template>
          
          <el-descriptions :column="2" border>
            <el-descriptions-item label="表单名称">
              <StatusTag 
                status="info" 
                :text="selectedForm.name"
                size="default" 
                :show-icon="false" />
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <StatusIndicator
                :status="selectedForm.status === 'submitted' ? 'success' : 'warning'"
                :title="selectedForm.status"
                size="small" />
            </el-descriptions-item>
            <el-descriptions-item label="表单日期">
              {{ formatDate(selectedForm.formDate) }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ formatDate(selectedForm.createdAt) }}
            </el-descriptions-item>
            <el-descriptions-item label="创建者">
              <StatusTag 
                status="info" 
                :text="selectedForm.createdBy || 'N/A'"
                size="small" 
                :show-icon="false" />
            </el-descriptions-item>
            <el-descriptions-item label="更新时间">
              {{ formatDate(selectedForm.updatedAt) }}
            </el-descriptions-item>
            <el-descriptions-item label="PDF状态">
              <div class="pdf-status">
                <StatusTag 
                  :status="selectedForm.pdfUrl ? 'available' : 'unavailable'"
                  :text="selectedForm.pdfUrl ? '✓ 可用' : '✗ 不可用'"
                  size="small" 
                  :show-icon="false" />
                <el-button
                  v-if="selectedForm.pdfUrl"
                  type="primary"
                  size="small"
                  :icon="Download"
                  @click="downloadPdf(selectedForm.pdfUrl)"
                  style="margin-left: 8px;">
                  下载PDF
                </el-button>
              </div>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 工作流时间线 -->
        <el-card class="details-section" shadow="never">
          <template #header>
            <div class="section-header">
              <h3>⏰ 工作流时间线</h3>
            </div>
          </template>
          
          <el-timeline>
            <el-timeline-item
              :timestamp="formatDate(selectedForm.createdAt)"
              placement="top"
              type="primary"
              icon="Plus">
              <div class="timeline-content">
                <h4>📝 表单创建</h4>
                <p>创建者: <StatusTag status="info" :text="selectedForm.createdBy || 'N/A'" size="small" :show-icon="false" /></p>
                <p v-if="selectedForm.formDate">表单日期: {{ formatDate(selectedForm.formDate) }}</p>
              </div>
            </el-timeline-item>
            
            <el-timeline-item
              v-if="selectedForm.updatedAt && selectedForm.updatedAt !== selectedForm.createdAt"
              :timestamp="formatDate(selectedForm.updatedAt)"
              placement="top"
              type="success"
              icon="Edit">
              <div class="timeline-content">
                <h4>📝 表单更新</h4>
                <p>最后更新时间</p>
              </div>
            </el-timeline-item>
            
            <el-timeline-item
              :timestamp="getCurrentTimestamp()"
              placement="top"
              :type="getStatusType(selectedForm.status)"
              icon="Flag">
              <div class="timeline-content">
                <h4>📋 当前状态</h4>
                <p>
                  <StatusIndicator
                    :status="selectedForm.status === 'submitted' ? 'success' : 'warning'"
                    :title="selectedForm.status"
                    size="small" />
                </p>
                <p v-if="workflowInfo.length > 0" class="workflow-info">
                  <strong>工作流信息:</strong>
                  <span v-for="(info, index) in workflowInfo" :key="index">
                    <StatusTag status="info" :text="info" size="small" :show-icon="false" style="margin: 2px;" />
                  </span>
                </p>
              </div>
            </el-timeline-item>
          </el-timeline>
        </el-card>

        <!-- 权限和审批信息 -->
        <el-card v-if="hasPermissionInfo" class="details-section" shadow="never">
          <template #header>
            <div class="section-header">
              <h3>👥 权限和审批信息</h3>
            </div>
          </template>
          
          <el-descriptions :column="2" border>
            <el-descriptions-item v-if="selectedForm.assignee" label="指派给">
              <StatusTag status="warning" :text="selectedForm.assignee" size="small" :show-icon="false" />
            </el-descriptions-item>
            <el-descriptions-item v-if="selectedForm.reviewer" label="审核者">
              <StatusTag status="info" :text="selectedForm.reviewer" size="small" :show-icon="false" />
            </el-descriptions-item>
            <el-descriptions-item v-if="selectedForm.approver" label="审批者">
              <StatusTag status="success" :text="selectedForm.approver" size="small" :show-icon="false" />
            </el-descriptions-item>
            <el-descriptions-item v-if="selectedForm.signature" label="签名状态">
              <StatusTag 
                :status="selectedForm.signature ? 'success' : 'pending'"
                :text="selectedForm.signature ? '已签名' : '未签名'"
                size="small" 
                :show-icon="false" />
            </el-descriptions-item>
          </el-descriptions>
          
          <!-- 权限详情 -->
          <div v-if="permissionDetails.length > 0" style="margin-top: 16px;">
            <h4>🔐 权限详情</h4>
            <div class="permission-grid">
              <div v-for="(perm, index) in permissionDetails" :key="index" class="permission-item">
                <div class="permission-label">{{ perm.label }}</div>
                <div class="permission-value">{{ perm.value }}</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 工作记录统计 -->
        <el-card class="details-section" shadow="never">
          <template #header>
            <div class="section-header">
              <h3>📊 工作记录统计</h3>
            </div>
          </template>
          
          <div class="work-stats-grid">
            <div class="stat-item">
              <div class="stat-icon">📝</div>
              <div class="stat-content">
                <div class="stat-number">{{ selectedForm.tabularValues?.worklogEntries?.length || 0 }}</div>
                <div class="stat-label">工作日志条目</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">🧱</div>
              <div class="stat-content">
                <div class="stat-number">{{ selectedForm.tabularValues?.materialsEntries?.length || 0 }}</div>
                <div class="stat-label">材料记录条目</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">🔧</div>
              <div class="stat-content">
                <div class="stat-number">{{ selectedForm.tabularValues?.equipmentEntries?.length || 0 }}</div>
                <div class="stat-label">设备记录条目</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 表单工作流信息 (如果有模板信息) -->
        <div v-if="getFormWorkflowInfo(selectedForm)" class="details-section">
          <WorkflowArchitecture
            :workflow-info="getFormWorkflowInfo(selectedForm)"
            :default-active-items="['structure', 'approval-settings']" />
        </div>

        <!-- 详细工作记录 -->
        <el-collapse v-model="activeCollapseItems" class="details-section">
          <!-- 工作日志 -->
          <el-collapse-item name="worklog" v-if="selectedForm.tabularValues?.worklogEntries?.length > 0">
            <template #title>
              <div class="collapse-title">
                <span class="collapse-icon">📝</span>
                <span>工作日志记录 ({{ selectedForm.tabularValues.worklogEntries.length }})</span>
              </div>
            </template>
            
            <DataTable
              :data="selectedForm.tabularValues.worklogEntries"
              :columns="worklogColumns"
              :show-index="true"
              :show-pagination="false"
              size="small">
              
              <template #timespan="{ row }">
                <StatusTag 
                  status="info" 
                  :text="`${convertTimespan(row.timespan)}h`"
                  size="small" 
                  :show-icon="false" />
              </template>
            </DataTable>
          </el-collapse-item>

          <!-- 材料记录 -->
          <el-collapse-item name="materials" v-if="selectedForm.tabularValues?.materialsEntries?.length > 0">
            <template #title>
              <div class="collapse-title">
                <span class="collapse-icon">🧱</span>
                <span>材料记录 ({{ selectedForm.tabularValues.materialsEntries.length }})</span>
              </div>
            </template>
            
            <DataTable
              :data="selectedForm.tabularValues.materialsEntries"
              :columns="materialsColumns"
              :show-index="true"
              :show-pagination="false"
              size="small" />
          </el-collapse-item>

          <!-- 设备记录 -->
          <el-collapse-item name="equipment" v-if="selectedForm.tabularValues?.equipmentEntries?.length > 0">
            <template #title>
              <div class="collapse-title">
                <span class="collapse-icon">🔧</span>
                <span>设备记录 ({{ selectedForm.tabularValues.equipmentEntries.length }})</span>
              </div>
            </template>
            
            <DataTable
              :data="selectedForm.tabularValues.equipmentEntries"
              :columns="equipmentColumns"
              :show-index="true"
              :show-pagination="false"
              size="small" />
          </el-collapse-item>

          <!-- 其他字段值 -->
          <el-collapse-item name="custom-values" v-if="hasCustomValues">
            <template #title>
              <div class="collapse-title">
                <span class="collapse-icon">📋</span>
                <span>其他表单字段</span>
              </div>
            </template>
            
            <div class="custom-values-grid">
              <div v-for="(value, key) in customValues" :key="key" class="custom-value-item">
                <div class="custom-value-label">{{ key }}</div>
                <div class="custom-value-content">{{ value }}</div>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>

        <!-- 原始数据查看 -->
        <el-card class="details-section" shadow="never">
          <template #header>
            <div class="section-header">
              <h3>🔍 原始数据</h3>
            </div>
          </template>
          
          <JsonViewer
            :data="selectedForm"
            title=""
            :collapsible="true"
            :show-controls="true"
            max-height="400px"
            theme="light" />
        </el-card>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showFormDetailsDialog = false">关闭</el-button>
          <el-button type="primary" @click="downloadFormData" :icon="Download">
            导出表单数据
          </el-button>
        </div>
      </template>
    </el-dialog>

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
import axios from 'axios'
import Breadcrumb from '../components/Breadcrumb.vue'
import PageHeader from '../components/PageHeader.vue'
import LoadingState from '../components/LoadingState.vue'
import ErrorState from '../components/ErrorState.vue'
import StatusIndicator from '../components/StatusIndicator.vue'
import DataTable from '../components/DataTable.vue'
import BaseCard from '../components/BaseCard.vue'
import JsonViewer from '../components/JsonViewer.vue'
import QueryInfoCard from '../components/QueryInfoCard.vue'
import WorkflowArchitecture from '../components/WorkflowArchitecture.vue'
import ProjectSelector from '../components/ProjectSelector.vue'
import StatusTag from '../components/StatusTag.vue'
import projectStore from '../utils/projectStore.js'
import { IconDashboard } from '@arco-design/web-vue/es/icon'
import { Refresh, Download, View } from '@element-plus/icons-vue'

export default {
  name: 'FormsData',
  components: {
    Breadcrumb,
    PageHeader,
    LoadingState,
    ErrorState,
    StatusIndicator,
    DataTable,
    BaseCard,
    JsonViewer,
    QueryInfoCard,
    WorkflowArchitecture,
    ProjectSelector,
    StatusTag,
    IconDashboard
  },
  data() {
    return {
      loading: false,
      error: null,
      formsData: null,
      // 表单详情对话框相关
      showFormDetailsDialog: false,
      selectedForm: null,
      activeCollapseItems: ['worklog', 'materials', 'equipment'],
      // 项目相关
      currentProject: null,
      showProjectSelector: false
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
          text: '导出数据',
          type: 'success',
          icon: Download,
          action: 'export'
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
          label: '表单名称',
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
          prop: 'formDate',
          label: '表单日期',
          width: 120,
          type: 'datetime'
        },
        {
          prop: 'createdAt',
          label: '创建时间',
          width: 180,
          type: 'datetime'
        },
        {
          prop: 'createdBy',
          label: '创建者',
          width: 120
        },
        {
          prop: 'updatedAt',
          label: '更新时间',
          width: 180,
          type: 'datetime'
        },
        {
          label: '工作记录',
          width: 200,
          slot: 'work-stats'
        },
        {
          label: 'PDF状态',
          width: 100,
          slot: 'pdf-status'
        }
      ]
    },
    
    worklogColumns() {
      return [
        {
          prop: 'trade',
          label: '工种',
          width: 120
        },
        {
          prop: 'headcount',
          label: '人数',
          width: 80,
          type: 'number',
          precision: 0
        },
        {
          label: '工时',
          width: 80,
          slot: 'timespan'
        },
        {
          prop: 'description',
          label: '描述',
          showOverflowTooltip: true
        }
      ]
    },
    
    tableActions() {
      return [
        {
          text: '导出JSON',
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
          text: '查看',
          type: 'primary',
          icon: View,
          action: 'view'
        }
      ]
    },
    
    // 材料记录表格列
    materialsColumns() {
      return [
        {
          prop: 'material',
          label: '材料名称',
          minWidth: 150
        },
        {
          prop: 'quantity',
          label: '数量',
          width: 100,
          type: 'number'
        },
        {
          prop: 'unit',
          label: '单位',
          width: 80
        },
        {
          prop: 'description',
          label: '描述',
          showOverflowTooltip: true
        }
      ]
    },
    
    // 设备记录表格列
    equipmentColumns() {
      return [
        {
          prop: 'equipment',
          label: '设备名称',
          minWidth: 150
        },
        {
          prop: 'hours',
          label: '使用小时',
          width: 100,
          type: 'number'
        },
        {
          prop: 'operator',
          label: '操作员',
          width: 120
        },
        {
          prop: 'description',
          label: '描述',
          showOverflowTooltip: true
        }
      ]
    },
    
    // 检查是否有自定义字段值
    hasCustomValues() {
      return Object.keys(this.customValues).length > 0
    },
    
    // 检查是否有权限信息
    hasPermissionInfo() {
      if (!this.selectedForm) return false
      const permissionFields = ['assignee', 'reviewer', 'approver', 'signature', 'permissions', 'userPermissions', 'groupPermissions']
      return permissionFields.some(field => this.selectedForm[field])
    },
    
    // 获取工作流信息
    workflowInfo() {
      if (!this.selectedForm) return []
      
      const workflowInfo = []
      
      // 检查工作流相关字段
      const workflowFields = {
        'assignee': '指派给',
        'reviewer': '审核者', 
        'approver': '审批者',
        'signature': '签名状态',
        'workflow': '工作流',
        'process': '流程'
      }
      
      Object.keys(workflowFields).forEach(key => {
        if (this.selectedForm[key]) {
          workflowInfo.push(`${workflowFields[key]}: ${this.selectedForm[key]}`)
        }
      })
      
      return workflowInfo
    },
    
    // 获取权限详情
    permissionDetails() {
      if (!this.selectedForm) return []
      
      const permissions = []
      
      // 检查用户权限
      if (this.selectedForm.userPermissions && Array.isArray(this.selectedForm.userPermissions)) {
        this.selectedForm.userPermissions.forEach((perm, index) => {
          permissions.push({
            label: `用户权限 ${index + 1}`,
            value: typeof perm === 'object' ? JSON.stringify(perm) : perm
          })
        })
      }
      
      // 检查组权限
      if (this.selectedForm.groupPermissions && Array.isArray(this.selectedForm.groupPermissions)) {
        this.selectedForm.groupPermissions.forEach((perm, index) => {
          permissions.push({
            label: `组权限 ${index + 1}`,
            value: typeof perm === 'object' ? JSON.stringify(perm) : perm
          })
        })
      }
      
      // 检查其他权限相关字段
      const otherPermissionFields = ['permissions', 'roles', 'access', 'capabilities']
      otherPermissionFields.forEach(field => {
        if (this.selectedForm[field]) {
          permissions.push({
            label: field,
            value: typeof this.selectedForm[field] === 'object' ? JSON.stringify(this.selectedForm[field]) : this.selectedForm[field]
          })
        }
      })
      
      return permissions
    },
    
    // 获取自定义字段值
    customValues() {
      if (!this.selectedForm) return {}
      
      const excludedKeys = ['name', 'status', 'formDate', 'createdAt', 'updatedAt', 'createdBy', 'pdfUrl', 'tabularValues', 'id', 'urn']
      const customValues = {}
      
      Object.keys(this.selectedForm).forEach(key => {
        if (!excludedKeys.includes(key) && this.selectedForm[key] !== null && this.selectedForm[key] !== undefined) {
          customValues[key] = this.selectedForm[key]
        }
      })
      
      return customValues
    }
  },
  mounted() {
    this.initializeProject()
  },
  methods: {
    async fetchFormsData() {
      if (!this.currentProject) {
        this.error = '未选择项目，无法获取表单数据'
        return
      }

      this.loading = true
      this.error = null
      
      console.log('开始获取表单数据...', '项目:', this.currentProject.name)
      
      try {
        const response = await axios.get('/api/forms/jarvis', {
          timeout: 30000, // 30秒超时
          params: {
            projectId: this.currentProject.id
          }
        })
        
        console.log('API响应:', response)
        
        // 检查响应类型
        if (response.headers['content-type']?.includes('application/json')) {
          this.formsData = response.data
          console.log('表单数据获取成功:', this.formsData)
        } else {
          // 如果返回HTML，说明需要重新认证
          console.log('响应不是JSON格式，可能需要重新认证')
          throw new Error('需要重新认证')
        }
      } catch (error) {
        console.error('获取表单数据失败:', error)
        
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
          this.error = `获取表单数据时发生错误: ${error.response?.data?.message || error.message}`
        }
      } finally {
        this.loading = false
        console.log('表单数据获取完成，loading状态:', this.loading)
      }
    },

    getTotalWorklogEntries() {
      if (!this.formsData?.forms) return 0
      return this.formsData.forms.reduce((total, form) => {
        return total + (form.tabularValues?.worklogEntries?.length || 0)
      }, 0)
    },

    getTotalMaterialsEntries() {
      if (!this.formsData?.forms) return 0
      return this.formsData.forms.reduce((total, form) => {
        return total + (form.tabularValues?.materialsEntries?.length || 0)
      }, 0)
    },

    getTotalEquipmentEntries() {
      if (!this.formsData?.forms) return 0
      return this.formsData.forms.reduce((total, form) => {
        return total + (form.tabularValues?.equipmentEntries?.length || 0)
      }, 0)
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      try {
        return new Date(dateString).toLocaleString('zh-CN')
      } catch {
        return dateString
      }
    },

    async exportJson() {
      try {
        const response = await axios.get('/api/forms/export-json', {
          responseType: 'blob'
        })
        
        // 创建下载链接
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `forms_data_${Date.now()}.json`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        this.$message.success('JSON数据导出成功')
      } catch (error) {
        console.error('导出失败:', error)
        this.$message.error(`导出失败: ${error.response?.data?.message || error.message}`)
      }
    },
    
    startAuth() {
      window.location.href = '/auth/start'
    },
    
    refreshData() {
      this.fetchFormsData()
    },
    
    cancelLoading() {
      this.loading = false
      this.error = '加载已取消'
      console.log('用户取消了加载操作')
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
        case 'export':
          this.exportJson()
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
          this.exportJson()
          break
        case 'refresh':
          this.refreshData()
          break
      }
    },
    
    handleRowOperation(action, button, index) {
      const [operation, rowIndex] = action.split(':')
      const row = this.formsData.forms[parseInt(rowIndex)]
      
      switch(operation) {
        case 'view':
          this.showFormDetails(row)
          break
      }
    },
    
    // 显示表单详情
    showFormDetails(form) {
      this.selectedForm = form
      this.showFormDetailsDialog = true
      this.activeCollapseItems = ['worklog', 'materials', 'equipment']
    },
    
    // 转换时间跨度（从毫秒转换为小时）
    convertTimespan(timespan) {
      if (!timespan) return '0'
      // 假设 timespan 是毫秒，转换为小时
      const hours = timespan / (1000 * 60 * 60)
      return hours.toFixed(2)
    },
    
    
    // 下载 PDF
    async downloadPdf(pdfUrl) {
      try {
        this.$message.info('正在下载 PDF...')
        
        // 直接打开 PDF 链接
        window.open(pdfUrl, '_blank')
        
        this.$message.success('PDF 链接已打开')
      } catch (error) {
        console.error('下载 PDF 失败:', error)
        this.$message.error('下载 PDF 失败')
      }
    },
    
    // 导出表单数据
    downloadFormData() {
      if (!this.selectedForm) return
      
      try {
        const dataStr = JSON.stringify(this.selectedForm, null, 2)
        const dataBlob = new Blob([dataStr], { type: 'application/json' })
        
        const url = window.URL.createObjectURL(dataBlob)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `form_${this.selectedForm.name || 'data'}_${Date.now()}.json`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        this.$message.success('表单数据导出成功')
      } catch (error) {
        console.error('导出表单数据失败:', error)
        this.$message.error('导出失败')
      }
    },
    
    // 获取当前时间戳
    getCurrentTimestamp() {
      return new Date().toLocaleString('zh-CN')
    },
    
    // 获取状态类型
    getStatusType(status) {
      switch(status) {
        case 'submitted': return 'success'
        case 'approved': return 'success'
        case 'rejected': return 'danger'
        case 'pending': return 'warning'
        case 'draft': return 'info'
        default: return 'info'
      }
    },

    // QueryInfoCard 相关方法
    getFormsQueryFields() {
      if (!this.formsData) return []
      
      const fields = []
      
      // 工作记录统计
      const totalWorklog = this.getTotalWorklogEntries()
      const totalMaterials = this.getTotalMaterialsEntries()
      const totalEquipment = this.getTotalEquipmentEntries()
      
      fields.push({
        label: '工作日志',
        value: `${totalWorklog}条`,
        component: 'StatusTag',
        props: { status: 'info', size: 'small', showIcon: false }
      })
      
      fields.push({
        label: '材料记录',
        value: `${totalMaterials}条`,
        component: 'StatusTag',
        props: { status: 'success', size: 'small', showIcon: false }
      })
      
      fields.push({
        label: '设备记录',
        value: `${totalEquipment}条`,
        component: 'StatusTag',
        props: { status: 'warning', size: 'small', showIcon: false }
      })
      
      // PDF可用统计
      const formsWithPdf = this.formsData.forms?.filter(form => form.pdfUrl)?.length || 0
      fields.push({
        label: 'PDF可用',
        value: `${formsWithPdf}个`,
        component: 'StatusTag',
        props: { status: 'info', size: 'small', showIcon: false }
      })
      
      return fields
    },

    // 获取表单工作流信息 (从表单数据中提取)
    getFormWorkflowInfo(form) {
      if (!form) return null

      // 从表单数据中提取工作流相关信息
      const workflowInfo = {
        template_id: form.id,
        template_name: form.name,
        roles_and_permissions: {},
        statuses: [],
        workflow_rules: {},
        participants: [],
        template_structure: {
          total_keys: Object.keys(form).length,
          top_level_keys: Object.keys(form),
          has_form_definition: !!form.formDefinition,
          has_workflow: !!form.workflow,
          has_settings: !!form.settings,
          has_permissions: !!form.permissions
        },
        form_fields: [],
        approval_settings: {}
      }

      // 提取审批设置
      const approvalKeys = ['status', 'assignee', 'reviewer', 'approver', 'signature', 'workflow']
      approvalKeys.forEach(key => {
        if (form[key] !== undefined && form[key] !== null) {
          workflowInfo.approval_settings[key] = form[key]
        }
      })

      // 如果有任何工作流相关信息，返回数据，否则返回null
      const hasWorkflowInfo = Object.keys(workflowInfo.approval_settings).length > 0 ||
                              workflowInfo.template_structure.has_workflow ||
                              workflowInfo.template_structure.has_permissions

      return hasWorkflowInfo ? workflowInfo : null
    },

    // 项目初始化方法
    async initializeProject() {
      // 检查URL参数中是否有项目ID
      const projectId = this.$route.query.projectId
      const projectName = this.$route.query.projectName
      
      if (projectId) {
        // 从URL参数获取项目信息
        this.currentProject = {
          id: projectId,
          name: projectName || projectId
        }
        console.log('从URL获取项目信息:', this.currentProject)
      } else {
        // 尝试从localStorage获取之前选择的项目
        const savedProject = projectStore.getSelectedProject()
        if (savedProject) {
          this.currentProject = savedProject
          console.log('从localStorage获取项目信息:', this.currentProject)
        }
      }

      if (this.currentProject) {
        // 有项目信息，开始获取数据
        this.fetchFormsData()
      } else {
        // 没有项目信息，显示项目选择对话框
        this.showProjectSelector = true
      }
    },

    // 处理项目选择确认
    handleProjectSelected(selectedProject) {
      this.currentProject = selectedProject
      projectStore.saveSelectedProject(selectedProject)
      this.$message.success(`已选择项目: ${selectedProject.name}`)
      this.fetchFormsData()
    },

    // 处理项目选择取消
    handleProjectSelectionCancel() {
      // 如果取消选择且没有当前项目，返回首页
      if (!this.currentProject) {
        this.$router.push('/')
      }
    }
    
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.forms-data {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

/* 表单详情样式 */
.form-details {
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border-radius: var(--border-radius-lg);
  margin: var(--spacing-md);
}

.form-details h4, .form-details h5 {
  color: var(--color-text-primary);
  margin: var(--spacing-lg) 0 var(--spacing-md) 0;
  font-weight: 600;
}

/* 工作记录统计样式 */
.work-records-stats {
  padding: var(--spacing-md) 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-lg);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border-light);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  font-size: 2rem;
  opacity: 0.8;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
  line-height: 1.2;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 工作统计标签 */
.work-stats {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
}

/* 表单详情对话框样式 */
.form-details-dialog {
  --el-dialog-padding-primary: 0;
}

.form-details-content {
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

/* 工作统计网格 */
.work-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 24px;
  opacity: 0.8;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: var(--color-text-primary);
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-top: 4px;
  font-weight: 500;
}

/* 折叠面板样式 */
.collapse-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.collapse-icon {
  font-size: 16px;
}

/* 自定义字段值网格 */
.custom-values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}

.custom-value-item {
  padding: 12px;
  background: var(--color-bg-secondary);
  border-radius: 6px;
  border-left: 3px solid var(--color-primary);
}

.custom-value-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.custom-value-content {
  font-size: 14px;
  color: var(--color-text-primary);
  word-break: break-word;
}

/* PDF状态样式 */
.pdf-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 对话框底部 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--color-border-light);
  background: var(--color-bg-secondary);
}

/* 工作流时间线样式 */
.timeline-content {
  padding: 8px 0;
}

.timeline-content h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.timeline-content p {
  margin: 4px 0;
  font-size: 13px;
  color: var(--color-text-regular);
}

.workflow-info {
  margin-top: 8px;
}

.workflow-info strong {
  color: var(--color-text-primary);
  margin-right: 8px;
}

/* 权限网格样式 */
.permission-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.permission-item {
  padding: 12px;
  background: var(--color-bg-secondary);
  border-radius: 6px;
  border-left: 3px solid var(--color-warning);
}

.permission-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.permission-value {
  font-size: 13px;
  color: var(--color-text-primary);
  word-break: break-word;
  max-height: 100px;
  overflow-y: auto;
}

/* 附加信息样式 */
.additional-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.info-item {
  padding: var(--spacing-md);
  background: var(--color-bg-secondary);
  border-radius: var(--border-radius-md);
  border-left: 4px solid var(--color-primary);
}

.info-item strong {
  color: var(--color-text-primary);
  display: block;
  margin-bottom: var(--spacing-xs);
}

.info-item p {
  color: var(--color-text-regular);
  margin: 0;
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .forms-data {
    padding: var(--spacing-md);
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .stat-card {
    padding: var(--spacing-md);
    gap: var(--spacing-sm);
  }
  
  .stat-icon {
    font-size: 1.5rem;
  }
  
  .stat-value {
    font-size: 1.2rem;
  }
  
  .work-stats {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-xs);
  }
  
  .stat-icon {
    font-size: 1.3rem;
  }
  
  .stat-value {
    font-size: 1.1rem;
  }
  
  /* 表单详情对话框响应式 */
  .work-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .custom-values-grid {
    grid-template-columns: 1fr;
  }
  
  .permission-grid {
    grid-template-columns: 1fr;
  }
  
  .form-details-content {
    padding: 0 12px;
  }
  
  .timeline-content h4 {
    font-size: 13px;
  }
  
  .timeline-content p {
    font-size: 12px;
  }
}
</style>


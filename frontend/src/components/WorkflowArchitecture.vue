<template>
  <div class="workflow-architecture">
    <el-card class="architecture-card" shadow="never">
      <template #header>
        <div class="architecture-header">
          <h3>🔄 工作流架构</h3>
          <div class="architecture-stats">
            <el-tag v-if="hasAnyWorkflow" type="success" size="small">有工作流</el-tag>
            <el-tag v-else type="info" size="small">无工作流</el-tag>
            <el-tag type="primary" size="small">{{ getTotalComponents() }} 个组件</el-tag>
          </div>
        </div>
      </template>

      <div v-if="!hasAnyWorkflow" class="no-workflow">
        <el-empty description="此模板暂无工作流配置" :image-size="100" />
      </div>

      <el-collapse v-else v-model="activeItems" class="workflow-collapse">
        <!-- 架构概览 -->
        <el-collapse-item name="architecture-summary" v-if="hasArchitectureSummary">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">📊</span>
              <span>架构概览</span>
              <el-tag size="small" type="primary" style="margin-left: 8px;">
                {{ getArchitectureSummary().total_templates || 0 }} 个模板
              </el-tag>
            </div>
          </template>

          <div class="architecture-summary-section">
            <div class="summary-stats">
              <div class="stat-row">
                <div class="stat-item">
                  <div class="stat-label">📄 PDF模板</div>
                  <el-tag type="success" size="large">{{ getArchitectureSummary().pdf_templates || 0 }}</el-tag>
                </div>
                <div class="stat-item">
                  <div class="stat-label">👥 有角色权限</div>
                  <el-tag type="warning" size="large">{{ getArchitectureSummary().templates_with_roles || 0 }}</el-tag>
                </div>
                <div class="stat-item">
                  <div class="stat-label">🔄 有工作流</div>
                  <el-tag type="info" size="large">{{ getArchitectureSummary().templates_with_workflow || 0 }}</el-tag>
                </div>
                <div class="stat-item">
                  <div class="stat-label">🎯 总角色数</div>
                  <el-tag type="primary" size="large">{{ getArchitectureSummary().total_roles_found || 0 }}</el-tag>
                </div>
              </div>
              
              <div class="template-types" v-if="getTemplateTypes().length > 0">
                <div class="types-label">📋 模板类型:</div>
                <div class="types-list">
                  <el-tag 
                    v-for="type in getTemplateTypes()" 
                    :key="type" 
                    :type="getTemplateTypeColor(type)"
                    size="small"
                    style="margin: 2px;">
                    {{ formatTemplateType(type) }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>

        <!-- 模板详情 -->
        <el-collapse-item name="template-details" v-if="hasTemplateMetadata">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">📋</span>
              <span>模板详情</span>
              <el-tag size="small" type="success" style="margin-left: 8px;">
                {{ getTemplateName() }}
              </el-tag>
            </div>
          </template>

          <div class="template-details-section">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="模板名称">
                <el-tag type="primary" size="large">{{ getTemplateName() }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="模板类型">
                <el-tag :type="getTemplateTypeColor(getTemplateType())" size="large">
                  {{ formatTemplateType(getTemplateType()) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="创建者">
                <el-tag type="info">{{ getTemplateCreator() }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="更新时间">
                <span>{{ formatDate(getTemplateUpdatedAt()) }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="PDF支持">
                <el-tag :type="isPdfSupported() ? 'success' : 'info'">
                  {{ isPdfSupported() ? '✅ 支持PDF' : '❌ 不支持PDF' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="表单API">
                <el-tag type="warning" v-if="getFormsUrl()">✅ 可用</el-tag>
                <el-tag type="info" v-else>❌ 不可用</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-collapse-item>

        <!-- 角色权限详情 -->
        <el-collapse-item name="roles" v-if="hasRolesAndPermissions">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">👥</span>
              <span>角色权限详情</span>
              <el-tag size="small" type="warning" style="margin-left: 8px;">
                {{ getRolesCount() }} 个角色
              </el-tag>
            </div>
          </template>

          <div class="roles-section">
            <div class="roles-grid">
              <div v-for="(roleData, roleName) in getRolesAndPermissions()" :key="roleName" class="role-card">
                <div class="role-header">
                  <div class="role-info">
                    <div class="role-name">{{ roleName }}</div>
                    <el-tag 
                      size="small" 
                      :type="roleData.type === 'role' ? 'primary' : 'success'"
                      style="margin-top: 4px;">
                      {{ roleData.type === 'role' ? '👥 组角色' : '👤 用户' }}
                    </el-tag>
                    <div v-if="roleData.role_key" class="role-key">
                      <span class="key-label">Key:</span>
                      <code>{{ roleData.role_key }}</code>
                    </div>
                  </div>
                  <div class="role-stats">
                    <el-tag size="small" type="info">{{ roleData.permissions?.length || 0 }} 项权限</el-tag>
                    <el-tag size="small" type="warning">{{ roleData.count || 1 }} 个实例</el-tag>
                  </div>
                </div>
                <div class="permissions-list">
                  <el-tag 
                    v-for="permission in (roleData.permissions || [])" 
                    :key="permission" 
                    size="small" 
                    :type="getPermissionType(permission)"
                    style="margin: 2px;">
                    {{ formatPermission(permission) }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>

        <!-- 模板元数据 -->
        <el-collapse-item name="metadata" v-if="hasTemplateMetadata">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">📋</span>
              <span>模板信息</span>
            </div>
          </template>

          <div class="metadata-section">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="模板类型" v-if="workflowInfo.templateType">
                <el-tag type="primary">{{ workflowInfo.templateType }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="状态" v-if="workflowInfo.status">
                <el-tag :type="workflowInfo.status === 'active' ? 'success' : 'info'">
                  {{ workflowInfo.status }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="创建者" v-if="workflowInfo.createdBy">
                <el-tag type="info">{{ workflowInfo.createdBy }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="项目ID" v-if="workflowInfo.projectId">
                <el-tag type="default" size="small">{{ workflowInfo.projectId }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="PDF支持" v-if="workflowInfo.isPdf !== undefined">
                <el-tag :type="workflowInfo.isPdf ? 'success' : 'info'">
                  {{ workflowInfo.isPdf ? '✅ 支持PDF' : '❌ 不支持PDF' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="更新时间" v-if="workflowInfo.updatedAt">
                <span>{{ formatDate(workflowInfo.updatedAt) }}</span>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-collapse-item>

        <!-- 组权限 -->
        <el-collapse-item name="group-permissions" v-if="hasGroupPermissions">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">👥</span>
              <span>组权限</span>
              <el-tag size="small" type="primary" style="margin-left: 8px;">
                {{ groupPermissions.length }} 个角色组
              </el-tag>
            </div>
          </template>

          <div class="group-permissions-section">
            <div class="permissions-grid">
              <div v-for="group in groupPermissions" :key="group.roleKey" class="permission-group-card">
                <div class="group-header">
                  <div class="group-name">
                    <h4>{{ group.roleName }}</h4>
                    <el-tag size="small" type="info">{{ group.roleKey }}</el-tag>
                  </div>
                  <el-tag size="small" type="primary">{{ group.permissions?.length || 0 }} 项权限</el-tag>
                </div>
                <div class="group-permissions-list">
                  <el-tag 
                    v-for="permission in (group.permissions || [])" 
                    :key="permission" 
                    size="small" 
                    :type="getPermissionType(permission)"
                    style="margin: 2px;">
                    {{ formatPermission(permission) }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>

        <!-- 用户权限 -->
        <el-collapse-item name="user-permissions" v-if="hasUserPermissions">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">👤</span>
              <span>用户权限</span>
              <el-tag size="small" type="success" style="margin-left: 8px;">
                {{ userPermissions.length }} 个用户
              </el-tag>
            </div>
          </template>

          <div class="user-permissions-section">
            <div class="permissions-grid">
              <div v-for="(userPerm, index) in userPermissions" :key="index" class="permission-user-card">
                <div class="user-header">
                  <div class="user-name">
                    <h4>{{ userPerm.userName || userPerm.userId || `用户 ${index + 1}` }}</h4>
                  </div>
                  <el-tag size="small" type="success">{{ userPerm.permissions?.length || 0 }} 项权限</el-tag>
                </div>
                <div class="user-permissions-list">
                  <el-tag 
                    v-for="permission in (userPerm.permissions || [])" 
                    :key="permission" 
                    size="small" 
                    :type="getPermissionType(permission)"
                    style="margin: 2px;">
                    {{ formatPermission(permission) }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>

        <!-- 资源链接 -->
        <el-collapse-item name="resources" v-if="hasResourceLinks">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">🔗</span>
              <span>资源链接</span>
            </div>
          </template>

          <div class="resources-section">
            <div class="resource-links">
              <div v-if="workflowInfo.forms?.url" class="resource-item">
                <div class="resource-label">
                  <span class="resource-icon">📝</span>
                  <span>表单API链接</span>
                </div>
                <div class="resource-value">
                  <el-input 
                    :value="workflowInfo.forms.url" 
                    readonly 
                    size="small">
                    <template #append>
                      <el-button @click="copyToClipboard(workflowInfo.forms.url)" size="small">
                        复制
                      </el-button>
                    </template>
                  </el-input>
                </div>
              </div>

              <div v-if="workflowInfo.pdfUrl" class="resource-item">
                <div class="resource-label">
                  <span class="resource-icon">📄</span>
                  <span>PDF模板链接</span>
                </div>
                <div class="resource-value">
                  <el-input 
                    :value="workflowInfo.pdfUrl" 
                    readonly 
                    size="small">
                    <template #append>
                      <el-button @click="copyToClipboard(workflowInfo.pdfUrl)" size="small">
                        复制
                      </el-button>
                      <el-button @click="openPdfUrl(workflowInfo.pdfUrl)" type="primary" size="small">
                        查看
                      </el-button>
                    </template>
                  </el-input>
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>

        <!-- 状态流程 -->
        <el-collapse-item name="statuses" v-if="hasStatuses">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">📊</span>
              <span>状态流程</span>
              <el-tag size="small" type="warning" style="margin-left: 8px;">
                {{ workflowInfo.statuses?.length || 0 }} 个状态
              </el-tag>
            </div>
          </template>

          <div class="statuses-section">
            <div class="statuses-flow">
              <div 
                v-for="(status, index) in workflowInfo.statuses" 
                :key="status"
                class="status-node">
                <div class="status-item" :class="getStatusClass(status)">
                  <div class="status-number">{{ index + 1 }}</div>
                  <div class="status-name">{{ status }}</div>
                  <el-tag :type="getStatusTagType(status)" size="small">
                    {{ getStatusDescription(status) }}
                  </el-tag>
                </div>
                <div v-if="index < workflowInfo.statuses.length - 1" class="status-arrow">
                  <el-icon><ArrowRight /></el-icon>
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>

        <!-- 工作流规则 -->
        <el-collapse-item name="workflow-rules" v-if="hasWorkflowRules">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">⚙️</span>
              <span>工作流规则</span>
              <el-tag size="small" type="danger" style="margin-left: 8px;">
                {{ Object.keys(workflowInfo.workflow_rules || {}).length }} 项规则
              </el-tag>
            </div>
          </template>

          <div class="workflow-rules-section">
            <div class="rules-grid">
              <div v-for="(rule, key) in workflowInfo.workflow_rules" :key="key" class="rule-card">
                <div class="rule-header">
                  <div class="rule-name">{{ formatRuleName(key) }}</div>
                  <el-tag size="small" :type="getRuleType(key)">{{ getRuleCategory(key) }}</el-tag>
                </div>
                <div class="rule-content">
                  <JsonViewer
                    :data="rule"
                    :title="`规则详情`"
                    :collapsible="true"
                    :show-controls="false"
                    max-height="200px"
                    theme="light" />
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>

        <!-- 参与者信息 -->
        <el-collapse-item name="participants" v-if="hasParticipants">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">👨‍👩‍👧‍👦</span>
              <span>参与者</span>
              <el-tag size="small" type="info" style="margin-left: 8px;">
                {{ workflowInfo.participants?.length || 0 }} 个参与者
              </el-tag>
            </div>
          </template>

          <div class="participants-section">
            <div class="participants-grid">
              <div v-for="(participant, index) in workflowInfo.participants" :key="index" class="participant-card">
                <div class="participant-header">
                  <div class="participant-title">参与者 {{ index + 1 }}</div>
                  <el-tag size="small" type="info">{{ participant.source_path }}</el-tag>
                </div>
                <div class="participant-content">
                  <JsonViewer
                    :data="participant.data"
                    :title="`参与者信息`"
                    :collapsible="true"
                    :show-controls="false"
                    max-height="150px"
                    theme="light" />
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>

        <!-- 表单字段 -->
        <el-collapse-item name="form-fields" v-if="hasFormFields">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">📝</span>
              <span>表单字段</span>
              <el-tag size="small" type="success" style="margin-left: 8px;">
                {{ workflowInfo.form_fields?.length || 0 }} 个字段
              </el-tag>
            </div>
          </template>

          <div class="form-fields-section">
            <DataTable
              :data="workflowInfo.form_fields"
              :columns="formFieldColumns"
              :show-index="true"
              :show-pagination="false"
              size="small">
              
              <template #required="{ row }">
                <el-tag :type="row.required ? 'danger' : 'success'" size="small">
                  {{ row.required ? '必填' : '选填' }}
                </el-tag>
              </template>

              <template #type="{ row }">
                <el-tag :type="getFieldTypeColor(row.type)" size="small">
                  {{ getFieldTypeText(row.type) }}
                </el-tag>
              </template>
            </DataTable>
          </div>
        </el-collapse-item>

        <!-- 审批设置 -->
        <el-collapse-item name="approval-settings" v-if="hasApprovalSettings">
          <template #title>
            <div class="collapse-title">
              <span class="collapse-icon">✅</span>
              <span>审批设置</span>
              <el-tag size="small" type="warning" style="margin-left: 8px;">
                {{ Object.keys(workflowInfo.approval_settings || {}).length }} 项设置
              </el-tag>
            </div>
          </template>

          <div class="approval-settings-section">
            <div class="approval-grid">
              <div v-for="(value, key) in workflowInfo.approval_settings" :key="key" class="approval-item">
                <div class="approval-label">{{ formatApprovalKey(key) }}</div>
                <div class="approval-value">
                  <el-tag :type="getApprovalValueType(key, value)" size="small">
                    {{ formatApprovalValue(value) }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script>
import JsonViewer from './JsonViewer.vue'
import DataTable from './DataTable.vue'
import { ArrowRight } from '@element-plus/icons-vue'

export default {
  name: 'WorkflowArchitecture',
  components: {
    JsonViewer,
    DataTable,
    ArrowRight
  },
  props: {
    workflowInfo: {
      type: Object,
      default: () => ({})
    },
    defaultActiveItems: {
      type: Array,
      default: () => ['architecture-summary', 'template-details', 'roles', 'resources']
    }
  },
  data() {
    return {
      activeItems: [...this.defaultActiveItems]
    }
  },
  computed: {
    hasAnyWorkflow() {
      return this.hasRolesAndPermissions || this.hasStatuses || this.hasWorkflowRules || 
             this.hasParticipants || this.hasFormFields || this.hasApprovalSettings ||
             this.hasGroupPermissions || this.hasUserPermissions || this.hasTemplateMetadata ||
             this.hasResourceLinks || this.hasArchitectureSummary
    },

    hasRolesAndPermissions() {
      return this.workflowInfo.roles_and_permissions && 
             Object.keys(this.workflowInfo.roles_and_permissions).length > 0
    },

    hasStatuses() {
      return this.workflowInfo.statuses && this.workflowInfo.statuses.length > 0
    },

    hasWorkflowRules() {
      return this.workflowInfo.workflow_rules && 
             Object.keys(this.workflowInfo.workflow_rules).length > 0
    },

    hasParticipants() {
      return this.workflowInfo.participants && this.workflowInfo.participants.length > 0
    },

    hasFormFields() {
      return this.workflowInfo.form_fields && this.workflowInfo.form_fields.length > 0
    },

    hasApprovalSettings() {
      return this.workflowInfo.approval_settings && 
             Object.keys(this.workflowInfo.approval_settings).length > 0
    },

    // New computed properties for actual template data structure
    hasTemplateMetadata() {
      return this.workflowInfo && (
        this.workflowInfo.templateType || 
        this.workflowInfo.createdBy || 
        this.workflowInfo.projectId ||
        this.workflowInfo.isPdf ||
        this.workflowInfo.pdfUrl ||
        this.workflowInfo.status
      )
    },

    hasResourceLinks() {
      return this.workflowInfo && (
        this.workflowInfo.forms?.url ||
        this.workflowInfo.pdfUrl
      )
    },

    hasGroupPermissions() {
      return this.workflowInfo?.groupPermissions && this.workflowInfo.groupPermissions.length > 0
    },

    hasUserPermissions() {
      return this.workflowInfo?.userPermissions && this.workflowInfo.userPermissions.length > 0
    },

    groupPermissions() {
      return this.workflowInfo?.groupPermissions || []
    },

    userPermissions() {
      return this.workflowInfo?.userPermissions || []
    },

    // New computed properties for template-specific workflow
    hasArchitectureSummary() {
      return this.workflowInfo?.architecture_summary || 
             (this.workflowInfo?.templatesData && this.workflowInfo.templatesData.architecture_summary)
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
          width: 120,
          slot: 'type'
        },
        {
          prop: 'required',
          label: '是否必填',
          width: 100,
          slot: 'required'
        },
        {
          prop: 'label',
          label: '显示标签',
          minWidth: 150
        }
      ]
    }
  },
  methods: {
    getTotalComponents() {
      let count = 0
      if (this.hasRolesAndPermissions) count++
      if (this.hasStatuses) count++
      if (this.hasWorkflowRules) count++
      if (this.hasParticipants) count++
      if (this.hasFormFields) count++
      if (this.hasApprovalSettings) count++
      return count
    },

    getTopLevelKeys() {
      return this.workflowInfo.template_structure?.top_level_keys || []
    },

    getKeyType(key) {
      const keyTypes = {
        'formDefinition': 'primary',
        'workflow': 'success',
        'permissions': 'warning',
        'settings': 'info',
        'metadata': 'default'
      }
      return keyTypes[key] || 'default'
    },

    getPermissionType(permission) {
      // Handle non-string permission values
      const permissionStr = typeof permission === 'string' ? permission : 
                           (permission && typeof permission === 'object' ? 
                            (permission.name || permission.type || permission.toString()) : 
                            String(permission || ''))
      
      if (!permissionStr) return 'default'
      
      const lowerPerm = permissionStr.toLowerCase()
      if (lowerPerm.includes('read') || lowerPerm.includes('view')) return 'info'
      if (lowerPerm.includes('write') || lowerPerm.includes('edit')) return 'warning'
      if (lowerPerm.includes('delete') || lowerPerm.includes('remove')) return 'danger'
      if (lowerPerm.includes('admin') || lowerPerm.includes('manage')) return 'success'
      return 'default'
    },

    formatPermission(permission) {
      // Handle non-string permission values
      const permissionStr = typeof permission === 'string' ? permission : 
                           (permission && typeof permission === 'object' ? 
                            (permission.name || permission.type || permission.toString()) : 
                            String(permission || ''))
      
      if (!permissionStr) return 'Unknown'
      
      return permissionStr.replace(/_/g, ' ').replace(/([A-Z])/g, ' $1').trim()
    },

    getStatusClass(status) {
      const statusClasses = {
        'draft': 'status-draft',
        'pending': 'status-pending',
        'approved': 'status-approved',
        'rejected': 'status-rejected',
        'completed': 'status-completed'
      }
      return statusClasses[status.toLowerCase()] || 'status-default'
    },

    getStatusTagType(status) {
      const statusTypes = {
        'draft': 'info',
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'completed': 'success',
        'active': 'primary'
      }
      return statusTypes[status.toLowerCase()] || 'default'
    },

    getStatusDescription(status) {
      const descriptions = {
        'draft': '草稿',
        'pending': '待处理',
        'approved': '已批准',
        'rejected': '已拒绝',
        'completed': '已完成',
        'active': '活跃',
        'inactive': '非活跃'
      }
      return descriptions[status.toLowerCase()] || status
    },

    formatRuleName(key) {
      return key.replace(/_/g, ' ').replace(/([A-Z])/g, ' $1')
        .split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    },

    getRuleType(key) {
      if (key.includes('transition')) return 'primary'
      if (key.includes('validation')) return 'warning'
      if (key.includes('condition')) return 'info'
      if (key.includes('action')) return 'success'
      return 'default'
    },

    getRuleCategory(key) {
      if (key.includes('transition')) return '流转'
      if (key.includes('validation')) return '验证'
      if (key.includes('condition')) return '条件'
      if (key.includes('action')) return '动作'
      return '规则'
    },

    getFieldTypeColor(type) {
      const typeColors = {
        'text': 'primary',
        'number': 'success',
        'date': 'warning',
        'boolean': 'info',
        'select': 'danger',
        'multiselect': 'danger',
        'textarea': 'primary'
      }
      return typeColors[type?.toLowerCase()] || 'default'
    },

    getFieldTypeText(type) {
      const typeTexts = {
        'text': '文本',
        'number': '数字',
        'date': '日期',
        'boolean': '布尔',
        'select': '选择',
        'multiselect': '多选',
        'textarea': '文本域'
      }
      return typeTexts[type?.toLowerCase()] || type
    },

    formatApprovalKey(key) {
      const keyNames = {
        'approval': '审批',
        'review': '审核',
        'signature': '签名',
        'status': '状态',
        'workflow': '工作流',
        'assignee': '指派人',
        'reviewer': '审核人'
      }
      return keyNames[key] || key
    },

    getApprovalValueType(key, value) {
      if (key === 'status') {
        return this.getStatusTagType(value)
      }
      if (typeof value === 'boolean') {
        return value ? 'success' : 'info'
      }
      return 'default'
    },

    formatApprovalValue(value) {
      if (typeof value === 'boolean') {
        return value ? '启用' : '禁用'
      }
      if (typeof value === 'object') {
        return JSON.stringify(value)
      }
      return String(value)
    },

    // Template-specific methods
    getArchitectureSummary() {
      return this.workflowInfo?.architecture_summary || 
             this.workflowInfo?.templatesData?.architecture_summary || {}
    },

    getTemplateTypes() {
      const summary = this.getArchitectureSummary()
      return summary.template_types || []
    },

    getTemplateTypeColor(type) {
      if (!type) return 'default'
      if (type.includes('time_sheet')) return 'primary'
      if (type.includes('daily_report')) return 'success'
      if (type.includes('safety')) return 'warning'
      return 'info'
    },

    formatTemplateType(type) {
      if (!type) return 'Unknown'
      return type.replace('pg.template_type.', '').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },

    getTemplateName() {
      return this.workflowInfo?.template_name || 
             this.workflowInfo?.name || 
             this.workflowInfo?.template_metadata?.template_name || 
             'Unknown Template'
    },

    getTemplateType() {
      return this.workflowInfo?.templateType || 
             this.workflowInfo?.template_metadata?.template_type || 
             ''
    },

    getTemplateCreator() {
      return this.workflowInfo?.createdBy || 
             this.workflowInfo?.template_metadata?.created_by || 
             'Unknown'
    },

    getTemplateUpdatedAt() {
      return this.workflowInfo?.updatedAt || 
             this.workflowInfo?.template_metadata?.updated_at || 
             null
    },

    isPdfSupported() {
      return this.workflowInfo?.isPdf || 
             this.workflowInfo?.template_metadata?.is_pdf || 
             false
    },

    getFormsUrl() {
      return this.workflowInfo?.forms?.url || 
             this.workflowInfo?.template_metadata?.forms_url || 
             null
    },

    getRolesAndPermissions() {
      return this.workflowInfo?.roles_and_permissions || {}
    },

    getRolesCount() {
      const roles = this.getRolesAndPermissions()
      return Object.keys(roles).length
    },

    // New methods for enhanced functionality
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      try {
        return new Date(dateString).toLocaleString('zh-CN')
      } catch {
        return dateString
      }
    },

    async copyToClipboard(text) {
      try {
        await navigator.clipboard.writeText(text)
        this.$message.success('链接已复制到剪贴板')
      } catch (error) {
        console.error('复制失败:', error)
        // Fallback for older browsers
        const textArea = document.createElement('textarea')
        textArea.value = text
        document.body.appendChild(textArea)
        textArea.select()
        try {
          document.execCommand('copy')
          this.$message.success('链接已复制到剪贴板')
        } catch (fallbackError) {
          this.$message.error('复制失败，请手动复制')
        }
        document.body.removeChild(textArea)
      }
    },

    openPdfUrl(url) {
      if (url) {
        window.open(url, '_blank')
      } else {
        this.$message.error('PDF链接无效')
      }
    }
  }
}
</script>

<style scoped>
.workflow-architecture {
  width: 100%;
}

.architecture-card {
  border: 1px solid var(--color-border-light);
}

.architecture-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.architecture-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.architecture-stats {
  display: flex;
  gap: 8px;
}

.no-workflow {
  text-align: center;
  padding: 40px 20px;
}

.workflow-collapse {
  border: none;
}

.collapse-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.collapse-icon {
  font-size: 16px;
}

/* 结构概览 */
.structure-overview {
  padding: 16px 0;
}

.structure-grid {
  display: grid;
  gap: 16px;
}

.structure-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.structure-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.structure-value {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.component-indicators {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
}

/* 角色和权限 */
.roles-section {
  padding: 16px 0;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.role-card {
  padding: 16px;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  background: var(--color-bg-secondary);
}

.role-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.role-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 状态流程 */
.statuses-section {
  padding: 16px 0;
}

.statuses-flow {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;
}

.status-node {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  border-radius: 8px;
  background: var(--color-bg-secondary);
  border: 2px solid var(--color-border-light);
  min-width: 120px;
}

.status-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.status-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.status-arrow {
  color: var(--color-text-secondary);
  font-size: 18px;
}

/* 工作流规则 */
.workflow-rules-section {
  padding: 16px 0;
}

.rules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
}

.rule-card {
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  overflow: hidden;
}

.rule-header {
  padding: 12px 16px;
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rule-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.rule-content {
  padding: 16px;
}

/* 参与者 */
.participants-section {
  padding: 16px 0;
}

.participants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.participant-card {
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  overflow: hidden;
}

.participant-header {
  padding: 12px 16px;
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.participant-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.participant-content {
  padding: 16px;
}

/* 表单字段 */
.form-fields-section {
  padding: 16px 0;
}

/* 审批设置 */
.approval-settings-section {
  padding: 16px 0;
}

.approval-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.approval-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  border: 1px solid var(--color-border-light);
  border-radius: 6px;
  background: var(--color-bg-secondary);
}

.approval-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
}

.approval-value {
  display: flex;
  align-items: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .architecture-header {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }

  .roles-grid,
  .rules-grid,
  .participants-grid {
    grid-template-columns: 1fr;
  }

  .statuses-flow {
    flex-direction: column;
  }

  .status-node {
    flex-direction: column;
  }

  .status-arrow {
    transform: rotate(90deg);
  }

  .component-indicators {
    grid-template-columns: 1fr;
  }
}

/* 新增样式 - 架构概览 */
.architecture-summary-section {
  padding: 16px 0;
}

.summary-stats {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 8px;
  border: 1px solid var(--el-border-color-light);
  text-align: center;
}

.stat-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 8px;
}

.template-types {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background: var(--el-bg-color-page);
  border-radius: 8px;
  border: 1px solid var(--el-border-color-light);
}

.types-label {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.types-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 模板详情样式 */
.template-details-section {
  padding: 16px 0;
}

/* 角色信息增强样式 */
.role-info {
  flex: 1;
}

.role-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.role-key {
  margin-top: 8px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.key-label {
  font-weight: 600;
  margin-right: 4px;
}

.role-key code {
  background: var(--el-fill-color-light);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
}

.role-stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-end;
}

/* 新增样式 - 模板元数据 */
.metadata-section {
  padding: 16px 0;
}

/* 组权限样式 */
.group-permissions-section {
  padding: 16px 0;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
}

.permission-group-card {
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 16px;
  background: var(--el-bg-color-page);
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.group-name h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.group-permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 用户权限样式 */
.user-permissions-section {
  padding: 16px 0;
}

.permission-user-card {
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 16px;
  background: var(--el-bg-color-page);
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.user-name h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.user-permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 资源链接样式 */
.resources-section {
  padding: 16px 0;
}

.resource-links {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.resource-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.resource-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.resource-icon {
  font-size: 16px;
}

.resource-value {
  width: 100%;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .permissions-grid {
    grid-template-columns: 1fr;
  }
  
  .group-header,
  .user-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .resource-item {
    gap: 12px;
  }
}
</style>

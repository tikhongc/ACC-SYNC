<template>
  <div class="review-detail">
    <div class="review-header">
      <h3>{{ review.name }}</h3>
      <div class="review-meta">
        <StatusTag 
          :status="getStatusForTag(review.status)" 
          :text="review.status"
          size="small"
          :show-icon="false" />
        <StatusTag v-if="review.archived" status="archived" text="已归档" size="small" :show-icon="false" />
        <span class="review-id">序列ID: #{{ review.sequenceId }}</span>
      </div>
    </div>
    
    <!-- 基本信息 -->
    <div class="review-info">
      <div class="info-grid">
        <div class="info-item">
          <strong>评审ID (id):</strong>
          <code>{{ review.id }}</code>
        </div>
        <div class="info-item">
          <strong>序列ID (sequenceId):</strong>
          <code>{{ review.sequenceId }}</code>
        </div>
        <div class="info-item">
          <strong>工作流ID:</strong>
          <code>{{ review.workflowId || 'N/A' }}</code>
        </div>
        <div class="info-item">
          <strong>当前步骤ID:</strong>
          <code>{{ review.currentStepId || 'N/A' }}</code>
        </div>
        <div class="info-item">
          <strong>步骤到期时间:</strong>
          <span>{{ formatDate(review.currentStepDueDate) }}</span>
        </div>
      </div>
    </div>

    <!-- 参与者信息 -->
    <div class="participants-section">
      <h4>👥 参与者信息</h4>
      
      <!-- 创建者 -->
      <div class="participant-group">
        <div class="participant-label">📝 创建者</div>
        <div class="participant-card" v-if="review.createdBy">
          <div class="participant-info">
            <div class="participant-name">{{ review.createdBy.name }}</div>
            <div class="participant-id">{{ review.createdBy.autodeskId }}</div>
          </div>
        </div>
        <div v-else class="no-data">暂无数据</div>
      </div>
      
      <!-- 归档者 -->
      <div v-if="review.archived && review.archivedBy" class="participant-group">
        <div class="participant-label">📦 归档者</div>
        <div class="participant-card">
          <div class="participant-info">
            <div class="participant-name">{{ review.archivedBy.name }}</div>
            <div class="participant-id">{{ review.archivedBy.autodeskId }}</div>
          </div>
        </div>
      </div>
      
      <!-- 下一步操作者 -->
      <div v-if="review.nextActionBy" class="participant-group">
        <div class="participant-label">⏭️ 下一步操作者</div>
        
        <!-- 已认领用户 -->
        <div v-if="review.nextActionBy.claimedBy && review.nextActionBy.claimedBy.length > 0" class="claimed-section">
          <div class="subsection-title">✅ 已认领用户</div>
          <div class="participants-list">
            <div 
              v-for="user in review.nextActionBy.claimedBy" 
              :key="user.autodeskId"
              class="participant-card claimed">
              <div class="participant-info">
                <div class="participant-name">{{ user.name }}</div>
                <div class="participant-id">{{ user.autodeskId }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 候选者 -->
        <div v-if="review.nextActionBy.candidates" class="candidates-section">
          <div class="subsection-title">🎯 候选者</div>
          
          <!-- 候选用户 -->
          <div v-if="review.nextActionBy.candidates.users && review.nextActionBy.candidates.users.length > 0" class="candidate-group">
            <div class="candidate-type">👤 用户 ({{ review.nextActionBy.candidates.users.length }})</div>
            <div class="participants-list">
              <div 
                v-for="user in review.nextActionBy.candidates.users" 
                :key="user.autodeskId"
                class="participant-card user">
                <div class="participant-info">
                  <div class="participant-name">{{ user.name }}</div>
                  <div class="participant-id">{{ user.autodeskId }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 候选角色 -->
          <div v-if="review.nextActionBy.candidates.roles && review.nextActionBy.candidates.roles.length > 0" class="candidate-group">
            <div class="candidate-type">🏷️ 角色 ({{ review.nextActionBy.candidates.roles.length }})</div>
            <div class="participants-list">
              <div 
                v-for="role in review.nextActionBy.candidates.roles" 
                :key="role.autodeskId"
                class="participant-card role">
                <div class="participant-info">
                  <div class="participant-name">{{ role.name }}</div>
                  <div class="participant-id">{{ role.autodeskId }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 候选公司 -->
          <div v-if="review.nextActionBy.candidates.companies && review.nextActionBy.candidates.companies.length > 0" class="candidate-group">
            <div class="candidate-type">🏢 公司 ({{ review.nextActionBy.candidates.companies.length }})</div>
            <div class="participants-list">
              <div 
                v-for="company in review.nextActionBy.candidates.companies" 
                :key="company.autodeskId"
                class="participant-card company">
                <div class="participant-info">
                  <div class="participant-name">{{ company.name }}</div>
                  <div class="participant-id">{{ company.autodeskId }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 时间线信息 -->
    <div class="timeline-section">
      <h4>📅 时间线</h4>
      <div class="timeline-grid">
        <div class="timeline-item">
          <div class="timeline-label">创建时间</div>
          <div class="timeline-value">{{ formatDate(review.createdAt) }}</div>
        </div>
        <div class="timeline-item">
          <div class="timeline-label">更新时间</div>
          <div class="timeline-value">{{ formatDate(review.updatedAt) }}</div>
        </div>
        <div v-if="review.finishedAt" class="timeline-item">
          <div class="timeline-label">完成时间</div>
          <div class="timeline-value">{{ formatDate(review.finishedAt) }}</div>
        </div>
        <div v-if="review.archivedAt" class="timeline-item">
          <div class="timeline-label">归档时间</div>
          <div class="timeline-value">{{ formatDate(review.archivedAt) }}</div>
        </div>
      </div>
    </div>

    <!-- 关联工作流 -->
    <div v-if="review.workflowId" class="workflow-section">
      <h4>🔄 关联工作流</h4>
      
      <!-- 加载状态 -->
      <div v-if="workflowLoading" class="workflow-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在加载工作流数据...</span>
      </div>
      
      <!-- 错误状态 -->
      <div v-else-if="workflowError" class="workflow-error">
        <el-alert
          :title="workflowError"
          type="error"
          :closable="false"
          show-icon />
        <el-button 
          type="primary" 
          size="small" 
          @click="loadWorkflow"
          style="margin-top: 8px;">
          重试加载
        </el-button>
      </div>
      
      <!-- 工作流可视化 -->
      <div v-else-if="workflowData" class="workflow-visualization">
        <WorkflowDiagram :workflow="workflowData.raw_data" />
        
        <!-- 工作流统计信息 -->
        <div class="workflow-stats" style="margin-top: 16px;">
          <el-row :gutter="16">
            <el-col :span="6">
              <el-statistic title="工作流步骤" :value="workflowData.workflow?.steps_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="审批选项" :value="workflowData.workflow?.approval_options_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="文件复制" :value="workflowData.workflow?.has_copy_files ? '启用' : '禁用'" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="附加属性" :value="workflowData.workflow?.has_attached_attributes ? '有' : '无'" />
            </el-col>
          </el-row>
        </div>
      </div>
      
      <!-- 手动加载按钮 -->
      <div v-else class="workflow-load-button">
        <el-button type="primary" @click="loadWorkflow">
          <el-icon><View /></el-icon>
          加载关联工作流
        </el-button>
      </div>
    </div>
    
    <!-- 无关联工作流提示 -->
    <div v-else class="no-workflow">
      <el-alert
        title="此评审未关联工作流"
        type="info"
        :closable="false"
        show-icon />
    </div>

    <!-- 评审文件版本 -->
    <div class="versions-section">
      <h4>📁 评审文件版本</h4>
      
      <!-- 加载状态 -->
      <div v-if="versionsLoading" class="versions-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在加载文件版本数据...</span>
      </div>
      
      <!-- 错误状态 -->
      <div v-else-if="versionsError" class="versions-error">
        <el-alert
          :title="versionsError"
          type="error"
          :closable="false"
          show-icon />
        <el-button 
          type="primary" 
          size="small" 
          @click="loadVersions"
          style="margin-top: 8px;">
          重试加载
        </el-button>
      </div>
      
      <!-- 文件版本列表 -->
      <div v-else-if="versionsData && versionsData.versions?.length > 0" class="versions-content">
        <!-- 文件版本统计 -->
        <div class="versions-stats">
          <el-row :gutter="16">
            <el-col :span="6">
              <el-statistic title="文件总数" :value="versionsData.stats?.total_versions || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="PDF文件" :value="versionsData.stats?.pdf_files_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="已复制版本" :value="versionsData.stats?.copied_versions_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="带属性文件" :value="versionsData.stats?.with_custom_attributes || 0" />
            </el-col>
          </el-row>
          
          <!-- 数据质量信息 -->
          <el-row v-if="versionsData.stats?.duplicate_versions_count > 0" :gutter="16" style="margin-top: 16px;">
            <el-col :span="6">
              <el-statistic title="原始文件" :value="versionsData.stats?.original_versions_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="重复文件" :value="versionsData.stats?.duplicate_versions_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="去重后" :value="versionsData.stats?.unique_versions_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-tag type="warning" size="small">
                已自动去重
              </el-tag>
            </el-col>
          </el-row>
        </div>
        
        <!-- 文件列表 -->
        <div class="versions-list">
          <div 
            v-for="version in versionsData.versions" 
            :key="version.urn"
            class="version-card">
            <div class="version-header">
              <div class="version-name">
                <el-icon><Document /></el-icon>
                <span>{{ version.display_name || version.name }}</span>
                <el-tag v-if="version.file_extension" size="small" type="info">
                  {{ version.file_extension }}
                </el-tag>
                <el-tag v-if="version.version_number" size="small" type="warning">
                  v{{ version.version_number }}
                </el-tag>
                <el-tag v-if="version.file_size" size="small" type="success">
                  {{ formatFileSize(version.file_size) }}
                </el-tag>
              </div>
              <div class="version-status">
                <el-tag 
                  :type="version.approve_status.status_type" 
                  size="small">
                  {{ version.approve_status.label }}
                </el-tag>
              </div>
            </div>
            
            <div class="version-details">
              <div class="version-info">
                <div class="info-item">
                  <strong>文件URN:</strong>
                  <code class="urn-text">{{ version.urn }}</code>
                </div>
                <div v-if="version.has_copied_version" class="info-item">
                  <strong>复制版本URN:</strong>
                  <code class="urn-text">{{ version.copied_file_version_urn }}</code>
                </div>
                <div v-if="version.review_content.name !== version.name" class="info-item">
                  <strong>评审内容名称:</strong>
                  <span>{{ version.review_content.name }}</span>
                </div>
                <div v-if="version.unique_identifier" class="info-item">
                  <strong>唯一标识:</strong>
                  <code class="identifier-text">{{ version.unique_identifier }}</code>
                </div>
                <div v-if="version.created_date" class="info-item">
                  <strong>创建时间:</strong>
                  <span>{{ version.created_date }}</span>
                </div>
                <div v-if="version.modified_date" class="info-item">
                  <strong>修改时间:</strong>
                  <span>{{ version.modified_date }}</span>
                </div>
              </div>
              
              <!-- 文件版本操作按钮 -->
              <div class="version-actions">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="showVersionDetail(version)"
                  :icon="Search">
                  查看审批历史
                </el-button>
              </div>
            
              <!-- 自定义属性 -->
              <div v-if="version.review_content.custom_attributes_count > 0" class="custom-attributes">
                <div class="attributes-title">🏷️ 自定义属性</div>
                <div class="attributes-list">
                  <div 
                    v-for="attr in version.review_content.custom_attributes" 
                    :key="attr.id"
                    class="attribute-item">
                    <div class="attribute-name">{{ attr.name }}</div>
                    <div class="attribute-value">{{ attr.value }}</div>
                    <el-tag size="small" type="info">{{ attr.type }}</el-tag>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 无文件版本或手动加载 -->
      <div v-else class="versions-load-button">
        <el-button type="primary" @click="loadVersions">
          <el-icon><FolderOpened /></el-icon>
          加载文件版本
        </el-button>
      </div>
    </div>

    <!-- 文件版本详情弹窗 -->
    <el-dialog
      v-model="showVersionDialog"
      :title="`文件版本详情 - ${selectedVersion?.name || ''}`"
      width="90%"
      :before-close="handleCloseVersionDialog"
      draggable
      destroy-on-close
      class="version-dialog">
      <div v-if="selectedVersion" class="dialog-content">
        <FileVersionDetail :file-version="selectedVersion" />
      </div>
    </el-dialog>

    <!-- 原始数据 -->
    <div class="raw-data-section">
      <el-collapse>
        <el-collapse-item title="🔍 查看评审原始数据" name="review-raw-data">
          <JsonViewer 
            :data="review"
            title="评审原始数据"
            :max-height="400" />
        </el-collapse-item>
        <el-collapse-item 
          v-if="workflowData" 
          title="🔄 查看工作流原始数据" 
          name="workflow-raw-data">
          <JsonViewer 
            :data="workflowData"
            title="工作流原始数据"
            :max-height="400" />
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Loading, View, Document, FolderOpened, Search } from '@element-plus/icons-vue'
import JsonViewer from './JsonViewer.vue'
import WorkflowDiagram from './WorkflowDiagram.vue'
import FileVersionDetail from './FileVersionDetail.vue'
import StatusTag from './StatusTag.vue'

export default {
  name: 'ReviewDetail',
  components: {
    JsonViewer,
    WorkflowDiagram,
    FileVersionDetail,
    StatusTag,
    Loading,
    View,
    Document,
    FolderOpened,
    Search
  },
  props: {
    review: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    // 响应式数据
    const workflowData = ref(null)
    const workflowLoading = ref(false)
    const workflowError = ref('')
    
    const versionsData = ref(null)
    const versionsLoading = ref(false)
    const versionsError = ref('')
    
    const showVersionDialog = ref(false)
    const selectedVersion = ref(null)
    
    // Force reactive display of review data
    const reviewDisplay = computed(() => ({
      id: props.review?.id,
      name: props.review?.name,
      sequenceId: props.review?.sequenceId,
      timestamp: Date.now(),
      componentKey: `${props.review?.id}-${Math.random()}`
    }))
    
    // 加载工作流数据
    const loadWorkflow = async () => {
      if (!props.review?.id || !props.review?.workflowId) {
        workflowError.value = '缺少评审ID或工作流ID'
        return
      }
      
      workflowLoading.value = true
      workflowError.value = ''
      
      try {
        const response = await axios.get(`/api/reviews/jarvis/${props.review.id}/workflow`, {
          timeout: 30000
        })
        
        if (response.data.success) {
          workflowData.value = response.data
          ElMessage.success('工作流数据加载成功')
        } else {
          throw new Error(response.data.error || '加载工作流失败')
        }
      } catch (err) {
        console.error('加载工作流失败:', err)
        workflowError.value = err.response?.data?.error || err.message || '加载工作流失败'
        ElMessage.error(workflowError.value)
      } finally {
        workflowLoading.value = false
      }
    }
    
    // 加载文件版本数据
    const loadVersions = async () => {
      if (!props.review?.id) {
        versionsError.value = '缺少评审ID'
        return
      }
      
      versionsLoading.value = true
      versionsError.value = ''
      
      try {
        const response = await axios.get(`/api/reviews/jarvis/${props.review.id}/versions`, {
          timeout: 30000,
          params: {
            _t: Date.now() // 防止缓存
          }
        })
        
        if (response.data.success) {
          versionsData.value = response.data
          
          // 输出调试信息
          console.log('文件版本API响应统计:', response.data.stats)
          console.log('文件版本数量:', response.data.versions?.length)
          
          // 检查前端是否还有重复的文件版本
          const versionUrns = response.data.versions?.map(v => v.urn) || []
          const uniqueUrns = new Set(versionUrns)
          console.log('文件版本检查 - 总URN数:', versionUrns.length)
          console.log('文件版本检查 - 唯一URN数:', uniqueUrns.size)
          if (versionUrns.length !== uniqueUrns.size) {
            console.warn('⚠️ 前端仍然检测到重复文件版本!')
          } else {
            console.log('✅ 文件版本数据无重复')
          }
          
          if (response.data.stats?.duplicate_versions_count > 0) {
            ElMessage.success(`文件版本数据加载成功，已去重 ${response.data.stats.duplicate_versions_count} 个重复文件`)
          } else {
            ElMessage.success('文件版本数据加载成功')
          }
        } else {
          throw new Error(response.data.error || '加载文件版本失败')
        }
      } catch (err) {
        console.error('加载文件版本失败:', err)
        versionsError.value = err.response?.data?.error || err.message || '加载文件版本失败'
        ElMessage.error(versionsError.value)
      } finally {
        versionsLoading.value = false
      }
    }
    
    // 显示文件版本详情
    const showVersionDetail = (version) => {
      selectedVersion.value = version
      showVersionDialog.value = true
    }
    
    // 关闭文件版本详情对话框
    const handleCloseVersionDialog = () => {
      showVersionDialog.value = false
      selectedVersion.value = null
    }
    
    // 工具方法
    const getStatusType = (status) => {
      const statusMap = {
        'OPEN': 'success',
        'CLOSED': 'info',
        'VOID': 'warning',
        'FAILED': 'danger'
      }
      return statusMap[status] || 'info'
    }

    // StatusTag适配方法
    const getStatusForTag = (status) => {
      const statusMap = {
        'OPEN': 'open',
        'CLOSED': 'closed',
        'VOID': 'void',
        'FAILED': 'failed'
      }
      return statusMap[status] || status?.toLowerCase() || 'unknown'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString('zh-CN')
    }
    
    const formatFileSize = (bytes) => {
      if (!bytes || bytes === 0) return ''
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(1024))
      return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
    }
    
    // 监听review变化，重置数据 - 使用sequenceId作为主要标识
    watch(() => props.review?.sequenceId || props.review?.id, (newId, oldId) => {
      console.log(`Review changed from ${oldId} to ${newId}`)
      workflowData.value = null
      workflowError.value = ''
      versionsData.value = null
      versionsError.value = ''
      showVersionDialog.value = false
      selectedVersion.value = null
    }, { immediate: true })
    
    // 如果有工作流ID，自动加载工作流数据
    onMounted(() => {
      console.log('ReviewDetail mounted with review:', {
        id: props.review?.id,
        name: props.review?.name,
        sequenceId: props.review?.sequenceId,
        fullReviewObject: props.review
      })
      if (props.review?.workflowId) {
        loadWorkflow()
      }
    })
    
    return {
      workflowData,
      workflowLoading,
      workflowError,
      loadWorkflow,
      versionsData,
      versionsLoading,
      versionsError,
      loadVersions,
      showVersionDialog,
      selectedVersion,
      showVersionDetail,
      handleCloseVersionDialog,
      reviewDisplay,
      getStatusType,
      getStatusForTag,
      formatDate,
      formatFileSize
    }
  }
}
</script>

<style scoped>
.review-detail {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f2f5;
}

.review-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 20px;
  font-weight: 600;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.review-id {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  color: #6b7280;
  background: #f9fafb;
  padding: 4px 8px;
  border-radius: 4px;
}

.review-info {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
  border-left: 4px solid #3b82f6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: white;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

.info-item strong {
  min-width: 120px;
  color: #374151;
  font-size: 13px;
}

.info-item code {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 11px;
  color: #dc2626;
}

.participants-section {
  margin-bottom: 24px;
}

.participants-section h4 {
  color: #1f2937;
  margin-bottom: 16px;
  font-size: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.participant-group {
  margin-bottom: 20px;
}

.participant-label {
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
  font-size: 14px;
}

.subsection-title {
  font-weight: 500;
  color: #6b7280;
  margin: 12px 0 8px 0;
  font-size: 13px;
}

.candidate-type {
  font-weight: 500;
  color: #4b5563;
  margin: 8px 0 6px 0;
  font-size: 12px;
}

.participants-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.participant-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.2s ease;
}

.participant-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.participant-card.claimed {
  border-color: #10b981;
  background: #f0fdf4;
}

.participant-card.user {
  border-color: #3b82f6;
  background: #eff6ff;
}

.participant-card.role {
  border-color: #10b981;
  background: #f0fdf4;
}

.participant-card.company {
  border-color: #f59e0b;
  background: #fffbeb;
}

.participant-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.participant-name {
  font-weight: 500;
  color: #1f2937;
  font-size: 14px;
}

.participant-id {
  font-size: 11px;
  color: #6b7280;
  font-family: 'Consolas', 'Monaco', monospace;
}

.no-data {
  color: #9ca3af;
  font-style: italic;
  padding: 12px;
  background: #f9fafb;
  border-radius: 4px;
  border: 1px dashed #d1d5db;
}

.timeline-section {
  margin-bottom: 24px;
}

.timeline-section h4 {
  color: #1f2937;
  margin-bottom: 16px;
  font-size: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.timeline-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.timeline-item {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.timeline-label {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
  font-weight: 500;
}

.timeline-value {
  font-size: 13px;
  color: #1f2937;
  font-family: 'Consolas', 'Monaco', monospace;
}

.workflow-section {
  margin-bottom: 24px;
}

.workflow-section h4 {
  color: #1f2937;
  margin-bottom: 16px;
  font-size: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.workflow-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  color: #6b7280;
}

.workflow-error {
  padding: 16px;
  background: #fef2f2;
  border-radius: 8px;
}

.workflow-visualization {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.workflow-stats {
  background: white;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.workflow-load-button {
  text-align: center;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  border: 2px dashed #d1d5db;
}

.no-workflow {
  margin-bottom: 24px;
}

.versions-section {
  margin-bottom: 24px;
}

.versions-section h4 {
  color: #1f2937;
  margin-bottom: 16px;
  font-size: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.versions-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  color: #6b7280;
}

.versions-error {
  padding: 16px;
  background: #fef2f2;
  border-radius: 8px;
}

.versions-content {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.versions-stats {
  background: white;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  margin-bottom: 16px;
}

.versions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.version-card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.version-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.version-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.version-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #1f2937;
}

.version-name span {
  flex: 1;
}

.version-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.version-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13px;
}

.info-item strong {
  min-width: 120px;
  color: #6b7280;
  flex-shrink: 0;
}

.urn-text {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 11px;
  color: #dc2626;
  word-break: break-all;
  flex: 1;
}

.identifier-text {
  background: #e0f2fe;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 11px;
  color: #0369a1;
  word-break: break-all;
  flex: 1;
}

.custom-attributes {
  background: #f9fafb;
  border-radius: 6px;
  padding: 12px;
  border: 1px solid #e5e7eb;
}

.attributes-title {
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
  font-size: 13px;
}

.attributes-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attribute-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: white;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

.attribute-name {
  font-weight: 500;
  color: #374151;
  min-width: 150px;
  font-size: 12px;
}

.attribute-value {
  flex: 1;
  color: #1f2937;
  font-size: 12px;
}

.versions-load-button {
  text-align: center;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  border: 2px dashed #d1d5db;
}

.version-actions {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
}

.version-dialog {
  --el-dialog-content-font-size: 14px;
}

.version-dialog .dialog-content {
  max-height: 70vh;
  overflow-y: auto;
}

.raw-data-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .review-detail {
    padding: 16px;
  }
  
  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .participants-list {
    grid-template-columns: 1fr;
  }
  
  .timeline-grid {
    grid-template-columns: 1fr;
  }
}
</style>

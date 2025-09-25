<template>
  <div class="file-version-detail">
    <!-- 文件版本基本信息 -->
    <div class="version-info-section">
      <h4>📄 文件版本信息</h4>
      <div class="version-basic-info">
        <div class="info-grid">
          <div class="info-item">
            <strong>文件名称:</strong>
            <span>{{ fileVersion.name || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <strong>文件URN:</strong>
            <code class="urn-text">{{ fileVersion.urn || 'N/A' }}</code>
          </div>
          <div class="info-item">
            <strong>文件类型:</strong>
            <el-tag v-if="fileVersion.file_extension" size="small" type="info">
              {{ fileVersion.file_extension }}
            </el-tag>
            <span v-else>N/A</span>
          </div>
          <div class="info-item">
            <strong>当前状态:</strong>
            <el-tag 
              v-if="fileVersion.approve_status"
              :type="fileVersion.approve_status.status_type" 
              size="small">
              {{ fileVersion.approve_status.label }}
            </el-tag>
            <span v-else>N/A</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 审批历史和评审记录 -->
    <div class="approval-history-section">
      <h4>📋 审批历史和评审记录</h4>
      
      <!-- 加载状态 -->
      <div v-if="historyLoading" class="history-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在加载审批历史...</span>
      </div>
      
      <!-- 错误状态 -->
      <div v-else-if="historyError" class="history-error">
        <el-alert
          :title="historyError"
          type="error"
          :closable="false"
          show-icon />
        <el-button 
          type="primary" 
          size="small" 
          @click="loadApprovalHistory"
          style="margin-top: 8px;">
          重试加载
        </el-button>
      </div>
      
      <!-- 审批历史内容 -->
      <div v-else-if="historyData && historyData.approval_history?.length > 0" class="history-content">
        <!-- 统计信息 -->
        <div class="history-stats">
          <el-row :gutter="16">
            <el-col :span="6">
              <el-statistic title="总评审次数" :value="historyData.stats?.total_approvals || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="进行中评审" :value="historyData.stats?.in_review_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="已完成评审" :value="historyData.stats?.finished_count || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="最新序号" :value="historyData.stats?.latest_sequence_id || 0" />
            </el-col>
          </el-row>
        </div>
        
        <!-- 分组显示审批历史 -->
        <div class="history-groups">
          <!-- 进行中的评审 -->
          <div v-if="historyData.in_review_approvals?.length > 0" class="history-group">
            <div class="group-header">
              <h5>🔄 进行中的评审</h5>
              <el-tag type="success" size="small">{{ historyData.in_review_approvals.length }} 项</el-tag>
            </div>
            <div class="approval-list">
              <div 
                v-for="approval in historyData.in_review_approvals" 
                :key="`${approval.review.id}-${approval.approval_status.id}`"
                class="approval-card in-review">
                <div class="approval-header">
                  <div class="review-info">
                    <el-icon><DocumentChecked /></el-icon>
                    <span class="review-sequence">评审 {{ approval.sequence_display }}</span>
                    <el-tag 
                      :type="approval.review.status_type" 
                      size="small">
                      {{ approval.review.status }}
                    </el-tag>
                  </div>
                  <div class="approval-status">
                    <el-tag 
                      :type="approval.approval_status.status_type" 
                      size="small">
                      {{ approval.approval_status.label }}
                    </el-tag>
                  </div>
                </div>
                <div class="approval-details">
                  <div class="detail-item">
                    <strong>评审ID:</strong>
                    <code class="review-id">{{ approval.review.id }}</code>
                  </div>
                  <div class="detail-item">
                    <strong>审批状态ID:</strong>
                    <code class="status-id">{{ approval.approval_status.id }}</code>
                  </div>
                  
                  <!-- 用户信息 -->
                  <div v-if="approval.has_user_info" class="user-info-section">
                    <div class="user-info-title">👤 相关人员</div>
                    <div class="user-info-list">
                      <div v-if="approval.user_info.approved_by?.name" class="user-info-item">
                        <el-icon><UserFilled /></el-icon>
                        <strong>批准人:</strong>
                        <span>{{ approval.user_info.approved_by.name }}</span>
                        <el-tag v-if="approval.user_info.approved_by.email" size="small" type="info">
                          {{ approval.user_info.approved_by.email }}
                        </el-tag>
                      </div>
                      <div v-if="approval.user_info.reviewed_by?.name" class="user-info-item">
                        <el-icon><View /></el-icon>
                        <strong>审核人:</strong>
                        <span>{{ approval.user_info.reviewed_by.name }}</span>
                        <el-tag v-if="approval.user_info.reviewed_by.email" size="small" type="info">
                          {{ approval.user_info.reviewed_by.email }}
                        </el-tag>
                      </div>
                      <div v-if="approval.user_info.created_by?.name" class="user-info-item">
                        <el-icon><Plus /></el-icon>
                        <strong>创建人:</strong>
                        <span>{{ approval.user_info.created_by.name }}</span>
                      </div>
                      <div v-if="approval.user_info.assigned_to?.name" class="user-info-item">
                        <el-icon><User /></el-icon>
                        <strong>分配给:</strong>
                        <span>{{ approval.user_info.assigned_to.name }}</span>
                      </div>
                      <div v-if="approval.user_info.current_assignee?.name" class="user-info-item">
                        <el-icon><Avatar /></el-icon>
                        <strong>当前负责人:</strong>
                        <span>{{ approval.user_info.current_assignee.name }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 时间信息 -->
                  <div v-if="approval.has_timestamps" class="timestamp-section">
                    <div class="timestamp-title">⏰ 时间记录</div>
                    <div class="timestamp-list">
                      <div v-if="approval.timestamps.approved_at" class="timestamp-item">
                        <el-icon><Check /></el-icon>
                        <strong>批准时间:</strong>
                        <span>{{ approval.timestamps.approved_at }}</span>
                      </div>
                      <div v-if="approval.timestamps.reviewed_at" class="timestamp-item">
                        <el-icon><View /></el-icon>
                        <strong>审核时间:</strong>
                        <span>{{ approval.timestamps.reviewed_at }}</span>
                      </div>
                      <div v-if="approval.timestamps.created_at" class="timestamp-item">
                        <el-icon><Plus /></el-icon>
                        <strong>创建时间:</strong>
                        <span>{{ approval.timestamps.created_at }}</span>
                      </div>
                      <div v-if="approval.timestamps.updated_at" class="timestamp-item">
                        <el-icon><Edit /></el-icon>
                        <strong>更新时间:</strong>
                        <span>{{ approval.timestamps.updated_at }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 调试信息：显示缺失的用户信息 -->
                  <div v-if="!approval.has_user_info" class="debug-info">
                    <el-alert
                      title="暂无用户信息"
                      type="info"
                      :closable="false"
                      show-icon
                      size="small">
                      <template #default>
                        API响应中未包含用户信息字段。可用字段: {{ Object.keys(approval).join(', ') }}
                      </template>
                    </el-alert>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 已完成的评审 -->
          <div v-if="historyData.finished_approvals?.length > 0" class="history-group">
            <div class="group-header">
              <h5>✅ 已完成的评审</h5>
              <el-tag type="info" size="small">{{ historyData.finished_approvals.length }} 项</el-tag>
            </div>
            <div class="approval-list">
              <div 
                v-for="approval in historyData.finished_approvals" 
                :key="`${approval.review.id}-${approval.approval_status.id}`"
                class="approval-card finished">
                <div class="approval-header">
                  <div class="review-info">
                    <el-icon><Document /></el-icon>
                    <span class="review-sequence">评审 {{ approval.sequence_display }}</span>
                    <el-tag 
                      :type="approval.review.status_type" 
                      size="small">
                      {{ approval.review.status }}
                    </el-tag>
                  </div>
                  <div class="approval-status">
                    <el-tag 
                      :type="approval.approval_status.status_type" 
                      size="small">
                      {{ approval.approval_status.label }}
                    </el-tag>
                  </div>
                </div>
                <div class="approval-details">
                  <div class="detail-item">
                    <strong>评审ID:</strong>
                    <code class="review-id">{{ approval.review.id }}</code>
                  </div>
                  <div class="detail-item">
                    <strong>审批状态ID:</strong>
                    <code class="status-id">{{ approval.approval_status.id }}</code>
                  </div>
                  
                  <!-- 用户信息 -->
                  <div v-if="approval.has_user_info" class="user-info-section">
                    <div class="user-info-title">👤 相关人员</div>
                    <div class="user-info-list">
                      <div v-if="approval.user_info.approved_by?.name" class="user-info-item">
                        <el-icon><UserFilled /></el-icon>
                        <strong>批准人:</strong>
                        <span>{{ approval.user_info.approved_by.name }}</span>
                        <el-tag v-if="approval.user_info.approved_by.email" size="small" type="info">
                          {{ approval.user_info.approved_by.email }}
                        </el-tag>
                      </div>
                      <div v-if="approval.user_info.reviewed_by?.name" class="user-info-item">
                        <el-icon><View /></el-icon>
                        <strong>审核人:</strong>
                        <span>{{ approval.user_info.reviewed_by.name }}</span>
                        <el-tag v-if="approval.user_info.reviewed_by.email" size="small" type="info">
                          {{ approval.user_info.reviewed_by.email }}
                        </el-tag>
                      </div>
                      <div v-if="approval.user_info.created_by?.name" class="user-info-item">
                        <el-icon><Plus /></el-icon>
                        <strong>创建人:</strong>
                        <span>{{ approval.user_info.created_by.name }}</span>
                      </div>
                      <div v-if="approval.user_info.assigned_to?.name" class="user-info-item">
                        <el-icon><User /></el-icon>
                        <strong>分配给:</strong>
                        <span>{{ approval.user_info.assigned_to.name }}</span>
                      </div>
                      <div v-if="approval.user_info.current_assignee?.name" class="user-info-item">
                        <el-icon><Avatar /></el-icon>
                        <strong>当前负责人:</strong>
                        <span>{{ approval.user_info.current_assignee.name }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 时间信息 -->
                  <div v-if="approval.has_timestamps" class="timestamp-section">
                    <div class="timestamp-title">⏰ 时间记录</div>
                    <div class="timestamp-list">
                      <div v-if="approval.timestamps.approved_at" class="timestamp-item">
                        <el-icon><Check /></el-icon>
                        <strong>批准时间:</strong>
                        <span>{{ approval.timestamps.approved_at }}</span>
                      </div>
                      <div v-if="approval.timestamps.reviewed_at" class="timestamp-item">
                        <el-icon><View /></el-icon>
                        <strong>审核时间:</strong>
                        <span>{{ approval.timestamps.reviewed_at }}</span>
                      </div>
                      <div v-if="approval.timestamps.created_at" class="timestamp-item">
                        <el-icon><Plus /></el-icon>
                        <strong>创建时间:</strong>
                        <span>{{ approval.timestamps.created_at }}</span>
                      </div>
                      <div v-if="approval.timestamps.updated_at" class="timestamp-item">
                        <el-icon><Edit /></el-icon>
                        <strong>更新时间:</strong>
                        <span>{{ approval.timestamps.updated_at }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 状态分布图表 -->
        <div class="status-distribution">
          <h5>📊 状态分布</h5>
          <div class="distribution-cards">
            <div class="distribution-card">
              <div class="card-title">审批状态分布</div>
              <div class="status-tags">
                <div 
                  v-for="(count, status) in historyData.stats?.approval_status_counts || {}" 
                  :key="status"
                  class="status-tag-item">
                  <el-tag size="small">{{ status }}</el-tag>
                  <span class="count">{{ count }}</span>
                </div>
              </div>
            </div>
            <div class="distribution-card">
              <div class="card-title">评审状态分布</div>
              <div class="status-tags">
                <div 
                  v-for="(count, status) in historyData.stats?.review_status_counts || {}" 
                  :key="status"
                  class="status-tag-item">
                  <el-tag size="small">{{ status }}</el-tag>
                  <span class="count">{{ count }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 无审批历史或手动加载 -->
      <div v-else class="history-load-button">
        <el-button type="primary" @click="loadApprovalHistory">
          <el-icon><Search /></el-icon>
          加载审批历史
        </el-button>
      </div>
    </div>

    <!-- 原始数据 -->
    <div class="raw-data-section">
      <el-collapse>
        <el-collapse-item title="🔍 查看文件版本原始数据" name="version-raw-data">
          <JsonViewer :data="fileVersion" />
        </el-collapse-item>
        <el-collapse-item 
          v-if="historyData" 
          title="🔍 查看审批历史原始数据" 
          name="history-raw-data">
          <JsonViewer :data="historyData.raw_data" />
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Loading, Document, DocumentChecked, Search, UserFilled, View, Plus, User, Avatar, Check, Edit } from '@element-plus/icons-vue'
import JsonViewer from './JsonViewer.vue'

export default {
  name: 'FileVersionDetail',
  components: {
    JsonViewer,
    Loading,
    Document,
    DocumentChecked,
    Search,
    UserFilled,
    View,
    Plus,
    User,
    Avatar,
    Check,
    Edit
  },
  props: {
    fileVersion: {
      type: Object,
      required: true
    },
    projectId: {
      type: String,
      default: 'jarvis'
    }
  },
  setup(props) {
    // 响应式数据
    const historyData = ref(null)
    const historyLoading = ref(false)
    const historyError = ref('')
    
    // 加载审批历史数据
    const loadApprovalHistory = async () => {
      if (!props.fileVersion?.urn) {
        historyError.value = '缺少文件版本URN'
        return
      }
      
      historyLoading.value = true
      historyError.value = ''
      
      try {
        // 使用文件版本的URN作为版本ID
        const versionId = props.fileVersion.urn
        const endpoint = props.projectId === 'jarvis' 
          ? `/api/versions/jarvis/${encodeURIComponent(versionId)}/approval-statuses`
          : `/api/versions/${props.projectId}/${encodeURIComponent(versionId)}/approval-statuses`
        
        console.log('Loading approval history for:', versionId)
        console.log('API endpoint:', endpoint)
        
        const response = await axios.get(endpoint, {
          timeout: 30000
        })
        
        if (response.data.success) {
          historyData.value = response.data
          ElMessage.success('审批历史加载成功')
        } else {
          throw new Error(response.data.error || '加载审批历史失败')
        }
      } catch (err) {
        console.error('加载审批历史失败:', err)
        historyError.value = err.response?.data?.error || err.message || '加载审批历史失败'
        ElMessage.error(historyError.value)
      } finally {
        historyLoading.value = false
      }
    }
    
    // 监听文件版本变化，重置数据
    watch(() => props.fileVersion?.urn, () => {
      historyData.value = null
      historyError.value = ''
    })
    
    return {
      historyData,
      historyLoading,
      historyError,
      loadApprovalHistory
    }
  }
}
</script>

<style scoped>
.file-version-detail {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.version-info-section h4,
.approval-history-section h4 {
  color: #1f2937;
  margin-bottom: 16px;
  font-size: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.version-basic-info {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
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
  font-size: 14px;
}

.info-item strong {
  min-width: 100px;
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

.history-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  color: #6b7280;
}

.history-error {
  padding: 16px;
  background: #fef2f2;
  border-radius: 8px;
}

.history-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.history-stats {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.history-groups {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.history-group {
  background: #ffffff;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.group-header h5 {
  margin: 0;
  color: #374151;
  font-size: 14px;
}

.approval-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.approval-card {
  background: #f9fafb;
  border-radius: 6px;
  padding: 12px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.approval-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.approval-card.in-review {
  border-left: 4px solid #10b981;
}

.approval-card.finished {
  border-left: 4px solid #6b7280;
}

.approval-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.review-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.review-sequence {
  font-weight: 500;
  color: #374151;
}

.approval-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.detail-item strong {
  min-width: 80px;
  color: #6b7280;
}

.review-id,
.status-id {
  background: #f3f4f6;
  padding: 1px 4px;
  border-radius: 2px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 10px;
  color: #059669;
}

.status-distribution {
  background: #ffffff;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.status-distribution h5 {
  margin: 0 0 12px 0;
  color: #374151;
  font-size: 14px;
}

.distribution-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.distribution-card {
  background: #f9fafb;
  border-radius: 6px;
  padding: 12px;
  border: 1px solid #e5e7eb;
}

.card-title {
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
  font-size: 13px;
}

.status-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.status-tag-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.count {
  font-weight: 500;
  color: #1f2937;
  font-size: 12px;
}

.history-load-button {
  text-align: center;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  border: 2px dashed #d1d5db;
}

.user-info-section {
  margin-top: 12px;
  background: #f0f9ff;
  border-radius: 6px;
  padding: 10px;
  border: 1px solid #e0f2fe;
}

.user-info-title {
  font-weight: 500;
  color: #0369a1;
  margin-bottom: 8px;
  font-size: 12px;
}

.user-info-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.user-info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #1e40af;
}

.user-info-item strong {
  min-width: 60px;
  color: #1e3a8a;
}

.timestamp-section {
  margin-top: 12px;
  background: #fef7f0;
  border-radius: 6px;
  padding: 10px;
  border: 1px solid #fed7aa;
}

.timestamp-title {
  font-weight: 500;
  color: #c2410c;
  margin-bottom: 8px;
  font-size: 12px;
}

.timestamp-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.timestamp-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #ea580c;
}

.timestamp-item strong {
  min-width: 70px;
  color: #c2410c;
}

.debug-info {
  margin-top: 12px;
}

.raw-data-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}
</style>

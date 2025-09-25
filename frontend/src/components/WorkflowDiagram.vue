<template>
  <div class="workflow-diagram">
    <div class="workflow-header">
      <h3>{{ workflow.name }}</h3>
      <div class="workflow-meta">
        <el-tag :type="workflow.status === 'ACTIVE' ? 'success' : 'warning'" size="small">
          {{ workflow.status }}
        </el-tag>
        <span class="workflow-id">ID: {{ workflow.id }}</span>
      </div>
    </div>
    
    <div class="workflow-info" v-if="workflow.description || workflow.notes">
      <div v-if="workflow.description" class="info-item">
        <strong>描述:</strong> {{ workflow.description }}
      </div>
      <div v-if="workflow.notes" class="info-item">
        <strong>备注:</strong> {{ workflow.notes }}
      </div>
    </div>

    <!-- 工作流步骤图表 -->
    <div class="workflow-steps">
      <div class="steps-container">
        <div 
          v-for="(step, index) in workflow.steps" 
          :key="step.id"
          class="step-item"
          :class="getStepClass(step.type)">
          
          <!-- 步骤连接线 -->
          <div v-if="index > 0" class="step-connector"></div>
          
          <!-- 步骤内容 -->
          <div class="step-content">
            <!-- 步骤图标和类型 -->
            <div class="step-icon">
              <el-icon :size="24">
                <User v-if="step.type === 'INITIATOR'" />
                <View v-else-if="step.type === 'REVIEWER'" />
                <CircleCheck v-else-if="step.type === 'APPROVER'" />
                <Setting v-else />
              </el-icon>
            </div>
            
            <!-- 步骤信息 -->
            <div class="step-info">
              <div class="step-title">{{ step.name }}</div>
              <div class="step-type">{{ getStepTypeText(step.type) }}</div>
              
              <!-- 期限信息 -->
              <div v-if="step.duration" class="step-duration">
                <el-tag size="small" type="info">
                  {{ step.duration }} {{ step.dueDateType === 'CALENDAR_DAY' ? '日历天' : '工作日' }}
                </el-tag>
              </div>
              
              <!-- 候选人信息 -->
              <div class="step-candidates">
                <!-- 用户 -->
                <div v-if="step.candidates?.users?.length > 0" class="candidates-section">
                  <div class="candidates-label">👤 用户:</div>
                  <div class="candidates-list">
                    <el-tag 
                      v-for="user in step.candidates.users" 
                      :key="user.autodeskId"
                      size="small" 
                      type="primary"
                      class="candidate-tag">
                      {{ user.name }}
                    </el-tag>
                  </div>
                </div>
                
                <!-- 角色 -->
                <div v-if="step.candidates?.roles?.length > 0" class="candidates-section">
                  <div class="candidates-label">🏷️ 角色:</div>
                  <div class="candidates-list">
                    <el-tag 
                      v-for="role in step.candidates.roles" 
                      :key="role.autodeskId"
                      size="small" 
                      type="success"
                      class="candidate-tag">
                      {{ role.name }}
                    </el-tag>
                  </div>
                </div>
                
                <!-- 公司 -->
                <div v-if="step.candidates?.companies?.length > 0" class="candidates-section">
                  <div class="candidates-label">🏢 公司:</div>
                  <div class="candidates-list">
                    <el-tag 
                      v-for="company in step.candidates.companies" 
                      :key="company.autodeskId"
                      size="small" 
                      type="warning"
                      class="candidate-tag">
                      {{ company.name }}
                    </el-tag>
                  </div>
                </div>
              </div>
              
              <!-- 组审查信息 -->
              <div v-if="step.groupReview?.enabled" class="group-review">
                <el-tag size="small" type="warning">
                  组审查: {{ step.groupReview.type }} 
                  {{ step.groupReview.min ? `(最少${step.groupReview.min}人)` : '' }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 审批状态选项 -->
    <div v-if="workflow.approvalStatusOptions?.length > 0" class="approval-options">
      <h4>✅ 审批状态选项</h4>
      <div class="options-grid">
        <div 
          v-for="option in workflow.approvalStatusOptions" 
          :key="option.id"
          class="option-card"
          :class="getOptionClass(option.value)">
          <div class="option-icon">
            <el-icon>
              <CircleCheck v-if="option.value === 'APPROVED'" />
              <CircleClose v-else-if="option.value === 'REJECTED'" />
              <Warning v-else />
            </el-icon>
          </div>
          <div class="option-info">
            <div class="option-label">{{ option.label }}</div>
            <div class="option-value">{{ option.value }}</div>
            <el-tag v-if="option.builtIn" size="small" type="info">内置</el-tag>
          </div>
        </div>
      </div>
    </div>

    <!-- 附加配置 -->
    <div class="additional-config">
      <div class="config-grid">
        <!-- 文件复制配置 -->
        <div v-if="workflow.copyFilesOptions?.enabled" class="config-card">
          <div class="config-header">
            <el-icon><FolderOpened /></el-icon>
            <span>文件复制配置</span>
          </div>
          <div class="config-content">
            <div class="config-item">
              <strong>允许覆盖:</strong> {{ workflow.copyFilesOptions.allowOverride ? '是' : '否' }}
            </div>
            <div class="config-item">
              <strong>条件:</strong> {{ workflow.copyFilesOptions.condition }}
            </div>
            <div class="config-item">
              <strong>包含标记:</strong> {{ workflow.copyFilesOptions.includeMarkups ? '是' : '否' }}
            </div>
          </div>
        </div>
        
        <!-- 附加选项 -->
        <div class="config-card">
          <div class="config-header">
            <el-icon><Setting /></el-icon>
            <span>附加选项</span>
          </div>
          <div class="config-content">
            <div class="config-item">
              <strong>允许发起者编辑:</strong> 
              {{ workflow.additionalOptions?.allowInitiatorToEdit ? '是' : '否' }}
            </div>
            <div class="config-item">
              <strong>附加属性:</strong> 
              {{ workflow.attachedAttributes?.length || 0 }} 个
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 时间信息 -->
    <div class="workflow-timeline">
      <div class="timeline-item">
        <strong>创建时间:</strong> {{ formatDate(workflow.createdAt) }}
      </div>
      <div class="timeline-item">
        <strong>更新时间:</strong> {{ formatDate(workflow.updatedAt) }}
      </div>
    </div>
  </div>
</template>

<script>
import { 
  User, 
  View, 
  CircleCheck, 
  CircleClose, 
  Warning, 
  Setting, 
  FolderOpened 
} from '@element-plus/icons-vue'

export default {
  name: 'WorkflowDiagram',
  components: {
    User,
    View,
    CircleCheck,
    CircleClose,
    Warning,
    Setting,
    FolderOpened
  },
  props: {
    workflow: {
      type: Object,
      required: true
    }
  },
  methods: {
    getStepClass(type) {
      const classes = {
        'INITIATOR': 'step-initiator',
        'REVIEWER': 'step-reviewer',
        'APPROVER': 'step-approver'
      }
      return classes[type] || 'step-default'
    },
    
    getStepTypeText(type) {
      const texts = {
        'INITIATOR': '发起者',
        'REVIEWER': '审阅者',
        'APPROVER': '批准者'
      }
      return texts[type] || type
    },
    
    getOptionClass(value) {
      const classes = {
        'APPROVED': 'option-approved',
        'REJECTED': 'option-rejected'
      }
      return classes[value] || 'option-default'
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString('zh-CN')
    }
  }
}
</script>

<style scoped>
.workflow-diagram {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin: 16px 0;
}

.workflow-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f2f5;
}

.workflow-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 20px;
  font-weight: 600;
}

.workflow-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.workflow-id {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  color: #6b7280;
  background: #f9fafb;
  padding: 4px 8px;
  border-radius: 4px;
}

.workflow-info {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
  border-left: 4px solid #3b82f6;
}

.info-item {
  margin-bottom: 8px;
  font-size: 14px;
  color: #374151;
}

.info-item:last-child {
  margin-bottom: 0;
}

.workflow-steps {
  margin-bottom: 32px;
}

.steps-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
}

.step-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.step-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.step-initiator {
  border-color: #10b981;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
}

.step-reviewer {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
}

.step-approver {
  border-color: #3b82f6;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.step-connector {
  position: absolute;
  left: 32px;
  top: -20px;
  width: 2px;
  height: 20px;
  background: linear-gradient(to bottom, #e5e7eb, #9ca3af);
}

.step-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  width: 100%;
}

.step-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid #e5e7eb;
}

.step-initiator .step-icon {
  background: #10b981;
  color: white;
  border-color: #10b981;
}

.step-reviewer .step-icon {
  background: #f59e0b;
  color: white;
  border-color: #f59e0b;
}

.step-approver .step-icon {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.step-info {
  flex: 1;
}

.step-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.step-type {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.step-duration {
  margin-bottom: 12px;
}

.step-candidates {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.candidates-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.candidates-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.candidates-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.candidate-tag {
  font-size: 11px;
}

.group-review {
  margin-top: 8px;
}

.approval-options {
  margin-bottom: 24px;
}

.approval-options h4 {
  color: #1f2937;
  margin-bottom: 16px;
  font-size: 16px;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.option-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: white;
  transition: all 0.2s ease;
}

.option-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.option-approved {
  border-color: #10b981;
  background: #f0fdf4;
}

.option-rejected {
  border-color: #ef4444;
  background: #fef2f2;
}

.option-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.option-approved .option-icon {
  color: #10b981;
}

.option-rejected .option-icon {
  color: #ef4444;
}

.option-info {
  flex: 1;
}

.option-label {
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 2px;
}

.option-value {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.additional-config {
  margin-bottom: 24px;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.config-card {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.config-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 12px;
}

.config-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.config-item {
  font-size: 14px;
  color: #374151;
}

.workflow-timeline {
  display: flex;
  gap: 24px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  font-size: 13px;
  color: #6b7280;
}

.timeline-item {
  display: flex;
  gap: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .workflow-diagram {
    padding: 16px;
  }
  
  .workflow-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .step-content {
    flex-direction: column;
    gap: 12px;
  }
  
  .step-icon {
    align-self: flex-start;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .config-grid {
    grid-template-columns: 1fr;
  }
  
  .workflow-timeline {
    flex-direction: column;
    gap: 8px;
  }
  
  .candidates-section {
    margin-bottom: 8px;
  }
}
</style>

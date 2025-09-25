<template>
  <el-tag 
    :type="tagType" 
    :size="size"
    :class="['status-tag', `status-${status}`, statusClass]">
    <el-icon v-if="showIcon" class="status-icon">
      <component :is="iconComponent" />
    </el-icon>
    <span class="status-text">{{ displayText }}</span>
  </el-tag>
</template>

<script>
import { 
  Check, 
  Warning, 
  Close, 
  Clock, 
  Document,
  CircleCheck,
  CircleClose,
  More
} from '@element-plus/icons-vue'

export default {
  name: 'StatusTag',
  components: {
    Check,
    Warning,
    Close,
    Clock,
    Document,
    CircleCheck,
    CircleClose,
    More
  },
  props: {
    status: {
      type: String,
      default: 'unknown',
      validator: value => typeof value === 'string' && value.length > 0
    },
    text: {
      type: String,
      default: null
    },
    size: {
      type: String,
      default: 'small',
      validator: value => ['large', 'default', 'small'].includes(value)
    },
    showIcon: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    displayText() {
      return this.text || this.getDefaultText()
    },
    
    tagType() {
      if (!this.status || typeof this.status !== 'string') {
        return 'info'
      }
      
      const statusMap = {
        // 成功状态
        'success': 'success',
        'completed': 'success', 
        'active': 'success',
        'approved': 'success',
        'submitted': 'success',
        'available': 'success',
        'ready': 'success',
        'running': 'success',
        
        // 警告状态
        'warning': 'warning',
        'pending': 'warning',
        'waiting': 'warning',
        'draft': 'warning',
        'reviewing': 'warning',
        'processing': 'warning',
        
        // 危险状态
        'error': 'danger',
        'failed': 'danger',
        'rejected': 'danger',
        'cancelled': 'danger',
        'expired': 'danger',
        'inactive': 'danger',
        'unavailable': 'danger',
        
        // 信息状态
        'info': 'info',
        'unknown': 'info',
        'default': 'info',
        'archived': 'info',
        
        // 评审相关状态映射
        'open': 'success',
        'closed': 'info',
        'void': 'warning',
        
        // 大写状态映射
        'OPEN': 'success',
        'CLOSED': 'info',
        'VOID': 'warning',
        'FAILED': 'danger',
        'ACTIVE': 'success',
        'INACTIVE': 'danger'
      }
      
      return statusMap[this.status.toLowerCase()] || 'info'
    },
    
    iconComponent() {
      if (!this.showIcon || !this.status || typeof this.status !== 'string') {
        return null
      }
      
      const iconMap = {
        // 成功图标
        'success': 'CircleCheck',
        'completed': 'CircleCheck',
        'active': 'CircleCheck',
        'approved': 'Check',
        'submitted': 'Check',
        'available': 'Check',
        'ready': 'Check',
        'running': 'Check',
        
        // 警告图标
        'warning': 'Warning',
        'pending': 'Clock',
        'waiting': 'Clock',
        'draft': 'Document',
        'reviewing': 'Clock',
        'processing': 'Clock',
        
        // 危险图标
        'error': 'CircleClose',
        'failed': 'CircleClose',
        'rejected': 'Close',
        'cancelled': 'Close',
        'expired': 'Close',
        'inactive': 'Close',
        'unavailable': 'Close',
        
        // 信息图标
        'info': 'More',
        'unknown': 'More',
        'default': 'More',
        'archived': 'Document'
      }
      
      return iconMap[this.status.toLowerCase()] || 'More'
    },
    
    statusClass() {
      if (!this.status || typeof this.status !== 'string') {
        return 'status-unknown'
      }
      return `status-${this.status.toLowerCase()}`
    }
  },
  methods: {
    getDefaultText() {
      if (!this.status || typeof this.status !== 'string') {
        return '未知'
      }
      
      const textMap = {
        'success': '成功',
        'completed': '已完成',
        'active': '活跃',
        'approved': '已审批',
        'submitted': '已提交',
        'available': '可用',
        'ready': '就绪',
        'running': '运行中',
        
        'warning': '警告',
        'pending': '待处理',
        'waiting': '等待中',
        'draft': '草稿',
        'reviewing': '审核中',
        'processing': '处理中',
        
        'error': '错误',
        'failed': '失败',
        'rejected': '已拒绝',
        'cancelled': '已取消',
        'expired': '已过期',
        'inactive': '非活跃',
        'unavailable': '不可用',
        
        'info': '信息',
        'unknown': '未知',
        'default': '默认',
        'archived': '已归档',
        
        // 评审相关状态
        'open': '开放',
        'closed': '已关闭',
        'void': '无效',
        
        // 大写状态映射
        'OPEN': '开放',
        'CLOSED': '已关闭',
        'VOID': '无效',
        'FAILED': '失败',
        'ACTIVE': '活跃',
        'INACTIVE': '非活跃'
      }
      
      return textMap[this.status.toLowerCase()] || this.status
    }
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.status-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  font-size: 12px;
  line-height: 1.2;
  border-width: 1px;
  border-style: solid;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.status-tag::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.3s ease;
}

.status-tag:hover::before {
  left: 100%;
}

.status-icon {
  font-size: 12px;
  flex-shrink: 0;
}

.status-text {
  white-space: nowrap;
  flex-shrink: 0;
}

/* 成功状态样式增强 */
.status-tag.el-tag--success {
  background: linear-gradient(135deg, #f0f9f4 0%, #e8f7ed 100%);
  color: #059669;
  border-color: #a7f3d0;
}

.status-tag.el-tag--success:hover {
  background: linear-gradient(135deg, #e8f7ed 0%, #d1fae5 100%);
  border-color: #6ee7b7;
  transform: translateY(-1px);
}

/* 警告状态样式增强 */
.status-tag.el-tag--warning {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  color: #d97706;
  border-color: #fde68a;
}

.status-tag.el-tag--warning:hover {
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border-color: #fbbf24;
  transform: translateY(-1px);
}

/* 危险状态样式增强 */
.status-tag.el-tag--danger {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
  border-color: #fecaca;
}

.status-tag.el-tag--danger:hover {
  background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%);
  border-color: #f87171;
  transform: translateY(-1px);
}

/* 信息状态样式增强 */
.status-tag.el-tag--info {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  color: #475569;
  border-color: #cbd5e1;
}

.status-tag.el-tag--info:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border-color: #94a3b8;
  transform: translateY(-1px);
}

/* 大尺寸样式 */
.status-tag.el-tag--large {
  padding: 6px 12px;
  font-size: 14px;
  border-radius: var(--border-radius-lg);
}

.status-tag.el-tag--large .status-icon {
  font-size: 14px;
}

/* 默认尺寸样式 */
.status-tag.el-tag--default {
  padding: 5px 10px;
  font-size: 13px;
}

.status-tag.el-tag--default .status-icon {
  font-size: 13px;
}

/* 特定状态的额外样式 */
.status-submitted {
  box-shadow: 0 1px 3px rgba(16, 185, 129, 0.12);
}

.status-pending {
  box-shadow: 0 1px 3px rgba(217, 119, 6, 0.12);
}

.status-error,
.status-failed {
  box-shadow: 0 1px 3px rgba(220, 38, 38, 0.12);
}

.status-archived,
.status-inactive {
  opacity: 0.8;
}

/* 动画效果 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.status-processing,
.status-running {
  animation: pulse 2s infinite;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .status-tag {
    font-size: 11px;
    padding: 3px 6px;
  }
  
  .status-icon {
    font-size: 11px;
  }
}
</style>

<template>
  <div class="status-indicator" :class="statusClass">
    <div class="status-main">
      <div class="status-icon">
        <el-icon :size="iconSize" :color="statusColor">
          <component :is="statusIcon" />
        </el-icon>
      </div>
      
      <div class="status-content">
        <div class="status-title">{{ title }}</div>
        <div v-if="description" class="status-description">{{ description }}</div>
        <div v-if="details" class="status-details">{{ details }}</div>
      </div>
      
      <div v-if="showCode" class="status-code">
        <el-tag :type="tagType" size="small">{{ code }}</el-tag>
      </div>
    </div>
    
    <!-- 额外信息 -->
    <div v-if="$slots.extra || suggestion" class="status-extra">
      <div v-if="suggestion" class="status-suggestion">
        <el-text type="info" size="small">
          <i class="el-icon-lightbulb"></i>
          {{ suggestion }}
        </el-text>
      </div>
      <slot name="extra"></slot>
    </div>
  </div>
</template>

<script>
import { 
  CircleCheck, 
  CircleClose, 
  Warning, 
  InfoFilled,
  Clock,
  Refresh
} from '@element-plus/icons-vue'

export default {
  name: 'StatusIndicator',
  components: {
    CircleCheck,
    CircleClose,
    Warning,
    InfoFilled,
    Clock,
    Refresh
  },
  props: {
    status: {
      type: String,
      required: true,
      validator: (value) => ['success', 'error', 'warning', 'info', 'loading', 'pending'].includes(value)
    },
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      default: ''
    },
    details: {
      type: String,
      default: ''
    },
    code: {
      type: [String, Number],
      default: ''
    },
    suggestion: {
      type: String,
      default: ''
    },
    showCode: {
      type: Boolean,
      default: true
    },
    size: {
      type: String,
      default: 'default', // 'small', 'default', 'large'
      validator: (value) => ['small', 'default', 'large'].includes(value)
    }
  },
  computed: {
    statusClass() {
      return [`status-${this.status}`, `size-${this.size}`]
    },
    
    statusIcon() {
      const iconMap = {
        success: 'CircleCheck',
        error: 'CircleClose',
        warning: 'Warning',
        info: 'InfoFilled',
        loading: 'Refresh',
        pending: 'Clock'
      }
      return iconMap[this.status] || 'InfoFilled'
    },
    
    statusColor() {
      const colorMap = {
        success: '#67c23a',
        error: '#f56c6c',
        warning: '#e6a23c',
        info: '#409eff',
        loading: '#909399',
        pending: '#909399'
      }
      return colorMap[this.status] || '#909399'
    },
    
    tagType() {
      const typeMap = {
        success: 'success',
        error: 'danger',
        warning: 'warning',
        info: 'primary',
        loading: 'info',
        pending: 'info'
      }
      return typeMap[this.status] || 'info'
    },
    
    iconSize() {
      const sizeMap = {
        small: 16,
        default: 20,
        large: 24
      }
      return sizeMap[this.size] || 20
    }
  }
}
</script>

<style scoped>
.status-indicator {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.status-main {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
}

.status-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.status-content {
  flex: 1;
  min-width: 0;
}

.status-title {
  font-weight: 600;
  font-size: 16px;
  color: #2c3e50;
  margin-bottom: 4px;
  line-height: 1.4;
}

.status-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 4px;
  line-height: 1.5;
}

.status-details {
  color: #909399;
  font-size: 13px;
  line-height: 1.4;
}

.status-code {
  flex-shrink: 0;
  margin-top: 2px;
}

.status-extra {
  border-top: 1px solid #f0f0f0;
  padding: 12px 16px;
  background: #fafafa;
}

.status-suggestion {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 状态主题色 */
.status-success {
  border-left: 4px solid #67c23a;
}

.status-error {
  border-left: 4px solid #f56c6c;
}

.status-warning {
  border-left: 4px solid #e6a23c;
}

.status-info {
  border-left: 4px solid #409eff;
}

.status-loading, .status-pending {
  border-left: 4px solid #909399;
}

/* 加载动画 */
.status-loading .status-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 尺寸变体 */
.size-small .status-main {
  padding: 12px;
  gap: 8px;
}

.size-small .status-title {
  font-size: 14px;
}

.size-small .status-description {
  font-size: 13px;
}

.size-small .status-details {
  font-size: 12px;
}

.size-large .status-main {
  padding: 20px;
  gap: 16px;
}

.size-large .status-title {
  font-size: 18px;
}

.size-large .status-description {
  font-size: 15px;
}

.size-large .status-details {
  font-size: 14px;
}

/* 悬停效果 */
.status-indicator:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  transform: translateY(-2px);
  border-color: #d0d7de;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .status-main {
    flex-direction: column;
    gap: 8px;
  }
  
  .status-icon {
    align-self: flex-start;
  }
  
  .status-code {
    align-self: flex-start;
    margin-top: 8px;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .status-indicator {
    background: #2c3e50;
    border-color: #34495e;
  }
  
  .status-title {
    color: #ecf0f1;
  }
  
  .status-description {
    color: #bdc3c7;
  }
  
  .status-details {
    color: #95a5a6;
  }
  
  .status-extra {
    background: #34495e;
    border-color: #34495e;
  }
}
</style>

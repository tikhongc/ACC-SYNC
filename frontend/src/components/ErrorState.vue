<template>
  <div class="error-state" :class="[`type-${type}`, `severity-${severity}`]">
    <div class="error-content">
      <div class="error-icon">
        <el-icon :size="iconSize" :color="iconColor">
          <component :is="errorIcon" />
        </el-icon>
      </div>
      
      <div class="error-text">
        <h3 class="error-title">{{ title }}</h3>
        <p v-if="message" class="error-message">{{ message }}</p>
        <div v-if="details" class="error-details">
          <el-collapse>
            <el-collapse-item title="查看详细信息" name="details">
              <pre class="error-details-content">{{ details }}</pre>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>
    </div>
    
    <div v-if="showActions" class="error-actions">
      <slot name="actions">
        <ActionButtons 
          :buttons="actionButtons" 
          layout="horizontal"
          @button-click="handleAction" />
      </slot>
    </div>
    
    <!-- 建议信息 -->
    <div v-if="suggestions.length > 0" class="error-suggestions">
      <h4 class="suggestions-title">💡 解决建议</h4>
      <ul class="suggestions-list">
        <li v-for="(suggestion, index) in suggestions" :key="index">
          {{ suggestion }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { 
  CircleClose, 
  Warning, 
  InfoFilled,
  WarnTriangleFilled,
  QuestionFilled
} from '@element-plus/icons-vue'
import ActionButtons from './ActionButtons.vue'

export default {
  name: 'ErrorState',
  components: {
    CircleClose,
    Warning,
    InfoFilled,
    WarnTriangleFilled,
    QuestionFilled,
    ActionButtons
  },
  props: {
    // 错误类型
    type: {
      type: String,
      default: 'card', // 'card', 'inline', 'banner'
      validator: (value) => ['card', 'inline', 'banner'].includes(value)
    },
    
    // 严重程度
    severity: {
      type: String,
      default: 'error', // 'error', 'warning', 'info'
      validator: (value) => ['error', 'warning', 'info'].includes(value)
    },
    
    // 内容
    title: {
      type: String,
      required: true
    },
    message: {
      type: String,
      default: ''
    },
    details: {
      type: String,
      default: ''
    },
    
    // 建议
    suggestions: {
      type: Array,
      default: () => []
    },
    
    // 操作按钮
    showActions: {
      type: Boolean,
      default: true
    },
    actionButtons: {
      type: Array,
      default: () => [
        {
          text: '重试',
          type: 'primary',
          action: 'retry'
        },
        {
          text: '返回',
          type: 'default',
          action: 'back'
        }
      ]
    },
    
    // 样式
    size: {
      type: String,
      default: 'default', // 'small', 'default', 'large'
      validator: (value) => ['small', 'default', 'large'].includes(value)
    }
  },
  computed: {
    errorIcon() {
      const iconMap = {
        error: 'CircleClose',
        warning: 'WarnTriangleFilled',
        info: 'InfoFilled'
      }
      return iconMap[this.severity] || 'CircleClose'
    },
    
    iconColor() {
      const colorMap = {
        error: '#f56c6c',
        warning: '#e6a23c',
        info: '#409eff'
      }
      return colorMap[this.severity] || '#f56c6c'
    },
    
    iconSize() {
      const sizeMap = {
        small: 32,
        default: 48,
        large: 64
      }
      return sizeMap[this.size] || 48
    }
  },
  emits: ['action'],
  methods: {
    handleAction(action, button, index) {
      this.$emit('action', action, button, index)
    }
  }
}
</script>

<style scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--spacing-lg);
}

/* 卡片类型 */
.type-card {
  background: var(--color-bg-primary);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-border-light);
  padding: var(--spacing-xxl);
  max-width: 500px;
  margin: var(--spacing-xl) auto;
}

.type-card.severity-error {
  border-left: 4px solid #f56c6c;
  background: linear-gradient(135deg, #fef0f0 0%, #ffffff 100%);
}

.type-card.severity-warning {
  border-left: 4px solid #e6a23c;
  background: linear-gradient(135deg, #fdf6ec 0%, #ffffff 100%);
}

.type-card.severity-info {
  border-left: 4px solid #409eff;
  background: linear-gradient(135deg, #ecf5ff 0%, #ffffff 100%);
}

/* 内联类型 */
.type-inline {
  flex-direction: row;
  text-align: left;
  padding: var(--spacing-md);
  background: var(--color-bg-secondary);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border-light);
}

.type-inline .error-content {
  flex-direction: row;
  text-align: left;
  gap: var(--spacing-md);
}

.type-inline .error-icon {
  flex-shrink: 0;
  margin-top: var(--spacing-xs);
}

/* 横幅类型 */
.type-banner {
  width: 100%;
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  margin-bottom: var(--spacing-lg);
}

.type-banner.severity-error {
  background: #fef0f0;
  border: 1px solid #fbc4c4;
  color: #c45656;
}

.type-banner.severity-warning {
  background: #fdf6ec;
  border: 1px solid #f5dab1;
  color: #b88230;
}

.type-banner.severity-info {
  background: #ecf5ff;
  border: 1px solid #b3d8ff;
  color: #337ecc;
}

/* 内容区域 */
.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  width: 100%;
}

.error-icon {
  flex-shrink: 0;
}

.error-text {
  flex: 1;
  min-width: 0;
}

.error-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
  line-height: 1.3;
}

.error-message {
  color: var(--color-text-regular);
  margin: 0 0 var(--spacing-md) 0;
  line-height: 1.5;
  font-size: 1rem;
}

.error-details {
  width: 100%;
  margin-top: var(--spacing-md);
}

.error-details-content {
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  font-family: var(--font-family-mono);
  font-size: 0.8rem;
  line-height: 1.4;
  color: var(--color-text-regular);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 200px;
  overflow-y: auto;
  margin: 0;
}

/* 操作按钮 */
.error-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

/* 建议信息 */
.error-suggestions {
  width: 100%;
  text-align: left;
  background: var(--color-bg-secondary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border-light);
}

.suggestions-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-md) 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.suggestions-list {
  margin: 0;
  padding-left: var(--spacing-lg);
  color: var(--color-text-regular);
}

.suggestions-list li {
  margin-bottom: var(--spacing-xs);
  line-height: 1.5;
}

.suggestions-list li:last-child {
  margin-bottom: 0;
}

/* 尺寸变体 */
.error-state.size-small {
  gap: var(--spacing-md);
}

.error-state.size-small .type-card {
  padding: var(--spacing-lg);
  max-width: 400px;
}

.error-state.size-small .error-title {
  font-size: 1rem;
}

.error-state.size-small .error-message {
  font-size: 0.9rem;
}

.error-state.size-large {
  gap: var(--spacing-xl);
}

.error-state.size-large .type-card {
  padding: 3rem;
  max-width: 600px;
}

.error-state.size-large .error-title {
  font-size: 1.4rem;
}

.error-state.size-large .error-message {
  font-size: 1.1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .type-card {
    margin: var(--spacing-md);
    padding: var(--spacing-lg) !important;
    max-width: none !important;
  }
  
  .error-actions {
    flex-direction: column;
  }
  
  .error-actions .el-button {
    width: 100%;
  }
  
  .type-inline {
    flex-direction: column;
    text-align: center;
  }
  
  .type-inline .error-content {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .error-title {
    font-size: 1.1rem !important;
  }
  
  .error-message {
    font-size: 0.9rem !important;
  }
  
  .suggestions-title {
    font-size: 0.9rem;
  }
  
  .suggestions-list {
    font-size: 0.8rem;
  }
}
</style>

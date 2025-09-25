<template>
  <div class="page-header" :class="{ 'compact': compact }">
    <div class="header-content">
      <!-- 左侧：标题区域 -->
      <div class="header-left">
        <div class="title-section">
          <h1 v-if="title" class="page-title">
            <component v-if="icon" :is="icon" class="title-icon" />
            <span class="title-text">{{ title }}</span>
            <el-tag v-if="tag" :type="tagType" size="small" class="title-tag">{{ tag }}</el-tag>
          </h1>
          <p v-if="description" class="page-description">{{ description }}</p>
        </div>
      </div>
      
      <!-- 右侧：操作区域 -->
      <div v-if="$slots.actions || actionButtons.length > 0" class="header-right">
        <div class="header-actions">
          <slot name="actions"></slot>
          <ActionButtons 
            v-if="actionButtons.length > 0"
            :buttons="actionButtons" 
            :layout="compact ? 'compact' : 'horizontal'"
            @button-click="handleAction" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ActionButtons from './ActionButtons.vue'

export default {
  name: 'PageHeader',
  components: {
    ActionButtons
  },
  props: {
    // 基础内容
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    icon: {
      type: [String, Object],
      default: null
    },
    
    // 标签
    tag: {
      type: String,
      default: ''
    },
    tagType: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'success', 'warning', 'danger', 'info'].includes(value)
    },
    
    // 布局
    compact: {
      type: Boolean,
      default: false
    },
    
    // 操作按钮
    actionButtons: {
      type: Array,
      default: () => []
    }
  },
  
  emits: ['action'],
  
  methods: {
    handleAction(action) {
      this.$emit('action', action)
    }
  }
}
</script>

<style scoped>
/* CSS变量定义 */
:root {
  --header-padding: 24px 32px;
  --header-min-height: 80px;
  --title-font-size: 24px;
  --description-font-size: 14px;
  --icon-size: 20px;
  --border-radius: 8px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-lg: 16px;
}

/* 主容器 */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: var(--border-radius);
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 头部内容 */
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--header-padding);
  min-height: var(--header-min-height);
  gap: var(--spacing-lg);
}

/* 左侧标题区域 */
.header-left {
  flex: 1;
  min-width: 0;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.page-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin: 0;
  font-size: var(--title-font-size);
  font-weight: 600;
  line-height: 1.2;
}

.title-icon {
  font-size: var(--icon-size);
  opacity: 0.9;
  flex-shrink: 0;
}

.title-text {
  flex: 1;
  min-width: 0;
}

.title-tag {
  font-size: 12px;
  font-weight: normal;
  flex-shrink: 0;
}

.page-description {
  margin: 0;
  font-size: var(--description-font-size);
  opacity: 0.85;
  line-height: 1.4;
}

/* 右侧操作区域 */
.header-right {
  flex-shrink: 0;
  margin-left: auto;
  align-self: flex-start;
  padding-top: 8px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  justify-content: flex-end;
}

/* 紧凑模式 */
.compact {
  margin-bottom: 16px;
}

.compact .header-content {
  padding: 16px 24px;
  min-height: 60px;
}

.compact .page-title {
  font-size: 20px;
}

.compact .page-description {
  font-size: 13px;
}

.compact .title-icon {
  font-size: 18px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-lg);
    padding: 20px;
    min-height: auto;
  }
  
  .page-title {
    font-size: 20px;
    flex-wrap: wrap;
  }
  
  .header-actions {
    justify-content: flex-end;
    margin-top: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .header-content {
    padding: 16px;
  }
  
  .page-title {
    font-size: 18px;
  }
  
  .page-description {
    font-size: 13px;
  }
  
  .title-icon {
    font-size: 16px;
  }
}

/* 确保ActionButtons样式正确 */
.header-actions :deep(.el-button) {
  border-radius: 6px;
  font-size: 14px;
}

.header-actions :deep(.el-button .arco-icon),
.header-actions :deep(.arco-icon) {
  font-size: 14px !important;
}

/* 全局图标大小控制 */
.page-header :deep(.arco-icon) {
  font-size: var(--icon-size) !important;
}
</style>
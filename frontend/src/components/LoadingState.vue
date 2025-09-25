<template>
  <div class="loading-state" :class="[`type-${type}`, `size-${size}`]">
    <div v-if="type === 'card'" class="loading-card">
      <div class="loading-content">
        <div class="loading-spinner">
          <el-icon class="rotating">
            <Loading />
          </el-icon>
        </div>
        <div class="loading-text">
          <h3 v-if="title">{{ title }}</h3>
          <p>{{ text }}</p>
          <div v-if="showProgress && progress >= 0" class="loading-progress">
            <el-progress 
              :percentage="progress" 
              :status="progressStatus"
              :stroke-width="6" />
          </div>
        </div>
      </div>
      <div v-if="showCancel" class="loading-actions">
        <el-button size="small" @click="$emit('cancel')">取消</el-button>
      </div>
    </div>
    
    <div v-else-if="type === 'overlay'" class="loading-overlay" v-loading="true" :element-loading-text="text">
      <div class="overlay-content">
        <slot></slot>
      </div>
    </div>
    
    <div v-else-if="type === 'inline'" class="loading-inline">
      <el-icon class="rotating">
        <Loading />
      </el-icon>
      <span class="loading-text">{{ text }}</span>
    </div>
    
    <div v-else-if="type === 'skeleton'" class="loading-skeleton">
      <el-skeleton :rows="skeletonRows" :animated="true" />
    </div>
    
    <div v-else class="loading-simple">
      <el-loading-directive v-loading="true" :element-loading-text="text" />
    </div>
  </div>
</template>

<script>
import { Loading } from '@element-plus/icons-vue'

export default {
  name: 'LoadingState',
  components: {
    Loading
  },
  props: {
    // 加载类型
    type: {
      type: String,
      default: 'simple', // 'simple', 'card', 'overlay', 'inline', 'skeleton'
      validator: (value) => ['simple', 'card', 'overlay', 'inline', 'skeleton'].includes(value)
    },
    
    // 尺寸
    size: {
      type: String,
      default: 'default', // 'small', 'default', 'large'
      validator: (value) => ['small', 'default', 'large'].includes(value)
    },
    
    // 文本内容
    title: {
      type: String,
      default: ''
    },
    text: {
      type: String,
      default: '加载中...'
    },
    
    // 进度条
    showProgress: {
      type: Boolean,
      default: false
    },
    progress: {
      type: Number,
      default: -1
    },
    progressStatus: {
      type: String,
      default: 'primary'
    },
    
    // 取消按钮
    showCancel: {
      type: Boolean,
      default: false
    },
    
    // 骨架屏配置
    skeletonRows: {
      type: Number,
      default: 5
    },
    
    // 高度
    height: {
      type: [String, Number],
      default: ''
    },
    minHeight: {
      type: [String, Number],
      default: '200px'
    }
  },
  emits: ['cancel']
}
</script>

<style scoped>
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: v-bind(minHeight);
  height: v-bind(height);
}

/* 卡片类型 */
.loading-card {
  background: var(--color-bg-primary);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-border-light);
  padding: var(--spacing-xxl);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
}

.loading-spinner {
  font-size: 3rem;
  color: var(--color-primary);
}

.loading-text h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.loading-text p {
  color: var(--color-text-secondary);
  margin: 0;
  font-size: 1rem;
}

.loading-progress {
  width: 100%;
  margin-top: var(--spacing-md);
}

.loading-actions {
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border-light);
}

/* 覆盖层类型 */
.loading-overlay {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 200px;
}

.overlay-content {
  opacity: 0.3;
  pointer-events: none;
}

/* 内联类型 */
.loading-inline {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--color-text-secondary);
  font-size: 0.9rem;
}

.loading-inline .loading-text {
  color: var(--color-text-secondary);
}

/* 骨架屏类型 */
.loading-skeleton {
  width: 100%;
  padding: var(--spacing-lg);
}

/* 简单类型 */
.loading-simple {
  position: relative;
  width: 100%;
  height: 200px;
}

/* 旋转动画 */
.rotating {
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 尺寸变体 */
.size-small .loading-card {
  padding: var(--spacing-lg);
  max-width: 300px;
}

.size-small .loading-spinner {
  font-size: 2rem;
}

.size-small .loading-text h3 {
  font-size: 1rem;
}

.size-small .loading-text p {
  font-size: 0.9rem;
}

.size-large .loading-card {
  padding: 3rem;
  max-width: 500px;
}

.size-large .loading-spinner {
  font-size: 4rem;
}

.size-large .loading-text h3 {
  font-size: 1.4rem;
}

.size-large .loading-text p {
  font-size: 1.1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .loading-card {
    margin: var(--spacing-md);
    padding: var(--spacing-lg);
  }
  
  .loading-spinner {
    font-size: 2.5rem !important;
  }
  
  .loading-text h3 {
    font-size: 1.1rem !important;
  }
  
  .loading-text p {
    font-size: 0.9rem !important;
  }
}
</style>

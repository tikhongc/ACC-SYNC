<template>
  <el-card :class="['base-card', cardClass]" :style="cardStyle">
    <template #header v-if="$slots.header || title">
      <div class="card-header">
        <div class="card-title-section">
          <span v-if="icon" class="card-icon">{{ icon }}</span>
          <span class="card-title">{{ title }}</span>
          <el-tag v-if="tag" :type="tagType" size="small">{{ tag }}</el-tag>
        </div>
        <div v-if="$slots.actions" class="card-actions">
          <slot name="actions"></slot>
        </div>
        <slot name="header"></slot>
      </div>
    </template>
    
    <div class="card-content">
      <slot></slot>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'BaseCard',
  props: {
    title: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: ''
    },
    tag: {
      type: String,
      default: ''
    },
    tagType: {
      type: String,
      default: 'primary'
    },
    cardClass: {
      type: String,
      default: ''
    },
    cardStyle: {
      type: Object,
      default: () => ({})
    },
    hover: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.base-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
}

.base-card:hover {
  box-shadow: 0 6px 16px rgba(0,0,0,0.12);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  flex-wrap: wrap;
  gap: 12px;
}

.card-title-section {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.card-icon {
  font-size: 18px;
}

.card-title {
  font-weight: 600;
  font-size: 16px;
  color: #2c3e50;
}

.card-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.card-content {
  padding: 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .card-actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>

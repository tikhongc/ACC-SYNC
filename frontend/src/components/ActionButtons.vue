<template>
  <div :class="['action-buttons', layoutClass]">
    <el-button
      v-for="(button, index) in buttons"
      :key="index"
      :type="button.type || 'default'"
      :size="button.size || 'default'"
      :icon="button.icon"
      :loading="button.loading || false"
      :disabled="button.disabled || false"
      @click="handleClick(button, index)"
      :class="buttonClass">
      {{ button.text }}
    </el-button>
  </div>
</template>

<script>
export default {
  name: 'ActionButtons',
  props: {
    buttons: {
      type: Array,
      required: true,
      validator: (buttons) => {
        return buttons.every(button => 
          typeof button === 'object' && 
          button.text && 
          (typeof button.action === 'function' || typeof button.action === 'string')
        )
      }
    },
    layout: {
      type: String,
      default: 'horizontal', // 'horizontal', 'vertical', 'grid', 'compact'
      validator: (value) => ['horizontal', 'vertical', 'grid', 'compact'].includes(value)
    },
    buttonClass: {
      type: String,
      default: ''
    }
  },
  computed: {
    layoutClass() {
      return `layout-${this.layout}`
    }
  },
  methods: {
    handleClick(button, index) {
      if (typeof button.action === 'function') {
        button.action(button, index)
      } else if (typeof button.action === 'string') {
        this.$emit('button-click', button.action, button, index)
      }
    }
  }
}
</script>

<style scoped>
.action-buttons {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.layout-horizontal {
  flex-direction: row;
  flex-wrap: wrap;
}

.layout-vertical {
  flex-direction: column;
}

.layout-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.layout-grid .el-button {
  width: 100%;
}

.layout-compact {
  flex-direction: row;
  gap: 8px;
}

.layout-compact .el-button {
  padding: 6px 12px;
  font-size: 13px;
  border-radius: 6px;
}

/* Enhanced button styling */
.action-buttons .el-button {
  font-weight: 500;
  border-radius: 8px;
  padding: 8px 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-buttons .el-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.action-buttons .el-button:active {
  transform: translateY(0);
}

/* Primary button enhancement */
.action-buttons .el-button--primary {
  background: linear-gradient(135deg, #409eff 0%, #3a8ee6 100%);
  border: none;
}

.action-buttons .el-button--primary:hover {
  background: linear-gradient(135deg, #3a8ee6 0%, #337ecc 100%);
}

/* Default button enhancement */
.action-buttons .el-button--default {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #2c3e50;
  backdrop-filter: blur(10px);
}

.action-buttons .el-button--default:hover {
  background: rgba(255, 255, 255, 1);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Success button enhancement */
.action-buttons .el-button--success {
  background: linear-gradient(135deg, #67c23a 0%, #5daf34 100%);
  border: none;
}

.action-buttons .el-button--success:hover {
  background: linear-gradient(135deg, #5daf34 0%, #529b2e 100%);
}

/* Loading and disabled states */
.action-buttons .el-button.is-loading {
  pointer-events: none;
}

.action-buttons .el-button.is-disabled {
  opacity: 0.6;
  pointer-events: none;
  transform: none !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}

/* Icon spacing */
.action-buttons .el-button .el-icon {
  margin-right: 6px;
}

.action-buttons .el-button .el-icon + span {
  margin-left: 2px;
}

/* Responsive design */
@media (max-width: 768px) {
  .action-buttons {
    gap: 12px;
    width: 100%;
  }
  
  .layout-horizontal {
    flex-direction: row;
    justify-content: flex-end;
    flex-wrap: wrap;
  }
  
  .layout-horizontal .el-button {
    min-width: 100px;
    flex: 0 0 auto;
  }
  
  .layout-grid {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .action-buttons {
    gap: 8px;
  }
  
  .layout-horizontal {
    flex-direction: column;
    align-items: stretch;
  }
  
  .layout-horizontal .el-button {
    width: 100%;
    min-width: auto;
  }
  
  .layout-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons .el-button {
    padding: 10px 16px;
    font-size: 14px;
  }
}
</style>

<template>
  <div class="stats-section" v-if="stats.length > 0">
    <div class="stats-container">
      <div 
        v-for="(stat, index) in stats" 
        :key="index" 
        class="stat-card"
        :class="[`stat-${stat.type}`, { 'clickable': stat.clickable }]"
        @click="stat.clickable && $emit('stat-click', stat, index)">
        <div class="stat-icon" v-if="stat.icon">
          <span v-if="typeof stat.icon === 'string' && !stat.icon.includes('-')">{{ stat.icon }}</span>
          <component v-else :is="stat.icon" />
        </div>
        <div class="stat-content">
          <div class="stat-value" :class="stat.valueClass">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div v-if="stat.description" class="stat-description">{{ stat.description }}</div>
        </div>
        <div v-if="stat.trend" class="stat-trend" :class="`trend-${stat.trend.type}`">
          <span class="trend-icon">{{ getTrendIcon(stat.trend.type) }}</span>
          <span class="trend-value">{{ stat.trend.value }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatsSection',
  props: {
    stats: {
      type: Array,
      default: () => []
    },
    layout: {
      type: String,
      default: 'grid', // 'grid', 'horizontal', 'vertical'
      validator: (value) => ['grid', 'horizontal', 'vertical'].includes(value)
    },
    columns: {
      type: Number,
      default: 4
    }
  },
  emits: ['stat-click'],
  methods: {
    getTrendIcon(type) {
      const icons = {
        up: '↗',
        down: '↘',
        stable: '→'
      }
      return icons[type] || '→'
    }
  }
}
</script>

<style scoped>
.stats-section {
  margin: var(--spacing-xl) 0;
  padding: var(--spacing-lg);
  background: var(--color-bg-primary);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--spacing-xl);
  background: var(--color-bg-secondary);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border-light);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--color-border-light);
  transition: all 0.3s ease;
}

.stat-card.stat-primary::before {
  background: var(--color-primary);
}

.stat-card.stat-success::before {
  background: var(--color-success);
}

.stat-card.stat-info::before {
  background: var(--color-info);
}

.stat-card.stat-warning::before {
  background: var(--color-warning);
}

.stat-card.stat-danger::before {
  background: var(--color-danger);
}

.stat-card.clickable {
  cursor: pointer;
}

.stat-card.clickable:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-primary);
}

.stat-card.clickable:hover::before {
  height: 4px;
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.8;
  color: var(--color-text-secondary);
}

.stat-content {
  flex: 1;
  width: 100%;
}

.stat-value {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: var(--spacing-xs);
  line-height: 1;
  color: var(--color-text-primary);
}

.stat-card.stat-primary .stat-value {
  color: var(--color-primary);
}

.stat-card.stat-success .stat-value {
  color: var(--color-success);
}

.stat-card.stat-info .stat-value {
  color: var(--color-info);
}

.stat-card.stat-warning .stat-value {
  color: var(--color-warning);
}

.stat-card.stat-danger .stat-value {
  color: var(--color-danger);
}

.stat-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--spacing-xs);
}

.stat-description {
  font-size: 0.8rem;
  color: var(--color-text-tertiary);
  line-height: 1.4;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-sm);
  font-size: 0.8rem;
  font-weight: 600;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-tertiary);
}

.trend-up {
  color: var(--color-success);
  background: rgba(var(--color-success-rgb), 0.1);
}

.trend-down {
  color: var(--color-danger);
  background: rgba(var(--color-danger-rgb), 0.1);
}

.trend-stable {
  color: var(--color-info);
  background: rgba(var(--color-info-rgb), 0.1);
}

.trend-icon {
  font-size: 1rem;
}

/* 布局变体 */
.stats-container.layout-horizontal {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.stats-container.layout-vertical {
  display: flex;
  flex-direction: column;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--spacing-md);
  }
  
  .stat-card {
    padding: var(--spacing-lg);
  }
  
  .stat-icon {
    font-size: 2rem;
  }
  
  .stat-value {
    font-size: 1.8rem;
  }
}

@media (max-width: 480px) {
  .stats-container {
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-sm);
  }
  
  .stat-card {
    padding: var(--spacing-md);
  }
  
  .stat-icon {
    font-size: 1.8rem;
    margin-bottom: var(--spacing-sm);
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
}
</style>

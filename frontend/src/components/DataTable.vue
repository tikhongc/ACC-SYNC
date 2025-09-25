<template>
  <div class="data-table">
    <!-- 表格头部 -->
    <div v-if="showHeader" class="table-header">
      <div class="table-info">
        <h3 v-if="title" class="table-title">{{ title }}</h3>
        <p v-if="description" class="table-description">{{ description }}</p>
        <div v-if="showStats" class="table-stats">
          <el-tag size="small" type="info">
            <i class="el-icon-document"></i>
            共 {{ tableData.length }} 条记录
          </el-tag>
        </div>
      </div>
      <div v-if="$slots.actions || showActions" class="table-actions">
        <slot name="actions"></slot>
        <ActionButtons 
          v-if="actionButtons.length > 0"
          :buttons="actionButtons" 
          layout="horizontal"
          @button-click="handleAction" />
      </div>
    </div>

    <!-- 表格主体 -->
    <div class="table-container">
      <el-table 
        :data="paginatedData"
        :loading="loading"
        :stripe="stripe"
        :border="border"
        :size="size"
        :height="height"
        :max-height="maxHeight"
        :empty-text="emptyText"
        :default-sort="defaultSort"
        :row-key="rowKey"
        @selection-change="handleSelectionChange"
        @sort-change="handleSortChange"
        @row-click="handleRowClick"
        v-bind="$attrs">
        
        <!-- 选择列 -->
        <el-table-column 
          v-if="selectable" 
          type="selection" 
          width="55" 
          align="center" />
        
        <!-- 序号列 -->
        <el-table-column 
          v-if="showIndex" 
          type="index" 
          label="#" 
          width="60" 
          align="center" />
        
        <!-- 动态列 -->
        <el-table-column
          v-for="column in columns"
          :key="column.prop"
          :prop="column.prop"
          :label="column.label"
          :width="column.width"
          :min-width="column.minWidth"
          :fixed="column.fixed"
          :sortable="column.sortable"
          :align="column.align || 'left'"
          :show-overflow-tooltip="column.showOverflowTooltip !== false">
          
          <template #default="scope">
            <!-- 自定义插槽 -->
            <slot 
              v-if="column.slot" 
              :name="column.slot" 
              :row="scope.row" 
              :column="column" 
              :index="scope.$index">
            </slot>
            
            <!-- 标签类型 -->
            <el-tag 
              v-else-if="column.type === 'tag'"
              :type="getTagType(scope.row[column.prop], column.tagMap)"
              size="small">
              {{ getTagText(scope.row[column.prop], column.tagMap) }}
            </el-tag>
            
            <!-- 状态类型 -->
            <StatusIndicator
              v-else-if="column.type === 'status'"
              :status="getStatusType(scope.row[column.prop], column.statusMap)"
              :title="getStatusText(scope.row[column.prop], column.statusMap)"
              size="small" />
            
            <!-- 时间类型 -->
            <span v-else-if="column.type === 'datetime'">
              {{ formatDateTime(scope.row[column.prop]) }}
            </span>
            
            <!-- 数字类型 -->
            <span v-else-if="column.type === 'number'">
              {{ formatNumber(scope.row[column.prop], column.precision) }}
            </span>
            
            <!-- 链接类型 -->
            <el-link 
              v-else-if="column.type === 'link'"
              :href="scope.row[column.prop]"
              target="_blank"
              type="primary">
              {{ scope.row[column.prop] }}
            </el-link>
            
            <!-- 默认文本 -->
            <span v-else>{{ scope.row[column.prop] }}</span>
          </template>
        </el-table-column>
        
        <!-- 操作列 -->
        <el-table-column 
          v-if="$slots.operations || operations.length > 0" 
          label="操作" 
          :width="operationWidth"
          fixed="right"
          align="center">
          <template #default="scope">
            <slot name="operations" :row="scope.row" :index="scope.$index">
              <ActionButtons 
                :buttons="getRowOperations(scope.row, scope.$index)"
                layout="horizontal"
                button-class="table-operation-btn"
                @button-click="handleRowOperation" />
            </slot>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div v-if="showPagination && totalCount > currentPageSize" class="table-pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="currentPageSize"
          :page-sizes="pageSizes"
          :total="totalCount"
          :background="true"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange" />
    </div>
  </div>
</template>

<script>
import ActionButtons from './ActionButtons.vue'
import StatusIndicator from './StatusIndicator.vue'

export default {
  name: 'DataTable',
  components: {
    ActionButtons,
    StatusIndicator
  },
  props: {
    // 数据
    data: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      required: true
    },
    
    // 表格配置
    loading: {
      type: Boolean,
      default: false
    },
    stripe: {
      type: Boolean,
      default: true
    },
    border: {
      type: Boolean,
      default: true
    },
    size: {
      type: String,
      default: 'default'
    },
    height: {
      type: [String, Number],
      default: ''
    },
    maxHeight: {
      type: [String, Number],
      default: ''
    },
    emptyText: {
      type: String,
      default: '暂无数据'
    },
    defaultSort: {
      type: Object,
      default: () => ({})
    },
    
    // 头部配置
    showHeader: {
      type: Boolean,
      default: true
    },
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    showStats: {
      type: Boolean,
      default: true
    },
    showActions: {
      type: Boolean,
      default: true
    },
    actionButtons: {
      type: Array,
      default: () => []
    },
    
    // 功能配置
    selectable: {
      type: Boolean,
      default: false
    },
    showIndex: {
      type: Boolean,
      default: false
    },
    operations: {
      type: Array,
      default: () => []
    },
    operationWidth: {
      type: [String, Number],
      default: 150
    },
    
    // 分页配置
    showPagination: {
      type: Boolean,
      default: true
    },
    pageSize: {
      type: Number,
      default: 20
    },
    pageSizes: {
      type: Array,
      default: () => [10, 20, 50, 100]
    },
    
    // 行标识
    rowKey: {
      type: [String, Function],
      default: ''
    }
  },
  data() {
    return {
      currentPage: 1,
      currentPageSize: this.pageSize,
      selectedRows: []
    }
  },
  computed: {
    tableData() {
      return this.data || []
    },
    
    totalCount() {
      return this.tableData.length
    },
    
    paginatedData() {
      if (!this.showPagination) return this.tableData
      
      const start = (this.currentPage - 1) * this.currentPageSize
      const end = start + this.currentPageSize
      return this.tableData.slice(start, end)
    }
  },
  watch: {
    pageSize: {
      immediate: true,
      handler(newValue) {
        this.currentPageSize = newValue
      }
    }
  },
  methods: {
    // 事件处理
    handleAction(action, button, index) {
      this.$emit('action', action, button, index)
    },
    
    handleRowOperation(action, button, index) {
      this.$emit('row-operation', action, button, index)
    },
    
    handleSelectionChange(selection) {
      this.selectedRows = selection
      this.$emit('selection-change', selection)
    },
    
    handleSortChange(sort) {
      this.$emit('sort-change', sort)
    },
    
    handleRowClick(row, column, event) {
      this.$emit('row-click', row, column, event)
    },
    
    handleSizeChange(size) {
      this.currentPageSize = size
      this.currentPage = 1
      this.$emit('page-change', { page: this.currentPage, size: this.currentPageSize })
    },
    
    handleCurrentChange(page) {
      this.currentPage = page
      this.$emit('page-change', { page: this.currentPage, size: this.currentPageSize })
    },
    
    // 数据格式化
    getTagType(value, tagMap) {
      if (!tagMap) return 'info'
      return tagMap[value]?.type || 'info'
    },
    
    getTagText(value, tagMap) {
      if (!tagMap) return value
      return tagMap[value]?.text || value
    },
    
    getStatusType(value, statusMap) {
      if (!statusMap) return 'info'
      return statusMap[value]?.type || 'info'
    },
    
    getStatusText(value, statusMap) {
      if (!statusMap) return value
      return statusMap[value]?.text || value
    },
    
    formatDateTime(value) {
      if (!value) return '-'
      return new Date(value).toLocaleString('zh-CN')
    },
    
    formatNumber(value, precision = 2) {
      if (value === null || value === undefined) return '-'
      return Number(value).toFixed(precision)
    },
    
    getRowOperations(row, index) {
      return this.operations.map(op => ({
        ...op,
        action: `${op.action}:${index}`,
        row: row, // Pass the actual row data
        disabled: typeof op.disabled === 'function' ? op.disabled(row) : op.disabled
      }))
    }
  }
}
</script>

<style scoped>
.data-table {
  background: var(--color-bg-primary);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border-light);
  gap: var(--spacing-lg);
}

.table-info {
  flex: 1;
  min-width: 0;
}

.table-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.table-description {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  margin: 0 0 var(--spacing-sm) 0;
  line-height: 1.4;
}

.table-stats {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.table-actions {
  display: flex;
  gap: var(--spacing-sm);
  align-items: flex-start;
  flex-shrink: 0;
}

.table-container {
  overflow: hidden;
}

.table-pagination {
  display: flex;
  justify-content: flex-end;
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border-top: 1px solid var(--color-border-light);
}

.table-operation-btn {
  margin: 0 var(--spacing-xs);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .table-header {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
  }
  
  .table-actions {
    justify-content: flex-start;
  }
  
  .table-pagination {
    justify-content: center;
  }
  
  .table-pagination .el-pagination {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>

<template>
  <div class="json-viewer">
    <!-- 顶部控制栏 -->
    <div v-if="showControls" class="json-controls">
      <div class="json-info">
        <el-tag size="small" type="info">
          <el-icon><Document /></el-icon>
          {{ getDataInfo() }}
        </el-tag>
      </div>
      <div class="json-actions">
        <el-button 
          size="small" 
          type="primary" 
          :icon="DocumentCopy"
          @click="copyJson">
          复制
        </el-button>
        <el-button 
          size="small" 
          type="success" 
          :icon="Download"
          @click="downloadJson">
          下载
        </el-button>
        <el-button 
          v-if="collapsible"
          size="small" 
          type="info"
          @click="toggleCollapse">
          <template #icon>
            <el-icon>
              <component :is="collapsed ? 'ArrowDown' : 'ArrowUp'" />
            </el-icon>
          </template>
          {{ collapsed ? '展开' : '收起' }}
        </el-button>
      </div>
    </div>

    <!-- JSON 内容显示 -->
    <div v-show="!collapsed" class="json-content" :class="{ 'with-controls': showControls }">
      <pre class="json-display" :class="displayClass">{{ formattedJson }}</pre>
    </div>

    <!-- 折叠状态提示 -->
    <div v-if="collapsed" class="collapsed-hint">
      <el-text type="info">
        <el-icon><InfoFilled /></el-icon>
        JSON 数据已折叠，点击展开查看详细内容
      </el-text>
    </div>
  </div>
</template>

<script>
import { DocumentCopy, Download, ArrowDown, ArrowUp, Document, InfoFilled } from '@element-plus/icons-vue'

export default {
  name: 'JsonViewer',
  components: {
    DocumentCopy,
    Download,
    ArrowDown,
    ArrowUp,
    Document,
    InfoFilled
  },
  props: {
    data: {
      type: [Object, Array, String],
      required: true
    },
    title: {
      type: String,
      default: 'JSON数据'
    },
    maxHeight: {
      type: String,
      default: '400px'
    },
    showControls: {
      type: Boolean,
      default: true
    },
    collapsible: {
      type: Boolean,
      default: false
    },
    theme: {
      type: String,
      default: 'light', // 'light', 'dark'
      validator: (value) => ['light', 'dark'].includes(value)
    },
    displayClass: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      collapsed: false
    }
  },
  computed: {
    formattedJson() {
      if (!this.data) return '暂无数据'
      
      try {
        if (typeof this.data === 'string') {
          // 尝试解析字符串为JSON
          const parsed = JSON.parse(this.data)
          return JSON.stringify(parsed, null, 2)
        }
        return JSON.stringify(this.data, null, 2)
      } catch (error) {
        // 如果不是有效的JSON字符串，直接返回
        return typeof this.data === 'string' ? this.data : JSON.stringify(this.data, null, 2)
      }
    }
  },
  methods: {
    getDataInfo() {
      if (!this.data) return '无数据'
      
      try {
        const jsonData = typeof this.data === 'string' ? JSON.parse(this.data) : this.data
        
        if (Array.isArray(jsonData)) {
          return `数组 (${jsonData.length} 项)`
        } else if (typeof jsonData === 'object') {
          const keys = Object.keys(jsonData)
          return `对象 (${keys.length} 个字段)`
        } else {
          return `${typeof jsonData} 类型`
        }
      } catch {
        return '文本数据'
      }
    },

    async copyJson() {
      try {
        const jsonString = this.formattedJson
        
        if (navigator.clipboard) {
          await navigator.clipboard.writeText(jsonString)
          this.$message.success('✅ JSON数据已复制到剪贴板')
        } else {
          // 兼容旧浏览器
          const textArea = document.createElement('textarea')
          textArea.value = jsonString
          document.body.appendChild(textArea)
          textArea.select()
          document.execCommand('copy')
          document.body.removeChild(textArea)
          this.$message.success('✅ JSON数据已复制到剪贴板')
        }
      } catch (error) {
        this.$message.error('❌ 复制失败: ' + error.message)
      }
    },

    downloadJson() {
      try {
        const jsonString = this.formattedJson
        const blob = new Blob([jsonString], { type: 'application/json;charset=utf-8' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0]
        const filename = `${this.title.replace(/[^\w\s-]/g, '')}-${timestamp}.json`
        
        link.href = url
        link.download = filename
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        this.$message.success('📥 JSON文件下载成功')
      } catch (error) {
        this.$message.error('❌ 下载失败: ' + error.message)
      }
    },

    toggleCollapse() {
      this.collapsed = !this.collapsed
      this.$emit('collapse-change', this.collapsed)
    }
  }
}
</script>

<style scoped>
.json-viewer {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #ffffff;
  overflow: hidden;
}

.json-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #e4e7ed;
  flex-wrap: wrap;
  gap: 12px;
}

.json-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.json-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.json-content {
  position: relative;
}

.json-content.with-controls {
  border-top: none;
}

.json-display {
  background: #f8f9fa;
  color: #2c3e50;
  padding: 16px;
  margin: 0;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-x: auto;
  overflow-y: auto;
  max-height: v-bind(maxHeight);
  
  /* 语法高亮效果 */
  background-image: 
    linear-gradient(90deg, transparent 79px, #e4e7ed 79px, #e4e7ed 81px, transparent 81px),
    linear-gradient(#f8f9fa 0px, #f8f9fa 100%);
  background-size: 4ch 1.6em;
  background-position: 0 0;
}

/* 深色主题 */
.json-viewer[data-theme="dark"] .json-display {
  background: #2c3e50;
  color: #ecf0f1;
  border-color: #34495e;
}

.json-viewer[data-theme="dark"] .json-controls {
  background: #34495e;
  border-color: #34495e;
  color: #ecf0f1;
}

.collapsed-hint {
  padding: 24px;
  text-align: center;
  background: #f8f9fa;
  color: #6c757d;
}

/* 滚动条样式 */
.json-display::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.json-display::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.json-display::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.json-display::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .json-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .json-actions {
    justify-content: center;
    width: 100%;
  }
  
  .json-actions .el-button {
    flex: 1;
    max-width: 100px;
  }
  
  .json-display {
    font-size: 11px;
    padding: 12px;
  }
}

/* 打印样式 */
@media print {
  .json-controls {
    display: none;
  }
  
  .json-display {
    max-height: none;
    background: white !important;
    color: black !important;
    border: 1px solid #ccc;
  }
}
</style>

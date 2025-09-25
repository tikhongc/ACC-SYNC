<template>
  <div class="home">
    <!-- 面包屑导航 -->
    <Breadcrumb />
    
    <!-- 页面头部 -->
    <PageHeader
      title="ACC 数据同步后台"
      description="Autodesk Construction Cloud 数据同步管理平台"
      :icon="IconDashboard" />

    <!-- API模块 -->
    <div class="api-modules">
      
      <!-- Forms API 模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>
              <icon-file />
              Forms API
            </span>
            <StatusTag status="info" text="表单数据管理" size="small" :show-icon="false" />
          </div>
        </template>
        
        <!-- 核心功能 -->
        <div class="function-group">
          <h4>核心功能</h4>
          <div class="button-grid">
            <el-button type="primary" @click="handleFormsDataClick">
              <icon-dashboard />
              项目表单数据
            </el-button>
            <el-button type="success" @click="handleFormsTemplatesClick">
              <icon-apps />
              表单模板管理
            </el-button>
          </div>
        </div>

        <!-- 数据导出 -->
        <div class="function-group">
          <h4>数据导出</h4>
          <div class="button-grid">
            <el-button type="warning" @click="handleFormsExportClick">
              <icon-download />
              表单JSON
            </el-button>
            <el-button type="warning" @click="handleTemplatesExportClick">
              <icon-download />
              模板JSON
            </el-button>
          </div>
        </div>

      </el-card>

   

      <!-- Data Connector API 模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>
              <icon-sync />
              Data Connector API
            </span>
            <StatusTag status="warning" text="数据连接器" size="small" :show-icon="false" />
          </div>
        </template>
        
        <!-- 核心功能 -->
        <div class="function-group">
          <h4>核心功能</h4>
          <div class="button-grid">
            <el-button type="primary" @click="$router.push('/data-connector/sync')">
              <icon-sync />
              数据同步管理
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- Reviews API 模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>
              <icon-branch />
              Reviews API
            </span>
            <StatusTag status="success" text="评审与工作流" size="small" :show-icon="false" />
          </div>
        </template>
        
        <!-- 评审管理 -->
        <div class="function-group">
          <h4>评审管理</h4>
          <div class="button-grid">
            <el-button type="primary" @click="handleReviewsDataClick">
              <icon-file />
              项目评审
            </el-button>
            <el-button type="success" @click="handleReviewsWorkflowsClick">
              <icon-branch />
              审批工作流
            </el-button>
          </div>
        </div>

        <!-- 数据导出 -->
        <div class="function-group">
          <h4>数据导出</h4>
          <div class="button-grid">
            <el-button type="warning" @click="handleReviewsExportClick">
              <icon-download />
              评审JSON
            </el-button>
            <el-button type="warning" @click="handleWorkflowsExportClick">
              <icon-download />
              工作流JSON
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- 系统管理模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>
              <icon-settings />
              系统管理
            </span>
            <StatusTag status="success" text="管理工具" size="small" :show-icon="false" />
          </div>
        </template>
        
        <!-- 系统功能 -->
        <div class="function-group">
          <h4>系统功能</h4>
          <div class="button-grid">
            <el-button type="success" @click="$router.push('/account-info')">
              <icon-user />
              账户信息
            </el-button>
            <el-button type="primary" @click="$router.push('/project-info')">
              <icon-folder />
              项目信息
            </el-button>
            <el-button type="info" @click="$router.push('/system/status')">
              <icon-check-circle />
              系统状态
            </el-button>
          </div>
        </div>
      </el-card>

    </div>

    <!-- API响应显示区域 -->
    <el-card v-if="apiResponse" class="response-card">
      <template #header>
        <div class="card-header">
            <span>API响应</span>
          <el-button type="text" @click="clearResponse">清除</el-button>
        </div>
      </template>
      <div class="response-content" v-html="apiResponse"></div>
    </el-card>

    <!-- 项目选择对话框 -->
    <ProjectSelector
      v-model="showProjectSelector"
      :multiple="false"
      :auto-refresh="true"
      @confirm="handleProjectSelected"
      @cancel="handleProjectSelectionCancel" />

  </div>
</template>

<script>
import axios from 'axios'
import Breadcrumb from '../components/Breadcrumb.vue'
import PageHeader from '../components/PageHeader.vue'
import ProjectSelector from '../components/ProjectSelector.vue'
import projectStore from '../utils/projectStore.js'
import { 
  IconDashboard, 
  IconFile, 
  IconSync, 
  IconSettings,
  IconUser,
  IconCheckCircle,
  IconApps,
  IconDownload,
  IconEye,
  IconCode,
  IconSafe,
  IconFolder,
  IconBranch
} from '@arco-design/web-vue/es/icon'

export default {
  name: 'Home',
  components: {
    Breadcrumb,
    PageHeader,
    ProjectSelector,
    IconDashboard,
    IconFile,
    IconSync,
    IconSettings,
    IconUser,
    IconCheckCircle,
    IconApps,
    IconDownload,
    IconEye,
    IconCode,
    IconSafe,
    IconFolder,
    IconBranch
  },
  data() {
    return {
      apiResponse: null,
      showProjectSelector: false,
      pendingApiCall: null, // 存储待执行的API调用
      selectedProject: null
    }
  },
  methods: {
    async checkHealth() {
      try {
        const response = await axios.get('/health')
        this.$message.success('系统运行正常')
        this.apiResponse = `<pre>${JSON.stringify(response.data, null, 2)}</pre>`
      } catch (error) {
        this.$message.error('系统检查失败')
        console.error(error)
      }
    },
    
    
    async callApi(endpoint) {
      try {
        this.$message.info(`正在调用 ${endpoint}...`)
        const response = await axios.get(endpoint)
        
        if (response.headers['content-type']?.includes('text/html')) {
          // 如果返回HTML，在新窗口打开
          window.open(endpoint, '_blank')
        } else {
          // 如果返回JSON，显示在页面上
          this.apiResponse = `
            <div class="api-info">
              <p><strong>端点:</strong> ${endpoint}</p>
              <p><strong>状态:</strong> ${response.status} ${response.statusText}</p>
              <p><strong>响应时间:</strong> ${new Date().toLocaleTimeString()}</p>
            </div>
            <pre>${JSON.stringify(response.data, null, 2)}</pre>
          `
        }
        this.$message.success('API调用成功')
      } catch (error) {
        this.$message.error(`API调用失败: ${error.response?.status || error.message}`)
        this.apiResponse = `
          <div class="error-info">
            <p><strong>错误端点:</strong> ${endpoint}</p>
            <p><strong>错误状态:</strong> ${error.response?.status || 'Network Error'}</p>
            <p><strong>错误信息:</strong> ${error.response?.statusText || error.message}</p>
            <p><strong>时间:</strong> ${new Date().toLocaleTimeString()}</p>
          </div>
          ${error.response?.data ? `<pre>${JSON.stringify(error.response.data, null, 2)}</pre>` : ''}
        `
      }
    },
    
    async downloadApi(endpoint) {
      try {
        this.$message.info(`正在下载 ${endpoint}...`)
        const response = await axios.get(endpoint, {
          responseType: 'blob'
        })
        
        // 创建下载链接
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `${endpoint.split('/').pop()}_${Date.now()}.json`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        this.$message.success('文件下载成功')
      } catch (error) {
        this.$message.error(`下载失败: ${error.response?.status || error.message}`)
      }
    },
    
    clearResponse() {
      this.apiResponse = null
    },

    // Forms数据页面点击处理
    handleFormsDataClick() {
      this.pendingApiCall = {
        type: 'route',
        target: '/forms/jarvis',
        description: '项目表单数据'
      }
      this.showProjectSelector = true
    },

    // Forms模板页面点击处理
    handleFormsTemplatesClick() {
      this.pendingApiCall = {
        type: 'route',
        target: '/forms/templates',
        description: '表单模板管理'
      }
      this.showProjectSelector = true
    },

    // Reviews数据页面点击处理
    handleReviewsDataClick() {
      this.pendingApiCall = {
        type: 'route',
        target: '/reviews/data',
        description: '项目评审'
      }
      this.showProjectSelector = true
    },

    // Reviews工作流页面点击处理
    handleReviewsWorkflowsClick() {
      this.pendingApiCall = {
        type: 'route',
        target: '/reviews/workflows',
        description: '审批工作流'
      }
      this.showProjectSelector = true
    },

    // 处理项目选择确认
    handleProjectSelected(selectedProject) {
      this.selectedProject = selectedProject
      
      // 保存选中的项目到存储
      projectStore.saveSelectedProject(selectedProject)
      
      this.$message.success(`已选择项目: ${selectedProject.name}`)
      
      // 执行待执行的操作
      if (this.pendingApiCall) {
        this.executePendingApiCall()
      }
    },

    // 处理项目选择取消
    handleProjectSelectionCancel() {
      this.pendingApiCall = null
    },

    // 执行待执行的API调用
    executePendingApiCall() {
      if (!this.pendingApiCall || !this.selectedProject) {
        return
      }

      const { type, target, description } = this.pendingApiCall
      
      console.log(`执行${description}，选中项目:`, this.selectedProject.name, this.selectedProject.id)
      
      if (type === 'route') {
        // 路由跳转，携带项目信息
        this.$router.push({
          path: target,
          query: {
            projectId: this.selectedProject.id,
            projectName: this.selectedProject.name
          }
        })
      } else if (type === 'api') {
        // API调用
        this.callApiWithProject(target)
      } else if (type === 'download') {
        // 文件下载
        this.downloadApiWithProject(target)
      }
      
      // 清除待执行的调用
      this.pendingApiCall = null
    },

    // 带项目信息的API调用
    async callApiWithProject(endpoint) {
      if (!this.selectedProject) {
        this.$message.error('未选择项目')
        return
      }

      try {
        this.$message.info(`正在调用 ${endpoint} (项目: ${this.selectedProject.name})...`)
        const response = await axios.get(endpoint, {
          params: {
            projectId: this.selectedProject.id
          }
        })
        
        if (response.headers['content-type']?.includes('text/html')) {
          // 如果返回HTML，在新窗口打开
          window.open(`${endpoint}?projectId=${this.selectedProject.id}`, '_blank')
        } else {
          // 如果返回JSON，显示在页面上
          this.apiResponse = `
            <div class="api-info">
              <p><strong>端点:</strong> ${endpoint}</p>
              <p><strong>项目:</strong> ${this.selectedProject.name} (${this.selectedProject.id})</p>
              <p><strong>状态:</strong> ${response.status} ${response.statusText}</p>
              <p><strong>响应时间:</strong> ${new Date().toLocaleTimeString()}</p>
            </div>
            <pre>${JSON.stringify(response.data, null, 2)}</pre>
          `
        }
        this.$message.success('API调用成功')
      } catch (error) {
        this.$message.error(`API调用失败: ${error.response?.status || error.message}`)
        this.apiResponse = `
          <div class="error-info">
            <p><strong>错误端点:</strong> ${endpoint}</p>
            <p><strong>项目:</strong> ${this.selectedProject.name} (${this.selectedProject.id})</p>
            <p><strong>错误状态:</strong> ${error.response?.status || 'Network Error'}</p>
            <p><strong>错误信息:</strong> ${error.response?.statusText || error.message}</p>
            <p><strong>时间:</strong> ${new Date().toLocaleTimeString()}</p>
          </div>
          ${error.response?.data ? `<pre>${JSON.stringify(error.response.data, null, 2)}</pre>` : ''}
        `
      }
    },

    // 带项目信息的文件下载
    async downloadApiWithProject(endpoint) {
      if (!this.selectedProject) {
        this.$message.error('未选择项目')
        return
      }

      try {
        this.$message.info(`正在下载 ${endpoint} (项目: ${this.selectedProject.name})...`)
        
        // 先尝试作为JSON获取数据
        let response
        let isJsonResponse = false
        
        try {
          response = await axios.get(endpoint, {
            params: {
              projectId: this.selectedProject.id
            }
          })
          isJsonResponse = true
        } catch (jsonError) {
          // 如果JSON请求失败，尝试作为blob下载
          response = await axios.get(endpoint, {
            responseType: 'blob',
            params: {
              projectId: this.selectedProject.id
            }
          })
          isJsonResponse = false
        }
        
        let blob
        if (isJsonResponse) {
          // 将JSON响应转换为blob
          const jsonString = JSON.stringify(response.data, null, 2)
          blob = new Blob([jsonString], { type: 'application/json' })
        } else {
          // 直接使用blob响应
          blob = new Blob([response.data])
        }
        
        // 创建下载链接
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        
        // 生成文件名，包含项目信息
        const projectName = this.selectedProject.name.replace(/[^a-zA-Z0-9]/g, '_')
        const endpointName = endpoint.split('/').pop()
        const fileName = `${endpointName}_${projectName}_${Date.now()}.json`
        link.setAttribute('download', fileName)
        
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        this.$message.success(`文件下载成功: ${fileName}`)
      } catch (error) {
        console.error('下载失败:', error)
        this.$message.error(`下载失败: ${error.response?.status || error.message}`)
      }
    },

    // Forms导出点击处理
    handleFormsExportClick() {
      this.pendingApiCall = {
        type: 'download',
        target: '/api/forms/export-json',
        description: '表单JSON导出'
      }
      this.showProjectSelector = true
    },

    // Templates导出点击处理
    handleTemplatesExportClick() {
      this.pendingApiCall = {
        type: 'download',
        target: '/api/forms/templates/export-json',
        description: '模板JSON导出'
      }
      this.showProjectSelector = true
    },

    // Reviews导出点击处理
    handleReviewsExportClick() {
      this.pendingApiCall = {
        type: 'download',
        target: '/api/reviews/jarvis',
        description: '评审JSON导出'
      }
      this.showProjectSelector = true
    },

    // Workflows导出点击处理
    handleWorkflowsExportClick() {
      this.pendingApiCall = {
        type: 'download',
        target: '/api/reviews/workflows/jarvis',
        description: '工作流JSON导出'
      }
      this.showProjectSelector = true
    }
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.home {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}


.api-modules {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--spacing-xxl);
  margin-bottom: 32px;
}

.module-card {
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: var(--color-bg-primary);
  overflow: hidden;
  position: relative;
}

.module-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-success) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.module-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
  border-color: var(--color-primary);
}

.module-card:hover::before {
  opacity: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 1.2em;
  padding: var(--spacing-lg) var(--spacing-xl);
  background: linear-gradient(135deg, var(--color-bg-secondary) 0%, var(--color-bg-tertiary) 100%);
  border-bottom: 1px solid var(--color-border-lighter);
}

.card-header span {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--color-text-primary);
}

.function-group {
  margin-bottom: var(--spacing-xl);
  padding: 0 var(--spacing-xl);
}

.function-group:last-child {
  margin-bottom: var(--spacing-lg);
}

.function-group h4 {
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
  font-size: 0.95em;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: relative;
  padding-left: var(--spacing-md);
}

.function-group h4::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 14px;
  background: var(--color-primary);
  border-radius: 2px;
}

.button-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

/* 系统管理模块特殊布局 */
.module-card:last-child .button-grid {
  grid-template-columns: 1fr;
  gap: var(--spacing-md);
}

.button-grid .el-button {
  width: 100%;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--border-radius-lg);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.button-grid .el-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.button-grid .el-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.button-grid .el-button:hover::before {
  left: 100%;
}

.button-grid .el-button:active {
  transform: translateY(-1px);
}

.response-card {
  margin-top: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.response-content {
  max-height: 500px;
  overflow-y: auto;
}

.response-content pre {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.5;
}

.api-info {
  background: #e8f5e8;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 10px;
  border-left: 4px solid #67c23a;
}

.error-info {
  background: #fef0f0;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 10px;
  border-left: 4px solid #f56c6c;
}

.api-info p, .error-info p {
  margin: 5px 0;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .api-modules {
    grid-template-columns: 1fr;
  }
  
  .button-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions .el-button {
    margin: 5px;
    width: calc(100% - 10px);
  }
}
</style>

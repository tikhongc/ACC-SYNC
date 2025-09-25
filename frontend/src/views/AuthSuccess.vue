<template>
  <div class="auth-success">
    <!-- 成功提示 -->
    <el-card class="success-card">
      <div class="success-content">
        <el-icon class="success-icon" size="48px">
          <CircleCheck />
        </el-icon>
        <h2>认证成功！</h2>
        <p>{{ saveStatus }}</p>
        <p v-if="countdown > 0" class="countdown">{{ countdown }} 秒后自动跳转到主页...</p>
      </div>
    </el-card>

    <!-- API模块 -->
    <div class="api-modules">
      
      <!-- Forms API 模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>📋 Forms API</span>
          </div>
        </template>
        
        <div class="button-group">
          <el-button type="primary" @click="navigateToApi('/api/forms/jarvis')">
            📊 项目表单数据
          </el-button>
          <el-button type="success" @click="navigateToApi('/api/forms/templates')">
            🏗️ 表单模板
          </el-button>
          <el-button type="warning" @click="downloadApi('/api/forms/export-json')">
            📄 导出表单JSON
          </el-button>
          <el-button type="warning" @click="downloadApi('/api/forms/templates/export-json')">
            📋 导出模板JSON
          </el-button>
        </div>
      </el-card>

  

      <!-- 账户管理模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>🔐 账户管理</span>
          </div>
        </template>
        
        <div class="button-group">
          <el-button type="success" @click="navigateToApi('/api/auth/account-info')">
            👤 账户详情
          </el-button>
          <el-button type="primary" @click="navigateToApi('/api/auth/token-status')">
            🔐 Token状态
          </el-button>
        </div>
      </el-card>

    </div>

    <!-- Token详情 -->
    <el-card class="token-card" v-if="tokenDetails">
      <template #header>
        <span>📄 Token详细信息</span>
      </template>
      <pre class="token-details">{{ tokenDetails }}</pre>
    </el-card>

    <!-- 底部导航 -->
    <div class="bottom-nav">
      <el-button type="primary" @click="goToMainPage">🏠 进入主页面</el-button>
      <el-button type="success" @click="checkHealth">💚 系统状态</el-button>
    </div>

  </div>
</template>

<script>
import { CircleCheck } from '@element-plus/icons-vue'
import axios from 'axios'
import projectStore from '../utils/projectStore.js'

export default {
  name: 'AuthSuccess',
  components: {
    CircleCheck
  },
  data() {
    return {
      saveStatus: '✅ Token 已保存到会话',
      tokenDetails: null,
      countdown: 5,
      projectsLoading: false,
      projectsLoaded: false
    }
  },
  mounted() {
    // 从URL参数或其他方式获取token详情
    this.loadTokenDetails()
    
    // 监听OAuth回调的postMessage
    this.setupOAuthMessageListener()
    
    // 预加载项目信息
    this.preloadProjects()
    
    // 5秒后自动跳转到主页
    setTimeout(() => {
      this.goToMainPage()
    }, 5000)
    
    // 显示倒计时提示
    this.showCountdown()
  },
  methods: {
    loadTokenDetails() {
      // 这里可以从URL参数或API获取token详情
      const urlParams = new URLSearchParams(window.location.search)
      const details = urlParams.get('details')
      if (details) {
        try {
          this.tokenDetails = JSON.parse(decodeURIComponent(details))
        } catch (e) {
          console.log('No token details available')
        }
      }
    },
    
    setupOAuthMessageListener() {
      // 监听来自OAuth回调窗口的消息
      window.addEventListener('message', (event) => {
        if (event.origin !== window.location.origin) {
          return // 只接受同源消息
        }
        
        if (event.data.type === 'oauth_success') {
          this.saveStatus = '✅ OAuth认证成功！Token已保存'
          this.$message.success('认证成功！')
        } else if (event.data.type === 'oauth_error') {
          this.saveStatus = `❌ OAuth认证失败: ${event.data.error_description}`
          this.$message.error(`认证失败: ${event.data.error_description}`)
        }
      })
    },
    
    navigateToApi(endpoint) {
      window.open(endpoint, '_blank')
    },
    
    async downloadApi(endpoint) {
      try {
        this.$message.info(`正在下载 ${endpoint}...`)
        const response = await axios.get(endpoint, {
          responseType: 'blob'
        })
        
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
    
    showCountdown() {
      const timer = setInterval(() => {
        this.countdown--
        if (this.countdown <= 0) {
          clearInterval(timer)
        }
      }, 1000)
    },
    
    goToMainPage() {
      // 强制刷新认证状态
      this.$router.push({ path: '/', query: { forceAuthCheck: 'true' } })
    },
    
    async checkHealth() {
      try {
        const response = await axios.get('/health')
        this.$message.success('系统运行正常')
      } catch (error) {
        this.$message.error('系统检查失败')
      }
    },

    // 预加载项目信息
    async preloadProjects() {
      this.projectsLoading = true
      this.saveStatus = '🔄 正在预加载项目信息...'
      
      try {
        console.log('开始预加载项目信息...')
        
        // 使用项目存储工具获取项目信息
        const projectData = await projectStore.getProjectsWithCache(false)
        
        if (projectData && projectData.projects?.list?.length > 0) {
          this.projectsLoaded = true
          this.saveStatus = `✅ Token已保存，项目信息已缓存 (${projectData.projects.list.length}个项目)`
          
          console.log('项目信息预加载成功:', projectData.projects.list.length, '个项目')
          this.$message.success(`项目信息已缓存 (${projectData.projects.list.length}个项目)`)
        } else {
          throw new Error('未获取到项目数据')
        }
        
      } catch (error) {
        console.error('预加载项目信息失败:', error)
        this.saveStatus = `⚠️ Token已保存，但项目信息预加载失败: ${error.message}`
        this.$message.warning('项目信息预加载失败，可在使用时手动刷新')
      } finally {
        this.projectsLoading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-success {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.success-card {
  margin-bottom: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.success-content {
  text-align: center;
  padding: 20px;
}

.success-icon {
  color: #67c23a;
  margin-bottom: 15px;
}

.success-content h2 {
  color: #2c3e50;
  margin: 15px 0 10px 0;
}

.success-content p {
  color: #7f8c8d;
  font-size: 1.1em;
}

.countdown {
  color: #409eff !important;
  font-weight: 600;
  margin-top: 15px;
}

.api-modules {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.module-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.card-header {
  font-weight: 600;
  font-size: 1.1em;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.button-group .el-button {
  width: 100%;
  justify-content: flex-start;
}

.token-card {
  margin-bottom: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.token-details {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.5;
  max-height: 200px;
  overflow-y: auto;
}

.bottom-nav {
  text-align: center;
}

.bottom-nav .el-button {
  margin: 0 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .api-modules {
    grid-template-columns: 1fr;
  }
  
  .bottom-nav .el-button {
    margin: 5px;
    width: calc(50% - 10px);
  }
}
</style>

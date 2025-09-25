<template>
  <div id="app">
    <router-view />
    <!-- Token状态监控组件 -->
    <TokenStatus 
      v-if="showTokenStatus" 
      @token-refreshed="handleTokenRefreshed"
      @logged-out="handleLoggedOut" />
    <!-- 全局监测面板 -->
    <GlobalMonitoringPanel v-if="showTokenStatus" />
  </div>
</template>

<script>
import TokenStatus from './components/TokenStatus.vue'
import GlobalMonitoringPanel from './components/GlobalMonitoringPanel.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    TokenStatus,
    GlobalMonitoringPanel
  },
  data() {
    return {
      showTokenStatus: false,
      projectsCache: {},
      projectsCacheLoaded: false
    }
  },
  async mounted() {
    // 检查是否已认证，如果已认证则显示Token状态组件
    await this.checkAuthStatus()
    
    // 监听路由变化，在认证相关页面更新后重新检查状态
    this.$router.afterEach((to, from) => {
      if (from.path === '/auth/success' || to.query.forceAuthCheck === 'true') {
        setTimeout(() => {
          this.checkAuthStatus()
        }, 1000) // 延迟1秒检查，确保token已保存
      }
    })
  },
  methods: {
    async checkAuthStatus() {
      try {
        console.log('🔐 检查认证状态...')
        const response = await axios.get('/api/auth/check')
        console.log('🔐 认证检查响应:', response.data)
        
        this.showTokenStatus = response.data.authenticated
        
        // 如果认证成功，自动获取项目信息和账户信息
        if (response.data.authenticated) {
          console.log('✅ 用户已认证，开始加载用户数据')
          await this.loadUserDataAfterAuth()
        } else {
          console.log('❌ 用户未认证')
        }
      } catch (error) {
        console.error('❌ 认证状态检查失败:', error)
        this.showTokenStatus = false
      }
    },

    // 认证成功后自动加载用户数据
    async loadUserDataAfterAuth() {
      try {
        console.log('🔄 认证成功，开始加载用户数据...')
        
        // 并行加载账户信息和项目信息
        const promises = [
          this.loadAccountInfo(),
          this.loadProjectsInfo()
        ]
        
        await Promise.allSettled(promises)
        console.log('✅ 用户数据加载完成')
        
        // 显示成功消息
        if (this.$message) {
          this.$message.success(`🎉 自动加载完成！账户信息和 ${Object.keys(this.projectsCache).length} 个项目已缓存`)
        }
        
        // 通知监测中心项目信息已更新
        console.log('🔄 准备通知监测中心项目缓存更新...')
        if (this.$eventBus) {
          console.log('📡 发送项目缓存更新事件')
          this.$eventBus.emit('projects-cache-updated', this.projectsCache)
        } else {
          console.error('❌ 事件总线未初始化')
        }
        
      } catch (error) {
        console.error('❌ 加载用户数据失败:', error)
      }
    },

    // 加载账户信息
    async loadAccountInfo() {
      try {
        console.log('📋 正在获取账户信息...')
        const response = await axios.get('/api/auth/account-info')
        console.log('📋 账户信息API响应:', response.data)
        
        if (response.data && response.data.status === 'success' && response.data.user) {
          const user = response.data.user
          console.log(`👤 账户信息已加载: ${user.userName}`)
          
          // 保存账户信息到localStorage
          const accountInfo = {
            userName: user.userName,
            emailId: user.emailId,
            userId: user.userId,
            firstName: user.firstName,
            lastName: user.lastName,
            loadedAt: new Date().toISOString()
          }
          localStorage.setItem('acc_account_info', JSON.stringify(accountInfo))
          console.log('💾 账户信息已保存到localStorage')
        } else {
          console.warn('⚠️ 账户信息响应格式异常:', response.data)
        }
      } catch (error) {
        console.error('❌ 获取账户信息失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
      }
    },

    // 加载项目信息
    async loadProjectsInfo() {
      try {
        console.log('📋 正在获取项目信息...')
        const response = await axios.get('/api/data-connector/get-projects')
        console.log('📋 项目信息API响应:', response.data)
        
         if (response.data.status === 'success') {
           const projectsData = response.data.projects
           let projects = []
           
           // 处理不同的数据格式
           if (Array.isArray(projectsData)) {
             projects = projectsData
           } else if (projectsData && typeof projectsData === 'object') {
             // 检查是否有list字段（ACC API的标准格式）
             if (projectsData.list && Array.isArray(projectsData.list)) {
               projects = projectsData.list
             } else if (projectsData.results && Array.isArray(projectsData.results)) {
               projects = projectsData.results
             } else {
               projects = Object.values(projectsData)
             }
           }
          
          // 构建项目ID到名称的映射
          this.projectsCache = {}
          
          projects.forEach((project) => {
            if (project && project.id && project.name) {
              this.projectsCache[project.id] = project.name
            }
          })
          
          // 保存到localStorage，带时间戳
          const cacheData = {
            projects: this.projectsCache,
            timestamp: new Date().toISOString()
          }
          localStorage.setItem('global_monitoring_projects_cache', JSON.stringify(cacheData))
          this.projectsCacheLoaded = true
          console.log(`✅ 项目信息加载完成: ${projects.length} 个项目已缓存`)
        } else {
          console.warn('⚠️ 项目信息API响应状态异常:', response.data)
        }
      } catch (error) {
        console.error('❌ 获取项目信息失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
      }
    },

    handleTokenRefreshed() {
      console.log('Token已刷新')
      // 可以在这里执行一些刷新后的操作
    },

    handleLoggedOut() {
      this.showTokenStatus = false
      console.log('用户已登出')
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}
</style>


<template>
  <div class="account-info">
    <!-- 面包屑导航 -->
    <Breadcrumb />
    
    <!-- 页面头部 -->
    <PageHeader
      title="账户信息"
      description="查看和管理 Autodesk Construction Cloud 账户信息"
      :icon="IconUser"
      :action-buttons="headerButtons"
      @action="handleHeaderAction" />

    <!-- 加载状态 -->
    <LoadingState 
      v-if="loading"
      type="card"
      title="正在获取账户信息"
      text="请稍候，正在从服务器获取最新的账户信息..."
      :show-progress="false"
      :show-cancel="false" />

    <!-- 错误状态 -->
    <ErrorState
      v-if="error"
      type="card"
      severity="error"
      title="获取账户信息失败"
      :message="error"
      :suggestions="errorSuggestions"
      :action-buttons="errorButtons"
      @action="handleErrorAction" />

    <!-- 成功状态指示器 -->
    <StatusIndicator
      v-if="accountData && !loading && !error"
      status="success"
      title="账户信息获取成功！"
      :description="`用户: ${getFullName()}`"
      :details="`Hub: ${accountData.hub?.hubName || 'N/A'}`"
      size="default"
      style="margin-bottom: 24px;" />

    <!-- 账户信息内容 -->
    <div v-if="accountData && !loading && !error">

      <!-- 用户基本信息 -->
      <el-card class="info-card" style="margin-bottom: 20px;">
        <template #header>
          <span>用户基本信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户ID">{{ accountData.user?.userId || 'N/A' }}</el-descriptions-item>
          <el-descriptions-item label="用户名">{{ accountData.user?.userName || 'N/A' }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ accountData.user?.emailId || 'N/A' }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ getFullName() }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- ACC 账户信息 -->
      <el-card class="info-card" style="margin-bottom: 20px;">
        <template #header>
          <span>ACC 账户信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="Hub ID">{{ accountData.hub?.hubId || 'N/A' }}</el-descriptions-item>
          <el-descriptions-item label="Hub 名称">{{ accountData.hub?.hubName || 'N/A' }}</el-descriptions-item>
          <el-descriptions-item label="真实 Account ID">{{ accountData.hub?.realAccountId || 'N/A' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
        <el-button type="success" @click="$router.push('/forms/jarvis')">查看表单数据</el-button>
        <el-button @click="refreshData">刷新数据</el-button>
      </div>

      <!-- 详细数据 -->
      <el-collapse style="margin-top: 20px;">
        <el-collapse-item title="用户信息详情" name="user">
          <pre class="json-display">{{ JSON.stringify(accountData.user, null, 2) }}</pre>
        </el-collapse-item>
        <el-collapse-item title="项目信息详情" name="projects">
          <pre class="json-display">{{ JSON.stringify(accountData.projects, null, 2) }}</pre>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Breadcrumb from '../components/Breadcrumb.vue'
import PageHeader from '../components/PageHeader.vue'
import LoadingState from '../components/LoadingState.vue'
import ErrorState from '../components/ErrorState.vue'
import StatusIndicator from '../components/StatusIndicator.vue'
import { IconUser, IconArrowLeft } from '@arco-design/web-vue/es/icon'
import { Refresh } from '@element-plus/icons-vue'

export default {
  name: 'AccountInfo',
  components: {
    Breadcrumb,
    PageHeader,
    LoadingState,
    ErrorState,
    StatusIndicator,
    IconUser,
    IconArrowLeft
  },
  data() {
    return {
      loading: false,
      error: null,
      accountData: null
    }
  },
  computed: {
    headerButtons() {
      return [
        {
          text: '返回首页',
          type: 'default',
          icon: 'ArrowLeft',
          action: 'home'
        },
        {
          text: '刷新数据',
          type: 'primary',
          icon: Refresh,
          loading: this.loading,
          action: 'refresh'
        }
      ]
    },
    
    errorSuggestions() {
      return [
        '检查网络连接是否正常',
        '确认已完成 Autodesk 认证',
        '验证 Token 是否有效',
        '联系管理员检查 API 配置'
      ]
    },
    
    errorButtons() {
      return [
        {
          text: '重新认证',
          type: 'primary',
          action: 'auth'
        },
        {
          text: '重试',
          type: 'default',
          action: 'retry'
        }
      ]
    }
  },
  mounted() {
    this.fetchAccountInfo()
  },
  methods: {
    async fetchAccountInfo() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/auth/account-info')
        
        // 检查响应类型
        if (response.headers['content-type']?.includes('application/json')) {
          this.accountData = response.data
        } else {
          // 如果返回HTML，说明需要重新认证
          throw new Error('需要重新认证')
        }
      } catch (error) {
        console.error('获取账户信息失败:', error)
        if (error.response?.status === 401) {
          this.error = '未找到 Access Token，请先进行认证'
        } else {
          this.error = `获取账户信息时发生错误: ${error.response?.data?.message || error.message}`
        }
      } finally {
        this.loading = false
      }
    },
    
    getFullName() {
      const user = this.accountData?.user
      if (!user) return 'N/A'
      const firstName = user.firstName || ''
      const lastName = user.lastName || ''
      return `${firstName} ${lastName}`.trim() || 'N/A'
    },
    
    startAuth() {
      window.location.href = '/auth/start'
    },

    handleHeaderAction(action) {
      switch (action) {
        case 'home':
          this.$router.push('/')
          break
        case 'refresh':
          this.fetchAccountInfo()
          break
      }
    },
    
    refreshData() {
      this.fetchAccountInfo()
    },
    
    handleErrorAction(action) {
      switch(action) {
        case 'auth':
          this.startAuth()
          break
        case 'retry':
          this.fetchAccountInfo()
          break
      }
    }
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.account-info {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}


.loading-container {
  height: 200px;
  position: relative;
}

.info-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.action-buttons {
  text-align: center;
  margin: 20px 0;
}

.action-buttons .el-button {
  margin: 0 10px;
}

.json-display {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.5;
  max-height: 400px;
  overflow-y: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .account-info {
    padding: 10px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .action-buttons .el-button {
    margin: 5px;
    width: calc(100% - 10px);
  }
}
</style>

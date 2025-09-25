<template>
  <div class="token-status-widget">
    <!-- Token状态指示器 -->
    <div class="token-indicator" :class="statusClass" @click="showDetails = !showDetails">
      <div class="status-dot" :class="statusClass"></div>
      <span class="status-text">{{ statusText }}</span>
      <span class="expires-text" v-if="tokenInfo.expires_in_minutes">
        ({{ formatExpiresIn(tokenInfo.expires_in_minutes) }})
      </span>
      <icon-down v-if="!showDetails" />
      <icon-up v-if="showDetails" />
    </div>

    <!-- 详细信息面板 -->
    <div class="token-details" v-if="showDetails">
      <div class="detail-row">
        <span class="label">Access Token:</span>
        <span class="value">{{ tokenInfo.has_access_token ? '✅ 有效' : '❌ 无效' }}</span>
      </div>
      <div class="detail-row">
        <span class="label">Refresh Token:</span>
        <span class="value">{{ tokenInfo.has_refresh_token ? '✅ 可用' : '❌ 不可用' }}</span>
      </div>
      <div class="detail-row" v-if="tokenInfo.expires_at">
        <span class="label">过期时间:</span>
        <span class="value">{{ formatDate(tokenInfo.expires_at) }}</span>
      </div>
      <div class="detail-row" v-if="tokenInfo.updated_at">
        <span class="label">更新时间:</span>
        <span class="value">{{ formatDate(tokenInfo.updated_at) }}</span>
      </div>
      <div class="detail-row" v-if="tokenInfo.refresh_attempts > 0">
        <span class="label">刷新尝试:</span>
        <span class="value">{{ tokenInfo.refresh_attempts }} 次</span>
      </div>
      <div class="detail-row" v-if="tokenInfo.next_auto_refresh_at">
        <span class="label">下次自动刷新:</span>
        <span class="value">{{ formatDate(tokenInfo.next_auto_refresh_at) }}</span>
      </div>
      <div class="detail-row" v-if="tokenInfo.next_auto_refresh_in_minutes !== null && tokenInfo.next_auto_refresh_in_minutes >= 0">
        <span class="label">距离下次刷新:</span>
        <span class="value" :class="getRefreshTimeClass(tokenInfo.next_auto_refresh_in_minutes)">
          {{ formatRefreshTime(tokenInfo.next_auto_refresh_in_minutes, tokenInfo.next_auto_refresh_in_seconds) }}
        </span>
      </div>

      <!-- 操作按钮 -->
      <div class="token-actions">
        <el-button 
          size="small" 
          type="primary" 
          @click="refreshToken"
          :loading="refreshing"
          :disabled="!tokenInfo.has_refresh_token">
          <icon-refresh />
          手动刷新
        </el-button>
        <el-button 
          size="small" 
          type="danger" 
          @click="logout"
          :loading="loggingOut">
          <icon-logout />
          登出
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { IconDown, IconUp, IconRefresh, IconExport } from '@arco-design/web-vue/es/icon'

export default {
  name: 'TokenStatus',
  components: {
    IconDown,
    IconUp,
    IconRefresh,
    IconExport
  },
  data() {
    return {
      tokenInfo: {},
      showDetails: false,
      refreshing: false,
      loggingOut: false,
      updateTimer: null
    }
  },
  computed: {
    statusClass() {
      if (!this.tokenInfo.is_valid) return 'invalid'
      if (this.tokenInfo.needs_refresh) return 'warning'
      return 'valid'
    },
    statusText() {
      if (!this.tokenInfo.is_valid) return 'Token无效'
      if (this.tokenInfo.needs_refresh) return 'Token即将过期'
      return 'Token正常'
    }
  },
  mounted() {
    this.loadTokenInfo()
    // 每30秒更新一次token状态
    this.updateTimer = setInterval(() => {
      this.loadTokenInfo()
    }, 30000)
  },
  beforeUnmount() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer)
    }
  },
  methods: {
    async loadTokenInfo() {
      try {
        const response = await axios.get('/api/auth/token-info')
        this.tokenInfo = response.data.token_info || {}
      } catch (error) {
        console.error('获取Token信息失败:', error)
        this.tokenInfo = { is_valid: false }
      }
    },

    async refreshToken() {
      this.refreshing = true
      try {
        const response = await axios.post('/api/auth/refresh-token')
        
        if (response.data.status === 'success') {
          this.$message.success(response.data.message)
          this.tokenInfo = response.data.token_info || {}
          this.$emit('token-refreshed')
        } else {
          throw new Error(response.data.message || 'Token刷新失败')
        }
      } catch (error) {
        console.error('刷新Token失败:', error)
        this.$message.error('刷新Token失败: ' + (error.response?.data?.message || error.message))
      } finally {
        this.refreshing = false
      }
    },

    async logout() {
      this.$confirm('确定要登出吗？这将清除所有Token。', '确认登出', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        this.loggingOut = true
        try {
          await axios.post('/api/auth/logout')
          this.$message.success('已成功登出')
          this.tokenInfo = { is_valid: false }
          this.$emit('logged-out')
          
          // 刷新页面或重定向到登录页
          setTimeout(() => {
            window.location.reload()
          }, 1000)
        } catch (error) {
          console.error('登出失败:', error)
          this.$message.error('登出失败: ' + (error.response?.data?.message || error.message))
        } finally {
          this.loggingOut = false
        }
      }).catch(() => {
        // 用户取消登出
      })
    },

    formatDate(dateString) {
      if (!dateString) return '-'
      try {
        return new Date(dateString).toLocaleString('zh-CN')
      } catch (e) {
        return dateString
      }
    },

    formatExpiresIn(minutes) {
      if (minutes < 60) {
        return `${minutes}分钟后过期`
      } else if (minutes < 1440) { // 24小时
        return `${Math.floor(minutes / 60)}小时后过期`
      } else {
        return `${Math.floor(minutes / 1440)}天后过期`
      }
    },

    formatRefreshTime(minutes, seconds) {
      if (minutes === null || minutes === undefined) {
        return '-'
      }
      
      if (minutes < 0) {
        return '即将刷新'
      } else if (minutes === 0) {
        return `${seconds || 0}秒`
      } else if (minutes < 60) {
        return `${minutes}分钟`
      } else if (minutes < 1440) { // 24小时
        return `${Math.floor(minutes / 60)}小时${minutes % 60}分钟`
      } else {
        return `${Math.floor(minutes / 1440)}天`
      }
    },

    getRefreshTimeClass(minutes) {
      if (minutes === null || minutes === undefined) return ''
      if (minutes <= 5) return 'refresh-urgent'
      if (minutes <= 15) return 'refresh-warning'
      return 'refresh-normal'
    }
  }
}
</script>

<style scoped>
.token-status-widget {
  position: fixed;
  top: 20px;
  right: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  min-width: 200px;
}

.token-indicator {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.token-indicator:hover {
  background-color: #f5f5f5;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}

.status-dot.valid {
  background-color: #52c41a;
}

.status-dot.warning {
  background-color: #faad14;
}

.status-dot.invalid {
  background-color: #f5222d;
}

.status-text {
  font-size: 14px;
  font-weight: 500;
  margin-right: 8px;
}

.expires-text {
  font-size: 12px;
  color: #666;
  margin-right: 8px;
}

.token-details {
  border-top: 1px solid #f0f0f0;
  padding: 12px;
  background-color: #fafafa;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.label {
  color: #666;
  font-weight: 500;
}

.value {
  color: #333;
}

/* 刷新时间状态样式 */
.refresh-normal {
  color: #52c41a;
}

.refresh-warning {
  color: #faad14;
}

.refresh-urgent {
  color: #ff4d4f;
  font-weight: 700;
}

.token-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.token-actions .el-button {
  flex: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .token-status-widget {
    position: static;
    margin: 10px;
    width: auto;
  }
}
</style>

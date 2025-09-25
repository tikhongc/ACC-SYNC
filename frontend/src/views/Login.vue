<template>
  <div class="login">
    <div class="login-container">
      <div class="login-header">
        <h1>ACC 同步 PoC</h1>
        <p>请先登录以继续使用系统</p>
      </div>

      <div class="login-content">
        <div class="feature-list">
          <h3>系统功能</h3>
          <ul>
            <li>🔐 OAuth 2.0 安全认证</li>
            <li>📋 ACC Forms API 集成</li>
            <li>🔄 Data Connector 批量同步</li>
            <li>📊 表单数据导出分析</li>
          </ul>
        </div>

        <div class="login-actions">
          <el-button type="primary" size="large" @click="startAuth" :loading="loading">
            <i class="el-icon-user"></i>
            开始 Autodesk 认证
          </el-button>
          
          <div class="auth-info">
            <p>点击上方按钮将跳转到 Autodesk 官方认证页面</p>
            <p>认证成功后将自动返回到系统主页</p>
          </div>
        </div>
      </div>

      <div class="system-status">
        <el-button type="text" @click="checkHealth" :loading="healthLoading">
          <i class="el-icon-monitor"></i>
          系统状态检查
        </el-button>
        <span v-if="healthStatus" :class="healthStatus.class">{{ healthStatus.message }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      loading: false,
      healthLoading: false,
      healthStatus: null
    }
  },
  mounted() {
    console.log('Login page mounted')
  },
  methods: {

    async startAuth() {
      this.loading = true
      try {
        // 跳转到Flask后端的认证端点
        window.location.href = '/auth/start'
      } catch (error) {
        this.$message.error('认证启动失败')
        this.loading = false
      }
    },

    async checkHealth() {
      this.healthLoading = true
      try {
        const response = await axios.get('/health')
        this.healthStatus = {
          message: '✅ 系统运行正常',
          class: 'status-success'
        }
        this.$message.success('系统运行正常')
      } catch (error) {
        this.healthStatus = {
          message: '❌ 系统连接失败',
          class: 'status-error'
        }
        this.$message.error('系统检查失败')
      } finally {
        this.healthLoading = false
      }
    }
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  padding: 40px;
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.login-header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2em;
}

.login-header p {
  color: #7f8c8d;
  margin-bottom: 30px;
  font-size: 1.1em;
}

.login-content {
  margin-bottom: 30px;
}

.feature-list {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
  text-align: left;
}

.feature-list h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  text-align: center;
}

.feature-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  padding: 8px 0;
  color: #5a6c7d;
  font-size: 1em;
}

.login-actions {
  text-align: center;
}

.login-actions .el-button {
  width: 280px;
  height: 50px;
  font-size: 16px;
  margin-bottom: 20px;
}

.auth-info {
  background: #e8f4f8;
  border-radius: 8px;
  padding: 15px;
  border-left: 4px solid #409eff;
}

.auth-info p {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}

.system-status {
  border-top: 1px solid #ebeef5;
  padding-top: 20px;
  text-align: center;
}

.status-success {
  color: #67c23a;
  margin-left: 10px;
}

.status-error {
  color: #f56c6c;
  margin-left: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    padding: 30px 20px;
    margin: 10px;
  }
  
  .login-header h1 {
    font-size: 1.5em;
  }
  
  .login-actions .el-button {
    width: 100%;
  }
}
</style>

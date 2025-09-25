<template>
  <div class="system-status">
    <!-- 面包屑导航 -->
    <Breadcrumb />
    
    <!-- 页面头部 -->
    <PageHeader
      title="系统状态"
      description="ACC数据同步后台系统运行状态和API端点监控"
      :icon="IconZoomOut" />

    <!-- 系统概览 -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic 
            title="系统状态" 
            :value="systemHealth.status === 'healthy' ? '正常' : '异常'"
            :value-style="systemHealth.status === 'healthy' ? { color: '#52c41a' } : { color: '#f5222d' }" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="API模块" :value="apiModules.length" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="API端点" :value="totalEndpoints" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic 
            title="Token状态" 
            :value="tokenStatus.is_valid ? '有效' : '无效'"
            :value-style="tokenStatus.is_valid ? { color: '#52c41a' } : { color: '#f5222d' }" />
        </el-card>
      </el-col>
    </el-row>

    <!-- API模块详情 -->
    <el-card class="module-details">
      <template #header>
        <div class="card-header">
          <span>
            <icon-list />
            API模块详情
          </span>
          <el-button type="primary" @click="refreshStatus" :loading="loading">
            <icon-refresh />
            刷新状态
          </el-button>
        </div>
      </template>

      <el-collapse v-model="activeModules">
        <!-- 认证模块 -->
        <el-collapse-item title="认证模块 (auth_api)" name="auth">
          <template #title>
            <div class="module-title">
              <icon-lock />
              <span>认证模块 (auth_api)</span>
              <StatusTag status="success" :text="`${authEndpoints.length} 个端点`" size="small" :show-icon="false" />
            </div>
          </template>
          
           <div class="endpoint-list">
             <div v-for="endpoint in authEndpoints" :key="endpoint.path" class="endpoint-card">
               <div class="endpoint-header">
                 <div class="endpoint-main">
                   <span class="method-tag" :class="endpoint.method.toLowerCase()">{{ endpoint.method }}</span>
                   <div class="endpoint-details">
                     <div class="endpoint-path">{{ endpoint.path }}</div>
                     <div class="endpoint-desc">{{ endpoint.description }}</div>
                   </div>
                 </div>
                 <div class="endpoint-actions">
                   <el-button 
                     size="small" 
                     type="primary" 
                     @click="testEndpoint(endpoint)" 
                     :loading="endpoint.testing"
                     class="test-button">
                     <IconPlayArrowFill />
                     测试
                   </el-button>
                 </div>
               </div>
               
               <!-- ACC API信息卡片 -->
               <div v-if="endpoint.accApi" class="acc-api-card">
                 <div class="acc-api-header">
                   <IconLink class="acc-api-icon" />
                   <span class="acc-api-title">对应的 ACC API</span>
                 </div>
                 <div class="acc-api-body">
                   <div class="acc-api-method">{{ endpoint.accApi.split(' ')[0] }}</div>
                   <div class="acc-api-url">{{ endpoint.accApi.split(' ').slice(1).join(' ') }}</div>
                   <div class="acc-api-note">{{ endpoint.note }}</div>
                 </div>
               </div>
             </div>
           </div>
        </el-collapse-item>

        <!-- Forms API模块 -->
        <el-collapse-item title="表单API模块 (forms_api)" name="forms">
          <template #title>
            <div class="module-title">
              <icon-file />
              <span>表单API模块 (forms_api)</span>
              <StatusTag status="info" :text="`${formsEndpoints.length} 个端点`" size="small" :show-icon="false" />
            </div>
          </template>
          
           <div class="endpoint-list">
             <div v-for="endpoint in formsEndpoints" :key="endpoint.path" class="endpoint-card">
               <div class="endpoint-header">
                 <div class="endpoint-main">
                   <span class="method-tag" :class="endpoint.method.toLowerCase()">{{ endpoint.method }}</span>
                   <div class="endpoint-details">
                     <div class="endpoint-path">{{ endpoint.path }}</div>
                     <div class="endpoint-desc">{{ endpoint.description }}</div>
                   </div>
                 </div>
                 <div class="endpoint-actions">
                   <el-button 
                     size="small" 
                     type="primary" 
                     @click="testEndpoint(endpoint)" 
                     :loading="endpoint.testing"
                     class="test-button">
                     <IconPlayArrowFill />
                     测试
                   </el-button>
                 </div>
               </div>
               
               <!-- ACC API信息卡片 -->
               <div v-if="endpoint.accApi" class="acc-api-card">
                 <div class="acc-api-header">
                   <IconLink class="acc-api-icon" />
                   <span class="acc-api-title">对应的 ACC API</span>
                 </div>
                 <div class="acc-api-body">
                   <div class="acc-api-method">{{ endpoint.accApi.split(' ')[0] }}</div>
                   <div class="acc-api-url">{{ endpoint.accApi.split(' ').slice(1).join(' ') }}</div>
                   <div class="acc-api-note">{{ endpoint.note }}</div>
                 </div>
               </div>
             </div>
           </div>
        </el-collapse-item>

        <!-- Data Connector API模块 -->
        <el-collapse-item title="数据连接器API模块 (data_connector_api)" name="data_connector">
          <template #title>
            <div class="module-title">
              <icon-link />
              <span>数据连接器API模块 (data_connector_api)</span>
              <StatusTag status="warning" :text="`${dataConnectorEndpoints.length} 个端点`" size="small" :show-icon="false" />
            </div>
          </template>
          
           <div class="endpoint-list">
             <div v-for="endpoint in dataConnectorEndpoints" :key="endpoint.path" class="endpoint-card">
               <div class="endpoint-header">
                 <div class="endpoint-main">
                   <span class="method-tag" :class="endpoint.method.toLowerCase()">{{ endpoint.method }}</span>
                   <div class="endpoint-details">
                     <div class="endpoint-path">{{ endpoint.path }}</div>
                     <div class="endpoint-desc">{{ endpoint.description }}</div>
                   </div>
                 </div>
                 <div class="endpoint-actions">
                   <el-button 
                     size="small" 
                     type="primary" 
                     @click="testEndpoint(endpoint)" 
                     :loading="endpoint.testing"
                     class="test-button">
                     <IconPlayArrowFill />
                     测试
                   </el-button>
                 </div>
               </div>
               
               <!-- ACC API信息卡片 -->
               <div v-if="endpoint.accApi" class="acc-api-card">
                 <div class="acc-api-header">
                   <IconLink class="acc-api-icon" />
                   <span class="acc-api-title">对应的 ACC API</span>
                 </div>
                 <div class="acc-api-body">
                   <div class="acc-api-method">{{ endpoint.accApi.split(' ')[0] }}</div>
                   <div class="acc-api-url">{{ endpoint.accApi.split(' ').slice(1).join(' ') }}</div>
                   <div class="acc-api-note">{{ endpoint.note }}</div>
                 </div>
               </div>
             </div>
           </div>
        </el-collapse-item>

        <!-- Reviews API模块 -->
        <el-collapse-item title="评审API模块 (reviews_api)" name="reviews">
          <template #title>
            <div class="module-title">
              <icon-branch />
              <span>评审API模块 (reviews_api)</span>
              <StatusTag status="info" :text="`${reviewsEndpoints.length} 个端点`" size="small" :show-icon="false" />
            </div>
          </template>
          
           <div class="endpoint-list">
             <div v-for="endpoint in reviewsEndpoints" :key="endpoint.path" class="endpoint-card">
               <div class="endpoint-header">
                 <div class="endpoint-main">
                   <span class="method-tag" :class="endpoint.method.toLowerCase()">{{ endpoint.method }}</span>
                   <div class="endpoint-details">
                     <div class="endpoint-path">{{ endpoint.path }}</div>
                     <div class="endpoint-desc">{{ endpoint.description }}</div>
                   </div>
                 </div>
                 <div class="endpoint-actions">
                   <el-button 
                     size="small" 
                     type="primary" 
                     @click="testEndpoint(endpoint)" 
                     :loading="endpoint.testing"
                     class="test-button">
                     <IconPlayArrowFill />
                     测试
                   </el-button>
                 </div>
               </div>
               
               <!-- ACC API信息卡片 -->
               <div v-if="endpoint.accApi" class="acc-api-card">
                 <div class="acc-api-header">
                   <IconLink class="acc-api-icon" />
                   <span class="acc-api-title">对应的 ACC API</span>
                 </div>
                 <div class="acc-api-body">
                   <div class="acc-api-method">{{ endpoint.accApi.split(' ')[0] }}</div>
                   <div class="acc-api-url">{{ endpoint.accApi.split(' ').slice(1).join(' ') }}</div>
                   <div class="acc-api-note">{{ endpoint.note }}</div>
                 </div>
               </div>
             </div>
           </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 测试结果 -->
    <el-card v-if="testResult" class="test-result">
      <template #header>
        <div class="card-header">
          <span>测试结果</span>
          <el-button type="text" @click="clearTestResult">清除</el-button>
        </div>
      </template>
      <div class="result-content">
        <div class="result-info">
          <p><strong>端点:</strong> {{ testResult.endpoint }}</p>
          <p><strong>方法:</strong> {{ testResult.method }}</p>
          <p><strong>状态码:</strong> 
            <span :class="testResult.success ? 'success' : 'error'">
              {{ testResult.status }}
            </span>
          </p>
          <p><strong>响应时间:</strong> {{ testResult.responseTime }}ms</p>
        </div>
        <pre class="result-data">{{ testResult.data }}</pre>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
import Breadcrumb from '../components/Breadcrumb.vue'
import PageHeader from '../components/PageHeader.vue'
import StatusTag from '../components/StatusTag.vue'
import { 
  IconZoomOut,
  IconList,
  IconRefresh,
  IconLock,
  IconFile,
  IconLink,
  IconBranch,
  IconPlayArrowFill,
  IconClose
} from '@arco-design/web-vue/es/icon'

export default {
  name: 'SystemStatus',
  components: {
    Breadcrumb,
    PageHeader,
    StatusTag,
    IconZoomOut,
    IconList,
    IconRefresh,
    IconLock,
    IconFile,
    IconLink,
    IconBranch,
    IconPlayArrowFill,
    IconClose
  },
  data() {
    return {
      loading: false,
      activeModules: ['auth', 'forms', 'data_connector', 'reviews'],
      systemHealth: {},
      tokenStatus: {},
      testResult: null,
      
       // API端点定义
       authEndpoints: [
         { 
           path: '/api/auth/check', 
           method: 'GET', 
           description: '检查认证状态', 
           testing: false,
           accApi: null,
           note: '本地认证状态检查'
         },
         { 
           path: '/api/auth/token-info', 
           method: 'GET', 
           description: '获取Token信息', 
           testing: false,
           accApi: null,
           note: '本地Token信息管理'
         },
         { 
           path: '/api/auth/refresh-token', 
           method: 'POST', 
           description: '刷新Token', 
           testing: false,
           accApi: 'POST https://developer.api.autodesk.com/authentication/v2/token',
           note: '调用Autodesk OAuth刷新端点'
         },
         { 
           path: '/api/auth/logout', 
           method: 'POST', 
           description: '用户登出', 
           testing: false,
           accApi: null,
           note: '本地登出，清除Token'
         },
         { 
           path: '/api/auth/account-info', 
           method: 'GET', 
           description: '获取账户信息', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/userprofile/v1/users/@me',
           note: '获取用户资料和Hub信息'
         },
         { 
           path: '/auth/start', 
           method: 'GET', 
           description: 'OAuth认证入口', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/authentication/v2/authorize',
           note: 'Autodesk OAuth认证流程'
         }
       ],
       
       formsEndpoints: [
         { 
           path: '/api/forms/jarvis', 
           method: 'GET', 
           description: '获取项目表单数据', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/forms/v2/projects/{projectId}/forms',
           note: '获取项目所有表单',
         },
         { 
           path: '/api/forms/templates', 
           method: 'GET', 
           description: '获取表单模板', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/forms/v2/projects/{projectId}/form-templates',
           note: '获取项目表单模板',
         },
         { 
           path: '/api/forms/export-json', 
           method: 'GET', 
           description: '导出表单JSON', 
           testing: false,
           accApi: null,
           note: '本地数据导出功能',
         },
         { 
           path: '/api/forms/templates/export-json', 
           method: 'GET', 
           description: '导出模板JSON', 
           testing: false,
           accApi: null,
           note: '本地模板导出功能',
         }
       ],
       
       dataConnectorEndpoints: [
         { 
           path: '/api/data-connector/get-projects', 
           method: 'GET', 
           description: '获取可用项目', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/project/v1/hubs/{hubId}/projects',
           note: '获取Hub下的所有项目',
         },
         { 
           path: '/api/data-connector/test-format', 
           method: 'POST', 
           description: '测试数据请求格式', 
           testing: false,
           accApi: null,
           note: '本地数据格式验证',
         },
         { 
           path: '/api/data-connector/create-batch-requests', 
           method: 'POST', 
           description: '批量创建数据请求', 
           testing: false,
           accApi: 'POST https://developer.api.autodesk.com/construction/dataconnector/v1/exchanges/{exchangeId}/collections/{collectionId}/requests',
           note: '创建Data Connector数据请求',
         },
         { 
           path: '/api/data-connector/list-jobs', 
           method: 'GET', 
           description: '列出数据作业', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/dataconnector/v1/exchanges/{exchangeId}/collections/{collectionId}/requests/{requestId}/jobs',
           note: '获取数据请求的作业列表',
         },
         { 
           path: '/api/data-connector/get-job-data', 
           method: 'GET', 
           description: '获取作业数据', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/dataconnector/v1/exchanges/{exchangeId}/collections/{collectionId}/requests/{requestId}/jobs/{jobId}/data',
           note: '获取作业生成的数据文件',
         }
       ],
       
       reviewsEndpoints: [
         { 
           path: '/api/reviews/jarvis', 
           method: 'GET', 
           description: '获取项目评审数据', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews',
           note: '获取项目所有评审',
         },
         { 
           path: '/api/reviews/workflows/jarvis', 
           method: 'GET', 
           description: '获取工作流数据', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/workflows/v1/projects/{projectId}/workflows',
           note: '获取项目工作流配置',
         },
         { 
           path: '/api/reviews/versions/{reviewId}', 
           method: 'GET', 
           description: '获取评审文件版本', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/versions',
           note: '获取特定评审的文件版本历史',
         },
         { 
           path: '/api/reviews/history/{reviewId}', 
           method: 'GET', 
           description: '获取审批历史', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/approvals',
           note: '获取评审的审批过程和历史记录',
         },
         { 
           path: '/api/reviews/comments/{reviewId}', 
           method: 'GET', 
           description: '获取评审评论', 
           testing: false,
           accApi: 'GET https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/comments',
           note: '获取评审相关的评论和反馈',
         }
       ]
    }
  },
  
  computed: {
    apiModules() {
      return [
        { name: 'auth_api', title: '认证模块', endpoints: this.authEndpoints.length },
        { name: 'forms_api', title: '表单API模块', endpoints: this.formsEndpoints.length },
        { name: 'data_connector_api', title: '数据连接器API模块', endpoints: this.dataConnectorEndpoints.length },
        { name: 'reviews_api', title: '评审API模块', endpoints: this.reviewsEndpoints.length }
      ]
    },
    
    totalEndpoints() {
      return this.authEndpoints.length + 
             this.formsEndpoints.length + 
             this.dataConnectorEndpoints.length + 
             this.reviewsEndpoints.length
    }
  },
  
  mounted() {
    this.refreshStatus()
  },
  
  methods: {
    async refreshStatus() {
      this.loading = true
      try {
        // 获取系统健康状态
        const healthResponse = await axios.get('/health')
        this.systemHealth = healthResponse.data
        
        // 获取Token状态
        const tokenResponse = await axios.get('/api/auth/token-info')
        this.tokenStatus = tokenResponse.data.token_info || {}
        
        this.$message.success('系统状态已刷新')
      } catch (error) {
        this.$message.error('获取系统状态失败: ' + (error.response?.data?.message || error.message))
      } finally {
        this.loading = false
      }
    },
    
    async testEndpoint(endpoint) {
      endpoint.testing = true
      const startTime = Date.now()
      
      try {
        let response
        if (endpoint.method === 'GET') {
          response = await axios.get(endpoint.path)
        } else if (endpoint.method === 'POST') {
          response = await axios.post(endpoint.path, {})
        }
        
        const responseTime = Date.now() - startTime
        
        this.testResult = {
          endpoint: endpoint.path,
          method: endpoint.method,
          status: response.status,
          success: response.status >= 200 && response.status < 300,
          responseTime: responseTime,
          data: JSON.stringify(response.data, null, 2)
        }
        
        this.$message.success(`端点测试成功: ${endpoint.path}`)
      } catch (error) {
        const responseTime = Date.now() - startTime
        
        this.testResult = {
          endpoint: endpoint.path,
          method: endpoint.method,
          status: error.response?.status || 'Error',
          success: false,
          responseTime: responseTime,
          data: error.response?.data ? 
                JSON.stringify(error.response.data, null, 2) : 
                error.message
        }
        
        this.$message.error(`端点测试失败: ${endpoint.path}`)
      } finally {
        endpoint.testing = false
      }
    },
    
     clearTestResult() {
       this.testResult = null
     },
     
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.system-status {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.stat-card {
  text-align: center;
}

.module-details {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.module-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 端点列表容器 */
.endpoint-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 8px 0;
}

/* 端点卡片 */
.endpoint-card {
  background: #ffffff;
  border: 1px solid #e1e5e9;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.endpoint-card:hover {
  border-color: #1890ff;
  box-shadow: 0 4px 16px rgba(24, 144, 255, 0.08);
  transform: translateY(-2px);
}

/* 端点头部 */
.endpoint-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px 20px;
  background: linear-gradient(135deg, #fafbfc 0%, #f8fafc 100%);
  border-bottom: 1px solid #f0f0f0;
}

.endpoint-main {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1;
}

.endpoint-details {
  flex: 1;
  min-width: 0;
}

.endpoint-path {
  font-family: 'Monaco', 'Consolas', 'SF Mono', monospace;
  font-weight: 600;
  font-size: 14px;
  color: #1f2937;
  margin-bottom: 4px;
  word-break: break-all;
}

.endpoint-desc {
  color: #6b7280;
  font-size: 13px;
  line-height: 1.4;
}

/* HTTP方法标签 */
.method-tag {
  padding: 6px 12px;
  border-radius: 20px;
  color: white;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  min-width: 60px;
  text-align: center;
  text-transform: uppercase;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.method-tag.get {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.method-tag.post {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}

.method-tag.put {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.method-tag.delete {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

/* 测试按钮 */
.endpoint-actions {
  flex-shrink: 0;
}

.test-button {
  border-radius: 8px !important;
  font-weight: 600 !important;
  box-shadow: 0 2px 4px rgba(24, 144, 255, 0.2) !important;
  transition: all 0.2s !important;
}

.test-button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 8px rgba(24, 144, 255, 0.3) !important;
}

/* 优化测试按钮图标大小 */
.test-button .arco-icon {
  font-size: 14px !important;
  margin-right: 4px;
}

/* ACC API 卡片 */
.acc-api-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-top: 1px solid #e0f2fe;
  padding: 16px 20px;
}

.acc-api-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.acc-api-icon {
  color: #0284c7;
  font-size: 16px;
}

.acc-api-title {
  font-weight: 600;
  color: #0369a1;
  font-size: 13px;
}

.acc-api-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.acc-api-method {
  display: inline-block;
  padding: 4px 8px;
  background: rgba(3, 105, 161, 0.1);
  color: #0369a1;
  font-size: 11px;
  font-weight: 700;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  width: fit-content;
}

.acc-api-url {
  font-family: 'Monaco', 'Consolas', 'SF Mono', monospace;
  font-size: 12px;
  color: #0c4a6e;
  background: rgba(255, 255, 255, 0.8);
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid rgba(3, 105, 161, 0.1);
  word-break: break-all;
  line-height: 1.4;
}

.acc-api-note {
  color: #64748b;
  font-size: 12px;
  font-style: italic;
  margin-top: 4px;
}

.test-result {
  margin-top: 20px;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-info p {
  margin: 4px 0;
}

.result-info .success {
  color: #52c41a;
  font-weight: bold;
}

.result-info .error {
  color: #f5222d;
  font-weight: bold;
}

.result-data {
  background: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  font-size: 13px;
  line-height: 1.45;
  overflow-x: auto;
}

/* ACC API 信息样式 */
.acc-api-info {
  margin-top: 8px;
  margin-left: 20px;
}

.acc-api-content {
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  border-radius: 6px;
  padding: 12px;
}

.acc-api-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.acc-api-label {
  font-weight: 600;
  color: #1890ff;
  font-size: 13px;
}

.acc-api-url {
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 12px;
  color: #0050b3;
  background: #f0f9ff;
  padding: 6px 8px;
  border-radius: 4px;
  margin-bottom: 6px;
  word-break: break-all;
}

.acc-api-note {
  font-size: 12px;
  color: #666;
  font-style: italic;
}
</style>

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
import axios from 'axios'
import App from './App.vue'
// 引入事件总线
import eventBus from './utils/eventBus'
// 导入通用样式
import './styles/common.css'
import Login from './views/Login.vue'
import Home from './views/Home.vue'
import AuthSuccess from './views/AuthSuccess.vue'
import AccountInfo from './views/AccountInfo.vue'
import FormsData from './views/FormsData.vue'
import FormsTemplates from './views/FormsTemplates.vue'
import DataConnectorSync from './views/DataConnectorSync.vue'
import ProjectInfo from './views/ProjectInfo.vue'
import ApprovalWorkflows from './views/ApprovalWorkflows.vue'
import Reviews from './views/Reviews.vue'
import SystemStatus from './views/SystemStatus.vue'

// 配置axios支持cookies
axios.defaults.withCredentials = true

// 添加axios响应拦截器处理Token过期和401错误
axios.interceptors.response.use(
  (response) => {
    // 正常响应直接返回
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    // 如果是401错误且不是已经重试过的请求
    if (error.response?.status === 401 && !originalRequest._retry) {
      console.log('🔄 Received 401 error, attempting to refresh auth...')
      originalRequest._retry = true
      
      try {
        // 尝试刷新Token
        const refreshResponse = await axios.post('/api/auth/refresh-token')
        
        if (refreshResponse.data.status === 'success') {
          console.log('✅ Token refreshed successfully, retrying request...')
          
          // 清除认证缓存，强制重新检查
          clearAuthCache()
          
          // 重试原始请求
          return axios(originalRequest)
        }
      } catch (refreshError) {
        console.log('❌ Token refresh failed:', refreshError.message)
        
        // 如果刷新失败，清除缓存并跳转到登录页
        clearAuthCache()
        
        // 避免在登录页面时无限重定向
        if (window.location.pathname !== '/login') {
          console.log('Redirecting to login due to auth failure')
          window.location.href = '/login'
        }
        
        return Promise.reject(refreshError)
      }
    }
    
    // 其他错误直接抛出
    return Promise.reject(error)
  }
)

// 认证状态缓存
let authCache = {
  isAuthenticated: null,
  lastCheck: 0,
  cacheTimeout: 30000 // 30秒缓存
}

// 检查认证状态的函数
async function checkAuth(forceRefresh = false) {
  const now = Date.now()
  
  // 如果有缓存且未过期，直接返回缓存结果
  if (!forceRefresh && authCache.isAuthenticated !== null && 
      (now - authCache.lastCheck) < authCache.cacheTimeout) {
    console.log('Using cached auth status:', authCache.isAuthenticated)
    return authCache.isAuthenticated
  }
  
  try {
    console.log('Checking auth status from server...')
    const response = await axios.get('/api/auth/check', {
      timeout: 8000 // 增加到8秒超时，给Token刷新更多时间
    })
    
    authCache.isAuthenticated = response.data.authenticated
    authCache.lastCheck = now
    
    console.log('Auth status updated:', authCache.isAuthenticated)
    return response.data.authenticated
  } catch (error) {
    console.log('Auth check failed:', error.message)
    
    // 如果是401错误，说明需要重新认证
    if (error.response?.status === 401) {
      console.log('Auth check returned 401, user needs to login')
      authCache.isAuthenticated = false
      authCache.lastCheck = now
      return false
    }
    
    // 如果是网络错误或超时且有缓存，使用缓存
    if (authCache.isAuthenticated !== null && 
        (error.code === 'ECONNABORTED' || error.code === 'NETWORK_ERROR')) {
      console.log('Using cached auth due to network issue:', error.code)
      return authCache.isAuthenticated
    }
    
    // 其他错误，假设未认证
    authCache.isAuthenticated = false
    authCache.lastCheck = now
    return false
  }
}

// 清除认证缓存的函数
function clearAuthCache() {
  authCache.isAuthenticated = null
  authCache.lastCheck = 0
}

const routes = [
  { path: '/', component: Home, meta: { requiresAuth: true } },
  { path: '/login', component: Login, meta: { requiresAuth: false } },
  { path: '/api', redirect: '/' },
  { path: '/auth/success', component: AuthSuccess, meta: { requiresAuth: false } },
  { path: '/account-info', component: AccountInfo, meta: { requiresAuth: true } },
  { path: '/project-info', component: ProjectInfo, meta: { requiresAuth: true } },
  { path: '/forms/jarvis', component: FormsData, meta: { requiresAuth: true } },
  { path: '/forms/templates', component: FormsTemplates, meta: { requiresAuth: true } },
  { path: '/data-connector/sync', component: DataConnectorSync, meta: { requiresAuth: true } },
  { path: '/reviews/workflows', component: ApprovalWorkflows, meta: { requiresAuth: true } },
  { path: '/reviews/data', component: Reviews, meta: { requiresAuth: true } },
  { path: '/system/status', component: SystemStatus, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  console.log('Navigating to:', to.path, 'from:', from.path)
  
  // 如果路由不需要认证，直接通过
  if (to.meta.requiresAuth === false) {
    console.log('Route does not require auth, proceeding')
    next()
    return
  }

  // 特殊处理：如果从认证成功页面跳转，强制刷新认证状态
  const forceRefresh = from.path === '/auth/success' || to.query.forceAuthCheck === 'true'
  
  // 检查认证状态
  console.log('Checking authentication...', forceRefresh ? '(forced refresh)' : '')
  const isAuthenticated = await checkAuth(forceRefresh)
  console.log('Authentication result:', isAuthenticated)
  
  if (isAuthenticated) {
    // 已认证，允许访问
    next()
  } else {
    // 未认证，跳转到登录页
    if (to.path !== '/login') {
      console.log('Redirecting to login page')
      next('/login')
    } else {
      next()
    }
  }
})

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.use(ArcoVue)

// 注册事件总线为全局属性
app.config.globalProperties.$eventBus = eventBus

app.mount('#app')

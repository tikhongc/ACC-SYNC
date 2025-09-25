<template>
  <div class="breadcrumb-container">
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item>
        <router-link to="/" class="breadcrumb-link">
          <IconHome class="breadcrumb-icon" />
          <span>首页</span>
        </router-link>
      </el-breadcrumb-item>
      <el-breadcrumb-item v-for="item in breadcrumbItems" :key="item.path || item.name">
        <router-link v-if="item.path" :to="item.path" class="breadcrumb-link">
          <component v-if="item.icon" :is="item.icon" class="breadcrumb-icon" />
          <span>{{ item.name }}</span>
        </router-link>
        <span v-else class="breadcrumb-current">
          <component v-if="item.icon" :is="item.icon" class="breadcrumb-icon" />
          <span>{{ item.name }}</span>
        </span>
      </el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>

<script>
import { ArrowRight } from '@element-plus/icons-vue'
import { 
  IconHome, 
  IconUser, 
  IconFile, 
  IconSync, 
  IconSettings,
  IconDashboard,
  IconApps,
  IconFolder,
  IconBranch,
  IconZoomOut
} from '@arco-design/web-vue/es/icon'

export default {
  name: 'Breadcrumb',
  components: {
    ArrowRight,
    IconHome,
    IconUser,
    IconFile,
    IconSync,
    IconSettings,
    IconDashboard,
    IconApps,
    IconFolder,
    IconBranch,
    IconZoomOut
  },
  computed: {
    breadcrumbItems() {
      const route = this.$route
      const items = []
      
      // 根据路由生成面包屑
      switch (route.path) {
        case '/':
        case '/api':
          // 首页不需要额外的面包屑
          break
        case '/account-info':
          items.push({ name: '系统管理', icon: 'IconSettings', path: '/system/status' })
          items.push({ name: '账户信息', icon: 'IconUser', path: null })
          break
        case '/project-info':
          items.push({ name: '系统管理', icon: 'IconSettings', path: '/system/status' })
          items.push({ name: '项目信息', icon: 'IconFolder', path: null })
          break
        case '/forms/jarvis':
          items.push({ name: 'Forms API', icon: 'IconFile', path: '/forms/templates' })
          items.push({ name: '项目表单数据', icon: 'IconDashboard', path: null })
          break
        case '/forms/templates':
          items.push({ name: 'Forms API', icon: 'IconFile', path: null })
          items.push({ name: '表单模板', icon: 'IconApps', path: null })
          break
        case '/forms/test':
          items.push({ name: 'Forms API', icon: 'IconFile', path: '/forms/templates' })
          items.push({ name: 'API测试', icon: 'IconSettings', path: null })
          break
        case '/data-connector/sync':
          items.push({ name: 'Data Connector API', icon: 'IconSync', path: null })
          items.push({ name: '数据同步', icon: 'IconDashboard', path: null })
          break
        case '/reviews/data':
          items.push({ name: 'Reviews API', icon: 'IconBranch', path: '/reviews/workflows' })
          items.push({ name: '项目评审数据', icon: 'IconDashboard', path: null })
          break
        case '/reviews/workflows':
          items.push({ name: 'Reviews API', icon: 'IconBranch', path: null })
          items.push({ name: '审批工作流', icon: 'IconSettings', path: null })
          break
        case '/system/status':
          items.push({ name: '系统管理', icon: 'IconSettings', path: null })
          items.push({ name: '系统状态', icon: 'IconZoomOut', path: null })
          break
        case '/auth/success':
          items.push({ name: '认证成功', icon: 'IconUser', path: null })
          break
        default:
          // 对于其他路径，尝试自动生成
          const pathSegments = route.path.split('/').filter(segment => segment)
          if (pathSegments.length > 0) {
            items.push({ name: '未知页面', icon: 'IconApps', path: null })
          }
          break
      }
      
      return items
    }
  }
}
</script>

<style scoped>
.breadcrumb-container {
  padding: 12px 0;
  margin-bottom: 16px;
  background: #fafafa;
  border-radius: 6px;
  padding: 8px 16px;
  border: 1px solid #f0f0f0;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #1890ff;
  text-decoration: none;
  transition: all 0.2s;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.breadcrumb-link:hover {
  color: #40a9ff;
  background: rgba(24, 144, 255, 0.08);
}

.breadcrumb-current {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #666;
  font-size: 13px;
  font-weight: 500;
}

.breadcrumb-icon {
  font-size: 12px !important;
  flex-shrink: 0;
}

/* Element Plus 面包屑样式 */
:deep(.el-breadcrumb) {
  font-size: 13px;
  line-height: 1.5;
}

:deep(.el-breadcrumb__separator) {
  color: #ccc;
  font-size: 12px;
}

:deep(.el-breadcrumb__item) {
  display: inline-flex;
  align-items: center;
}

:deep(.el-breadcrumb__inner) {
  font-weight: normal;
}
</style>

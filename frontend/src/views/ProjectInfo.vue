<template>
  <div class="project-info">
    <!-- 面包屑导航 -->
    <Breadcrumb />
    
    <!-- 页面头部 -->
    <PageHeader
      title="项目信息"
      description="查看和管理 Autodesk Construction Cloud 项目信息"
      :icon="IconFolder"
      :action-buttons="headerButtons"
      @action="handleHeaderAction" />

    <!-- 加载状态 -->
    <LoadingState 
      v-if="loading"
      type="card"
      title="正在获取项目信息"
      text="请稍候，正在从服务器获取最新的项目信息..."
      :show-progress="false"
      :show-cancel="false" />

    <!-- 错误状态 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      :closable="false"
      show-icon
      style="margin-bottom: 20px">
      <template #default>
        <p>{{ error }}</p>
        <el-button @click="startAuth" type="primary" size="small" style="margin-top: 10px">
          重新认证
        </el-button>
      </template>
    </el-alert>

    <!-- 成功状态 -->
    <div v-if="projectData && !loading && !error">
      <!-- Hub 信息 -->
      <el-card class="info-card" style="margin-bottom: 20px;">
        <template #header>
          <div class="card-header">
            <icon-cloud />
            Hub 信息
          </div>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="Hub ID">{{ projectData.hub.hubId }}</el-descriptions-item>
          <el-descriptions-item label="Hub 名称">{{ projectData.hub.hubName }}</el-descriptions-item>
          <el-descriptions-item label="真实 Account ID">{{ projectData.hub.realAccountId }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 项目列表 -->
      <el-card class="info-card" style="margin-bottom: 20px;">
        <template #header>
          <div class="card-header">
            <icon-folder />
            项目列表
          </div>
        </template>
        <div v-if="projectData.projects && projectData.projects.data && projectData.projects.data.length > 0">
          <el-table :data="projectData.projects.data" style="width: 100%" stripe>
            <el-table-column prop="id" label="项目ID" width="280" show-overflow-tooltip>
              <template #default="scope">
                <StatusTag status="info" :text="formatProjectId(scope.row.id)" size="small" :show-icon="false" />
              </template>
            </el-table-column>
            <el-table-column label="项目名称" min-width="200" show-overflow-tooltip>
              <template #default="scope">
                {{ scope.row.attributes?.name || 'Unknown Project' }}
              </template>
            </el-table-column>
            <el-table-column label="权限范围" width="150">
              <template #default="scope">
                <StatusTag 
                  :status="getPermissionStatus(scope.row.attributes?.permissions?.level)"
                  :text="scope.row.attributes?.permissions?.scope || '基础访问'"
                  size="small"
                  :show-icon="false" />
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="scope">
                <StatusTag 
                  :status="getProjectStatus(scope.row.attributes?.status)"
                  :text="getStatusText(scope.row.attributes?.status)"
                  size="small"
                  :show-icon="false" />
              </template>
            </el-table-column>
            <el-table-column label="项目类型" width="120" show-overflow-tooltip>
              <template #default="scope">
                <span class="project-type">{{ scope.row.attributes?.projectType || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button type="text" size="small" @click="viewProjectDetails(scope.row)">
                  查看详情
                </el-button>
                <el-button type="text" size="small" @click="toggleProjectExpand(scope.row.id)">
                  {{ expandedProjects.includes(scope.row.id) ? '收起' : '展开' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 展开的项目详情 -->
          <div v-for="project in projectData.projects.data" :key="project.id">
            <el-collapse-transition>
              <div v-if="expandedProjects.includes(project.id)" class="project-details-expanded">
                <el-card class="project-detail-card" shadow="never">
                  <template #header>
                    <div class="project-detail-header">
                      <icon-info-circle />
                      项目详细信息 - {{ project.attributes?.name || 'Unknown Project' }}
                    </div>
                  </template>
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-descriptions :column="1" size="small" border>
                        <el-descriptions-item label="完整项目ID">
                          <StatusTag status="info" :text="project.id" size="small" :show-icon="false" />
                        </el-descriptions-item>
                        <el-descriptions-item label="工作编号">
                          {{ project.attributes?.jobNumber || '-' }}
                        </el-descriptions-item>
                        <el-descriptions-item label="项目类型">
                          {{ project.attributes?.projectType || '-' }}
                        </el-descriptions-item>
                        <el-descriptions-item label="开始日期">
                          {{ formatDate(project.attributes?.startDate) }}
                        </el-descriptions-item>
                        <el-descriptions-item label="结束日期">
                          {{ formatDate(project.attributes?.endDate) }}
                        </el-descriptions-item>
                      </el-descriptions>
                    </el-col>
                    <el-col :span="12">
                      <el-descriptions :column="1" size="small" border>
                        <el-descriptions-item label="权限级别">
                          <StatusTag 
                            :status="getPermissionStatus(project.attributes?.permissions?.level)"
                            :text="project.attributes?.permissions?.level || 'member'"
                            size="small"
                            :show-icon="false" />
                        </el-descriptions-item>
                        <el-descriptions-item label="权限描述">
                          {{ project.attributes?.permissions?.description || '标准项目访问权限' }}
                        </el-descriptions-item>
                        <el-descriptions-item label="货币">
                          {{ project.attributes?.currency || '-' }}
                        </el-descriptions-item>
                        <el-descriptions-item label="时区">
                          {{ project.attributes?.timezone || '-' }}
                        </el-descriptions-item>
                        <el-descriptions-item label="语言">
                          {{ project.attributes?.language || '-' }}
                        </el-descriptions-item>
                      </el-descriptions>
                    </el-col>
                  </el-row>
                </el-card>
              </div>
            </el-collapse-transition>
          </div>
        </div>
        <div v-else>
          <el-empty description="暂无项目数据" />
        </div>
      </el-card>

      <!-- 项目统计 -->
      <el-row :gutter="20" style="margin-bottom: 20px;">
        <el-col :span="6">
          <el-card class="stat-card">
            <el-statistic title="项目总数" :value="getProjectCount()" />
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <el-statistic title="活跃项目" :value="getActiveProjectCount()" />
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <el-statistic title="管理员权限" :value="getAdminProjectCount()" />
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <el-statistic title="Hub 数量" :value="1" />
          </el-card>
        </el-col>
      </el-row>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button type="primary" @click="refreshData" :loading="loading">
          <icon-refresh />
          刷新数据
        </el-button>
        <el-button @click="debugProjects" type="info">
          <icon-bug />
          调试项目
        </el-button>
        <el-button @click="debugDataConnector" type="warning">
          <icon-link />
          调试Data Connector
        </el-button>
        <el-button @click="$router.push('/')">
          <icon-home />
          返回首页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Breadcrumb from '../components/Breadcrumb.vue'
import PageHeader from '../components/PageHeader.vue'
import LoadingState from '../components/LoadingState.vue'
import StatusTag from '../components/StatusTag.vue'
import { 
  IconFolder, 
  IconArrowLeft, 
  IconCloud, 
  IconRefresh, 
  IconHome,
  IconInfoCircle,
  IconBug,
  IconLink
} from '@arco-design/web-vue/es/icon'

export default {
  name: 'ProjectInfo',
  components: {
    Breadcrumb,
    PageHeader,
    LoadingState,
    StatusTag,
    IconFolder,
    IconArrowLeft,
    IconCloud,
    IconRefresh,
    IconHome,
    IconInfoCircle,
    IconBug,
    IconLink
  },
  data() {
    return {
      loading: false,
      error: null,
      projectData: null,
      expandedProjects: []
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
          icon: 'Refresh',
          action: 'refresh'
        }
      ]
    }
  },
  mounted() {
    this.fetchProjectInfo()
  },
  methods: {
    async fetchProjectInfo() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/auth/account-info')
        
        // 检查响应类型
        if (response.headers['content-type']?.includes('application/json')) {
          this.projectData = response.data
        } else {
          // 如果返回HTML，说明需要重新认证
          throw new Error('需要重新认证')
        }
      } catch (error) {
        console.error('获取项目信息失败:', error)
        if (error.response?.status === 401) {
          this.error = '未找到 Access Token，请先进行认证'
        } else {
          this.error = `获取项目信息时发生错误: ${error.response?.data?.message || error.message}`
        }
      } finally {
        this.loading = false
      }
    },
    
    getProjectCount() {
      return this.projectData?.projects?.data?.length || 0
    },

    getActiveProjectCount() {
      if (!this.projectData?.projects?.data) return 0
      return this.projectData.projects.data.filter(
        project => project.attributes?.status === 'active'
      ).length
    },

    getAdminProjectCount() {
      if (!this.projectData?.projects?.data) return 0
      return this.projectData.projects.data.filter(
        project => project.attributes?.permissions?.level === 'admin'
      ).length
    },
    
    viewProjectDetails(project) {
      // 自动展开项目详情
      if (!this.expandedProjects.includes(project.id)) {
        this.toggleProjectExpand(project.id)
      }
      this.$message.success(`已展开项目详情: ${project.attributes?.name || 'Unknown Project'}`)
    },
    
    startAuth() {
      window.location.href = '/auth/start'
    },
    
    refreshData() {
      this.fetchProjectInfo()
    },

    handleHeaderAction(action) {
      switch (action) {
        case 'home':
          this.$router.push('/')
          break
        case 'refresh':
          this.refreshData()
          break
      }
    },

    // 格式化项目ID显示
    formatProjectId(id) {
      if (!id) return ''
      // 如果ID太长，只显示前8位和后8位
      if (id.length > 20) {
        return `${id.substring(0, 8)}...${id.substring(id.length - 8)}`
      }
      return id
    },

    // 获取权限标签类型
    getPermissionTagType(level) {
      switch (level) {
        case 'admin':
          return 'danger'
        case 'member':
          return 'success'
        case 'viewer':
          return 'warning'
        default:
          return 'info'
      }
    },

    // 获取状态标签类型
    getStatusTagType(status) {
      switch (status) {
        case 'active':
          return 'success'
        case 'inactive':
          return 'warning'
        case 'archived':
          return 'info'
        case 'suspended':
          return 'danger'
        default:
          return 'info'
      }
    },

    // 获取权限状态（适配StatusTag）
    getPermissionStatus(level) {
      switch (level) {
        case 'admin':
          return 'warning'
        case 'member':
          return 'success'
        case 'viewer':
          return 'info'
        default:
          return 'info'
      }
    },

    // 获取项目状态（适配StatusTag）
    getProjectStatus(status) {
      switch (status) {
        case 'active':
          return 'active'
        case 'inactive':
          return 'inactive'
        case 'archived':
          return 'archived'
        case 'suspended':
          return 'error'
        default:
          return 'unknown'
      }
    },

    // 获取状态文本
    getStatusText(status) {
      switch (status) {
        case 'active':
          return '活跃'
        case 'inactive':
          return '非活跃'
        case 'archived':
          return '已归档'
        case 'suspended':
          return '已暂停'
        default:
          return status || '未知'
      }
    },

    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '-'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('zh-CN')
      } catch (e) {
        return dateString
      }
    },

    // 切换项目展开状态
    toggleProjectExpand(projectId) {
      const index = this.expandedProjects.indexOf(projectId)
      if (index > -1) {
        this.expandedProjects.splice(index, 1)
      } else {
        this.expandedProjects.push(projectId)
      }
    },

    // 调试项目获取功能
    async debugProjects() {
      this.loading = true
      try {
        const response = await axios.get('/api/auth/debug-projects')
        
        if (response.status === 200) {
          const debugInfo = response.data.debug_info
          
          let message = `🔍 调试信息:\n`
          message += `📊 找到 ${debugInfo.hubs_found || 0} 个Hub\n`
          
          if (debugInfo.first_hub) {
            message += `🏢 Hub: ${debugInfo.first_hub.name} (${debugInfo.first_hub.id})\n`
          }
          
          if (debugInfo.projects_found !== undefined) {
            message += `🎯 找到 ${debugInfo.projects_found} 个项目:\n`
            
            if (debugInfo.projects_list && debugInfo.projects_list.length > 0) {
              debugInfo.projects_list.forEach((project, index) => {
                message += `  ${index + 1}. ${project.name} (${project.status})\n`
                message += `     ID: ${project.id}\n`
              })
            }
          }
          
          this.$alert(message, '项目调试信息', {
            confirmButtonText: '确定',
            type: 'info'
          })
        }
      } catch (error) {
        console.error('调试项目时出错:', error)
        if (error.response?.status === 401) {
          this.$message.warning('请先进行认证')
        } else {
          this.$message.error('调试失败: ' + (error.response?.data?.error || error.message))
        }
      } finally {
        this.loading = false
      }
    },

    // 调试Data Connector项目查找功能
    async debugDataConnector() {
      this.loading = true
      try {
        const response = await axios.get('/api/data-connector/debug-find-projects')
        
        if (response.status === 200) {
          const debugInfo = response.data.debug_info
          const summary = response.data.summary
          
          let message = `🔍 Data Connector 调试信息:\n\n`
          
          // 步骤1：Hub信息
          message += `📊 步骤1 - Hub查找:\n`
          message += `  找到 ${debugInfo.step_1_hubs.hubs_found || 0} 个Hub\n\n`
          
          // 步骤2：项目查找
          message += `🎯 步骤2 - 项目查找:\n`
          message += `  总项目数: ${debugInfo.step_2_projects.total_projects_found}\n`
          
          if (debugInfo.step_2_projects.projects_by_hub) {
            Object.values(debugInfo.step_2_projects.projects_by_hub).forEach(hubInfo => {
              if (hubInfo.success) {
                message += `  Hub "${hubInfo.hub_name}": ${hubInfo.projects_found} 个项目\n`
              } else {
                message += `  Hub "${hubInfo.hub_name}": 获取失败\n`
              }
            })
          }
          
          // 步骤3：筛选结果
          message += `\n📋 步骤3 - 筛选结果:\n`
          message += `  活跃项目: ${debugInfo.step_3_filtering.active_projects_count}\n`
          message += `  非活跃项目: ${debugInfo.step_3_filtering.inactive_projects_count}\n\n`
          
          if (debugInfo.step_3_filtering.active_projects.length > 0) {
            message += `✅ 找到的活跃项目:\n`
            debugInfo.step_3_filtering.active_projects.forEach((project, index) => {
              message += `  ${index + 1}. ${project.project_name}\n`
              message += `     ID: ${project.project_id}\n`
              message += `     状态: ${project.project_status}\n`
            })
          } else {
            message += `❌ 未找到活跃项目\n`
            if (debugInfo.step_3_filtering.inactive_projects.length > 0) {
              message += `\n非活跃项目:\n`
              debugInfo.step_3_filtering.inactive_projects.forEach((project, index) => {
                message += `  ${index + 1}. ${project.project_name} (状态: ${project.project_status})\n`
              })
            }
          }
          
          // 配置建议
          if (debugInfo.final_result.configuration_recommendations.length > 0) {
            message += `\n💡 配置建议:\n`
            debugInfo.final_result.configuration_recommendations.forEach(rec => {
              message += `  ${rec.project_name}:\n`
              message += `  ${rec.config_line}\n\n`
            })
          }
          
          this.$alert(message, 'Data Connector 调试结果', {
            confirmButtonText: '确定',
            type: debugInfo.final_result.success ? 'success' : 'warning'
          })
          
        }
      } catch (error) {
        console.error('调试Data Connector时出错:', error)
        if (error.response?.status === 401) {
          this.$message.warning('请先进行认证')
        } else {
          this.$message.error('Data Connector调试失败: ' + (error.response?.data?.error || error.message))
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
@import '../styles/common.css';

.project-info {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}


.loading-container {
  height: 200px;
  position: relative;
}

.info-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border: 1px solid #e8e8e8;
  background: white;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.stat-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  text-align: center;
}

.action-buttons {
  text-align: center;
  margin: 20px 0;
}

.action-buttons .el-button {
  margin: 0 10px;
}

/* 项目详情展开区域 */
.project-details-expanded {
  margin-top: 10px;
  margin-bottom: 10px;
}

.project-detail-card {
  border-left: 4px solid #409eff;
  background-color: #f8f9fa;
}

.project-detail-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #409eff;
}

.project-type {
  color: #606266;
  font-size: 13px;
}

/* 表格样式优化 */
:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
  font-weight: 600;
}

:deep(.el-table td) {
  padding: 12px 0;
}

:deep(.el-tag) {
  border-radius: 4px;
  font-weight: 500;
}

/* 权限标签特殊样式 */
.el-tag.el-tag--danger {
  background-color: #fef0f0;
  border-color: #fbc4c4;
  color: #f56c6c;
}

.el-tag.el-tag--success {
  background-color: #f0f9ff;
  border-color: #b3d8ff;
  color: #409eff;
}

.el-tag.el-tag--warning {
  background-color: #fdf6ec;
  border-color: #f5dab1;
  color: #e6a23c;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .project-info {
    padding: 10px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .action-buttons .el-button {
    margin: 5px;
    width: calc(50% - 10px);
  }
  
  /* 移动端表格调整 */
  :deep(.el-table .el-table__cell) {
    padding: 8px 4px;
  }
  
  .project-detail-card {
    margin: 5px 0;
  }
}
</style>

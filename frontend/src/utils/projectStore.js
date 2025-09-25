/**
 * 项目信息本地存储管理工具
 * 用于管理ACC项目数据的localStorage缓存
 */

// 存储键名
const PROJECT_STORAGE_KEY = 'acc_projects'
const SELECTED_PROJECT_KEY = 'acc_selected_project'

/**
 * 项目存储管理类
 */
class ProjectStore {
  constructor() {
    this.cacheExpireHours = 24 // 缓存24小时过期
  }

  /**
   * 保存项目列表到localStorage
   * @param {Object} projectData - 项目数据对象
   * @param {Array} projectData.projects.list - 项目列表
   * @param {Object} projectData.cache_info - 缓存信息
   */
  saveProjects(projectData) {
    try {
      const dataToSave = {
        ...projectData,
        cache_info: {
          ...projectData.cache_info,
          cached_at: Date.now(), // 添加本地缓存时间
          expires_at: Date.now() + (this.cacheExpireHours * 60 * 60 * 1000)
        }
      }
      
      localStorage.setItem(PROJECT_STORAGE_KEY, JSON.stringify(dataToSave))
      console.log('项目数据已保存到localStorage:', dataToSave.projects?.list?.length, '个项目')
      return true
    } catch (error) {
      console.error('保存项目数据失败:', error)
      return false
    }
  }

  /**
   * 从localStorage获取项目列表
   * @param {boolean} checkExpiry - 是否检查过期时间
   * @returns {Object|null} 项目数据或null
   */
  getProjects(checkExpiry = true) {
    try {
      const cachedData = localStorage.getItem(PROJECT_STORAGE_KEY)
      if (!cachedData) {
        console.log('未找到缓存的项目数据')
        return null
      }

      const parsedData = JSON.parse(cachedData)
      
      // 检查缓存是否过期
      if (checkExpiry && parsedData.cache_info?.expires_at) {
        const now = Date.now()
        if (now > parsedData.cache_info.expires_at) {
          console.log('缓存已过期，需要刷新项目数据')
          return null
        }
      }

      console.log('从localStorage加载项目数据:', parsedData.projects?.list?.length, '个项目')
      return parsedData
    } catch (error) {
      console.error('获取缓存项目数据失败:', error)
      return null
    }
  }

  /**
   * 获取项目列表（仅列表部分）
   * @param {boolean} checkExpiry - 是否检查过期时间
   * @returns {Array} 项目列表数组
   */
  getProjectList(checkExpiry = true) {
    const projectData = this.getProjects(checkExpiry)
    return projectData?.projects?.list || []
  }

  /**
   * 根据ID查找项目
   * @param {string} projectId - 项目ID
   * @returns {Object|null} 项目对象或null
   */
  findProjectById(projectId) {
    const projects = this.getProjectList()
    return projects.find(p => p.id === projectId) || null
  }

  /**
   * 获取活跃项目列表
   * @returns {Array} 活跃项目列表
   */
  getActiveProjects() {
    const projects = this.getProjectList()
    return projects.filter(p => p.isActive)
  }

  /**
   * 保存当前选中的项目
   * @param {Object|Array} selectedProject - 选中的项目（对象）或项目列表（数组）
   */
  saveSelectedProject(selectedProject) {
    try {
      const dataToSave = {
        project: selectedProject,
        selected_at: Date.now(),
        expires_at: Date.now() + (2 * 60 * 60 * 1000) // 2小时过期
      }
      
      localStorage.setItem(SELECTED_PROJECT_KEY, JSON.stringify(dataToSave))
      console.log('已保存选中项目:', Array.isArray(selectedProject) ? 
        `${selectedProject.length}个项目` : selectedProject?.name)
      return true
    } catch (error) {
      console.error('保存选中项目失败:', error)
      return false
    }
  }

  /**
   * 获取当前选中的项目
   * @param {boolean} checkExpiry - 是否检查过期时间
   * @returns {Object|Array|null} 选中的项目或null
   */
  getSelectedProject(checkExpiry = true) {
    try {
      const cachedData = localStorage.getItem(SELECTED_PROJECT_KEY)
      if (!cachedData) {
        return null
      }

      const parsedData = JSON.parse(cachedData)
      
      // 检查是否过期
      if (checkExpiry && parsedData.expires_at) {
        const now = Date.now()
        if (now > parsedData.expires_at) {
          console.log('选中项目已过期')
          this.clearSelectedProject()
          return null
        }
      }

      return parsedData.project
    } catch (error) {
      console.error('获取选中项目失败:', error)
      return null
    }
  }

  /**
   * 清除选中的项目
   */
  clearSelectedProject() {
    try {
      localStorage.removeItem(SELECTED_PROJECT_KEY)
      console.log('已清除选中项目')
      return true
    } catch (error) {
      console.error('清除选中项目失败:', error)
      return false
    }
  }

  /**
   * 清除所有项目缓存
   */
  clearAllProjects() {
    try {
      localStorage.removeItem(PROJECT_STORAGE_KEY)
      localStorage.removeItem(SELECTED_PROJECT_KEY)
      console.log('已清除所有项目缓存')
      return true
    } catch (error) {
      console.error('清除项目缓存失败:', error)
      return false
    }
  }

  /**
   * 获取缓存状态信息
   * @returns {Object} 缓存状态信息
   */
  getCacheStatus() {
    const projectData = this.getProjects(false)
    const selectedProject = this.getSelectedProject(false)
    
    const now = Date.now()
    
    return {
      projects: {
        exists: !!projectData,
        count: projectData?.projects?.list?.length || 0,
        cached_at: projectData?.cache_info?.cached_at || null,
        expires_at: projectData?.cache_info?.expires_at || null,
        is_expired: projectData?.cache_info?.expires_at ? 
          now > projectData.cache_info.expires_at : true,
        age_hours: projectData?.cache_info?.cached_at ? 
          Math.round((now - projectData.cache_info.cached_at) / (1000 * 60 * 60) * 10) / 10 : null
      },
      selected_project: {
        exists: !!selectedProject,
        is_array: Array.isArray(selectedProject),
        count: Array.isArray(selectedProject) ? selectedProject.length : 
               (selectedProject ? 1 : 0),
        name: Array.isArray(selectedProject) ? 
              `${selectedProject.length}个项目` : 
              selectedProject?.name || null
      }
    }
  }

  /**
   * 强制刷新项目数据（从API）
   * @returns {Promise<Object>} API响应数据
   */
  async refreshProjectsFromAPI() {
    try {
      const axios = (await import('axios')).default
      console.log('开始从API刷新项目数据...')
      
      const response = await axios.get('/api/auth/projects', {
        timeout: 30000,
        params: {
          _t: Date.now() // 防止缓存
        }
      })

      if (response.data.status === 'success') {
        // 保存到缓存
        this.saveProjects(response.data)
        console.log('项目数据刷新成功:', response.data.projects?.list?.length, '个项目')
        return response.data
      } else {
        throw new Error(response.data.error || '获取项目数据失败')
      }
    } catch (error) {
      console.error('刷新项目数据失败:', error)
      throw error
    }
  }

  /**
   * 智能获取项目数据（优先缓存，必要时刷新）
   * @param {boolean} forceRefresh - 是否强制刷新
   * @returns {Promise<Object>} 项目数据
   */
  async getProjectsWithCache(forceRefresh = false) {
    // 如果强制刷新，直接从API获取
    if (forceRefresh) {
      return await this.refreshProjectsFromAPI()
    }

    // 尝试从缓存获取
    const cachedData = this.getProjects(true)
    if (cachedData && cachedData.projects?.list?.length > 0) {
      console.log('使用缓存的项目数据')
      return cachedData
    }

    // 缓存无效，从API获取
    console.log('缓存无效，从API获取项目数据')
    return await this.refreshProjectsFromAPI()
  }
}

// 创建单例实例
const projectStore = new ProjectStore()

// 导出实例和类
export default projectStore
export { ProjectStore }

// 便捷方法导出
export const {
  saveProjects,
  getProjects,
  getProjectList,
  findProjectById,
  getActiveProjects,
  saveSelectedProject,
  getSelectedProject,
  clearSelectedProject,
  clearAllProjects,
  getCacheStatus,
  refreshProjectsFromAPI,
  getProjectsWithCache
} = projectStore

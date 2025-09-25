// 简单的事件总线实现
class EventBus {
  constructor() {
    this.events = {}
  }

  // 监听事件
  on(event, callback) {
    if (!this.events[event]) {
      this.events[event] = []
    }
    this.events[event].push(callback)
  }

  // 移除事件监听
  off(event, callback) {
    if (!this.events[event]) return
    
    if (callback) {
      const index = this.events[event].indexOf(callback)
      if (index > -1) {
        this.events[event].splice(index, 1)
      }
    } else {
      // 如果没有指定回调函数，移除所有监听器
      this.events[event] = []
    }
  }

  // 触发事件
  emit(event, data) {
    if (!this.events[event]) {
      return
    }
    
    this.events[event].forEach((callback) => {
      try {
        callback(data)
      } catch (error) {
        console.error(`Event bus error for event "${event}":`, error)
      }
    })
  }

  // 一次性监听
  once(event, callback) {
    const onceCallback = (data) => {
      callback(data)
      this.off(event, onceCallback)
    }
    this.on(event, onceCallback)
  }
}

// 导出单例
export default new EventBus()

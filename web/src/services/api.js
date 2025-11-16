// API服务文件，处理与后端的通信
import { API_BASE_URL } from '../config/apiConfig';

class ApiService {
  constructor() {
    this.ws = null;
    this.messageHandlers = [];
    this.connectionHandlers = [];
    this.isConnecting = false;
  }

  // 连接WebSocket服务器
  connect() {
    return new Promise((resolve, reject) => {
      // 如果已经在连接中或已连接，返回已有连接
      if (this.isConnecting || this.ws?.readyState === WebSocket.OPEN) {
        if (this.ws?.readyState === WebSocket.OPEN) {
          resolve(this.ws);
        }
        return;
      }

      this.isConnecting = true;
      
      try {
        // 构建WebSocket URL
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsBaseUrl = API_BASE_URL.replace(/^http/, 'ws');
        const wsUrl = `${wsBaseUrl}/api/chat/ws`;
        
        // 开发环境时使用相对路径
        const finalWsUrl = process.env.NODE_ENV === 'production' ? wsUrl : '/api/chat/ws';
        
        this.ws = new WebSocket(finalWsUrl);
        
        // 连接打开
        this.ws.onopen = () => {
          console.log('WebSocket连接已建立');
          this.isConnecting = false;
          this.notifyConnectionHandlers(true);
          resolve(this.ws);
        };
        
        // 接收消息
        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.notifyMessageHandlers(data);
          } catch (error) {
            console.error('解析WebSocket消息失败:', error);
          }
        };
        
        // 连接关闭
        this.ws.onclose = () => {
          console.log('WebSocket连接已关闭');
          this.isConnecting = false;
          this.notifyConnectionHandlers(false);
        };
        
        // 连接错误
        this.ws.onerror = (error) => {
          console.error('WebSocket连接错误:', error);
          this.isConnecting = false;
          this.notifyConnectionHandlers(false);
          reject(error);
        };
      } catch (error) {
        console.error('创建WebSocket连接失败:', error);
        this.isConnecting = false;
        reject(error);
      }
    });
  }

  // 断开WebSocket连接
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  // 发送消息到服务器
  async sendMessage(message) {
    try {
      // 确保连接已建立
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
        await this.connect();
      }
      
      this.ws.send(JSON.stringify({
        type: 'message',
        content: message,
        timestamp: new Date().toISOString()
      }));
    } catch (error) {
      console.error('发送消息失败:', error);
      throw error;
    }
  }

  // 注册消息处理器
  onMessage(handler) {
    if (typeof handler === 'function') {
      this.messageHandlers.push(handler);
    }
  }

  // 移除消息处理器
  offMessage(handler) {
    this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
  }

  // 注册连接状态处理器
  onConnectionChange(handler) {
    if (typeof handler === 'function') {
      this.connectionHandlers.push(handler);
    }
  }

  // 移除连接状态处理器
  offConnectionChange(handler) {
    this.connectionHandlers = this.connectionHandlers.filter(h => h !== handler);
  }

  // 通知所有消息处理器
  notifyMessageHandlers(message) {
    this.messageHandlers.forEach(handler => {
      try {
        handler(message);
      } catch (error) {
        console.error('消息处理器执行错误:', error);
      }
    });
  }

  // 通知所有连接状态处理器
  notifyConnectionHandlers(isConnected) {
    this.connectionHandlers.forEach(handler => {
      try {
        handler(isConnected);
      } catch (error) {
        console.error('连接状态处理器执行错误:', error);
      }
    });
  }

  // 获取连接状态
  isConnected() {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// 创建单例实例
const apiService = new ApiService();

// 普通HTTP请求方法
export const httpGet = async (url, params = {}) => {
  try {
    const queryString = new URLSearchParams(params).toString();
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    const response = await fetch(fullUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP错误! 状态码: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('GET请求失败:', error);
    throw error;
  }
};

export const httpPost = async (url, data = {}) => {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP错误! 状态码: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('POST请求失败:', error);
    throw error;
  }
};

export default apiService;
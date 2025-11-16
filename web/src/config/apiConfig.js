// API配置文件

// 根据环境确定API基础URL
const isProduction = process.env.NODE_ENV === 'production';

// 生产环境的API URL（需要根据实际部署情况修改）
// 这里使用Vercel作为后端API托管服务的示例
const API_BASE_URL = isProduction 
  ? 'https://scientific-achievement-api.vercel.app' 
  : 'http://localhost:8000';

// API端点配置
export const API_ENDPOINTS = {
  ANALYZE: '/analyze',
  RESULT: '/result',
  HEALTH: '/health',
  CONFIG: '/config'
};

// 创建完整的API URL
export const getApiUrl = (endpoint) => {
  // 如果是开发环境，使用相对路径，让Vite代理处理
  if (!isProduction) {
    return `/api${endpoint}`;
  }
  // 生产环境直接使用完整URL
  return `${API_BASE_URL}${endpoint}`;
};

// API请求超时时间（毫秒）
export const API_TIMEOUT = 30000;

// 是否启用模拟数据（用于离线开发或演示）
export const USE_MOCK_DATA = false;

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  getApiUrl,
  API_TIMEOUT,
  USE_MOCK_DATA
};
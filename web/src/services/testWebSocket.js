// WebSocket连接测试脚本
// 这个文件用于测试WebSocket连接是否正常工作

import { API_CONFIG } from '../config/apiConfig';

export async function testWebSocketConnection() {
  return new Promise((resolve, reject) => {
    console.log('开始测试WebSocket连接...');
    
    // 生成随机客户端ID
    const clientId = `test-client-${Date.now()}`;
    
    // 构建WebSocket URL
    const wsUrl = `${API_CONFIG.WS_BASE_URL}${API_CONFIG.WS_ENDPOINTS.CHAT}/${clientId}`;
    console.log(`连接到: ${wsUrl}`);
    
    // 创建WebSocket连接
    const ws = new WebSocket(wsUrl);
    
    // 设置超时
    const timeout = setTimeout(() => {
      ws.close();
      reject(new Error('WebSocket连接超时'));
    }, 10000);
    
    // 连接打开事件
    ws.onopen = () => {
      console.log('WebSocket连接已建立');
      
      // 发送测试消息
      const testMessage = '这是一条测试消息';
      console.log(`发送测试消息: ${testMessage}`);
      ws.send(testMessage);
    };
    
    // 接收消息事件
    let receivedMessages = 0;
    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        console.log('收到消息:', message);
        
        receivedMessages++;
        
        // 期望收到两条消息：欢迎消息和回复消息
        if (receivedMessages >= 2) {
          clearTimeout(timeout);
          ws.close();
          resolve({
            success: true,
            message: 'WebSocket连接测试成功！'
          });
        }
      } catch (error) {
        console.error('解析消息时出错:', error);
      }
    };
    
    // 连接关闭事件
    ws.onclose = (event) => {
      console.log(`WebSocket连接已关闭，代码: ${event.code}, 原因: ${event.reason}`);
      if (!timeout) return;
      clearTimeout(timeout);
      
      if (receivedMessages < 2) {
        reject(new Error(`WebSocket连接已关闭，但未收到预期的所有消息。仅收到 ${receivedMessages} 条消息。`));
      }
    };
    
    // 错误事件
    ws.onerror = (error) => {
      console.error('WebSocket错误:', error);
      clearTimeout(timeout);
      ws.close();
      reject(new Error(`WebSocket连接错误: ${error.message || '未知错误'}`));
    };
  });
}

// 如果直接运行此脚本
if (typeof window !== 'undefined') {
  // 仅在浏览器环境中自动运行测试
  window.testWebSocket = testWebSocketConnection;
  console.log('WebSocket测试函数已添加到window对象');
  console.log('可以通过调用 testWebSocket() 来手动测试连接');
}

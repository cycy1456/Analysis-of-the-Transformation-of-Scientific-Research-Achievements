// WebSocket连接自定义Hook
import { useState, useEffect, useCallback, useRef } from 'react';
import apiService from '../services/api';

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const isMountedRef = useRef(true);

  // 处理连接状态变化
  const handleConnectionChange = useCallback((connected) => {
    if (isMountedRef.current) {
      setIsConnected(connected);
    }
  }, []);

  // 处理接收到的消息
  const handleMessage = useCallback((data) => {
    if (isMountedRef.current) {
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: data.content || '',
        sender: 'bot',
        timestamp: data.timestamp || new Date().toISOString()
      }]);
    }
  }, []);

  // 初始化WebSocket连接
  useEffect(() => {
    isMountedRef.current = true;
    
    // 注册事件处理器
    apiService.onConnectionChange(handleConnectionChange);
    apiService.onMessage(handleMessage);
    
    // 尝试连接
    const initConnection = async () => {
      try {
        setIsLoading(true);
        setError(null);
        await apiService.connect();
      } catch (err) {
        if (isMountedRef.current) {
          setError('WebSocket连接失败，请稍后重试');
          console.error('WebSocket初始化连接失败:', err);
        }
      } finally {
        if (isMountedRef.current) {
          setIsLoading(false);
        }
      }
    };
    
    initConnection();
    
    // 清理函数
    return () => {
      isMountedRef.current = false;
      apiService.offConnectionChange(handleConnectionChange);
      apiService.offMessage(handleMessage);
    };
  }, [handleConnectionChange, handleMessage]);

  // 发送消息
  const sendMessage = useCallback(async (message) => {
    if (!message.trim()) return;
    
    // 添加用户消息到本地
    const userMessage = {
      id: Date.now(),
      text: message.trim(),
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    try {
      setIsLoading(true);
      setError(null);
      await apiService.sendMessage(message.trim());
    } catch (err) {
      if (isMountedRef.current) {
        setError('发送消息失败，请稍后重试');
        console.error('发送消息失败:', err);
      }
    } finally {
      if (isMountedRef.current) {
        setIsLoading(false);
      }
    }
  }, []);

  // 重新连接
  const reconnect = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      await apiService.connect();
    } catch (err) {
      if (isMountedRef.current) {
        setError('重新连接失败，请稍后重试');
        console.error('WebSocket重新连接失败:', err);
      }
    } finally {
      if (isMountedRef.current) {
        setIsLoading(false);
      }
    }
  }, []);

  // 断开连接
  const disconnect = useCallback(() => {
    apiService.disconnect();
    setIsConnected(false);
    setMessages([]);
  }, []);

  return {
    isConnected,
    messages,
    isLoading,
    error,
    sendMessage,
    reconnect,
    disconnect
  };
};

export default useWebSocket;
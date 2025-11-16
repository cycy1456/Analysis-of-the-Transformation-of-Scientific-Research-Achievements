import React, { useState, useEffect } from 'react'
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  CircularProgress,
  Card,
  CardContent,
  useMediaQuery,
  useTheme,
  Alert,
  ButtonGroup
} from '@mui/material'
import SendIcon from '@mui/icons-material/Send'
import MessageIcon from '@mui/icons-material/Message'
import HelpIcon from '@mui/icons-material/Help'
import RefreshIcon from '@mui/icons-material/Refresh'
import WifiOffIcon from '@mui/icons-material/WifiOff'
import WifiIcon from '@mui/icons-material/Wifi'
import { useWebSocket } from '../hooks/useWebSocket'

function ChatPage() {
  const [inputMessage, setInputMessage] = useState('')
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))
  
  // 使用WebSocket Hook
  const {
    isConnected,
    messages,
    isLoading,
    error,
    sendMessage,
    reconnect,
    disconnect
  } = useWebSocket()

  // 检测连接状态变化
  useEffect(() => {
    if (isConnected) {
      console.log('WebSocket连接成功');
    } else {
      console.log('WebSocket连接断开');
    }
  }, [isConnected])

  // 处理发送消息
  const handleSendMessage = () => {
    if (!inputMessage.trim()) return
    
    // 保存输入内容，因为我们会清空输入框
    const message = inputMessage.trim();
    
    // 清空输入框
    setInputMessage('')
    
    // 发送消息
    sendMessage(message)
  }

  // 处理按键事件
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <Container maxWidth={isMobile ? 'xs' : 'md'} sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        科研成果转化咨询
      </Typography>
      <Typography variant="subtitle1" color="textSecondary" align="center" sx={{ mb: 4 }}>
        直接在网页中与智能体对话，获取科研成果转化相关建议
      </Typography>
      
      {/* 连接状态提示 */}
      {!isConnected && (
        <Alert 
          severity="warning" 
          icon={<WifiOffIcon />}
          action={
            <ButtonGroup size="small">
              <Button onClick={reconnect} startIcon={<RefreshIcon />}>重新连接</Button>
              <Button onClick={disconnect} variant="outlined" startIcon={<WifiOffIcon />}>断开</Button>
            </ButtonGroup>
          }
          sx={{ mb: 3 }}
        >
          连接已断开，无法进行实时对话
        </Alert>
      )}
      
      {/* 错误提示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* 聊天容器 */}
      <Paper elevation={3} sx={{ height: '70vh', display: 'flex', flexDirection: 'column' }}>
        {/* 聊天记录区域 */}
        <Box sx={{ flexGrow: 1, overflowY: 'auto', p: 3, bgcolor: '#f9f9f9' }}>
          <List sx={{ maxWidth: '100%' }}>
            {messages.map((message) => (
              <ListItem 
                key={message.id} 
                alignItems="flex-start"
                sx={{ 
                  justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                  flexDirection: message.sender === 'user' ? 'row-reverse' : 'row'
                }}
              >
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: message.sender === 'user' ? 'primary.main' : 'secondary.main' }}>
                    {message.sender === 'user' ? <MessageIcon /> : <HelpIcon />}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText 
                  primary={
                    <Card 
                      sx={{ 
                        maxWidth: '70%',
                        bgcolor: message.sender === 'user' ? 'primary.light' : 'background.paper',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                      }}
                    >
                      <CardContent>
                        <Typography variant="body1" sx={{ wordBreak: 'break-word' }}>
                          {message.text}
                        </Typography>
                      </CardContent>
                    </Card>
                  }
                />
              </ListItem>
            ))}
            {isLoading && (
              <ListItem alignItems="flex-start" sx={{ justifyContent: 'flex-start' }}>
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: 'secondary.main' }}>
                    <HelpIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText 
                  primary={
                    <Card sx={{ maxWidth: '50%', bgcolor: 'background.paper' }}>
                      <CardContent>
                        <Box display="flex" justifyContent="center" py={2}>
                          <CircularProgress size={24} />
                        </Box>
                      </CardContent>
                    </Card>
                  }
                />
              </ListItem>
            )}
          </List>
        </Box>

        {/* 输入区域 */}
        <Box sx={{ p: 2, borderTop: '1px solid #e0e0e0', bgcolor: 'background.paper' }}>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            {/* 连接状态指示器 */}
            <Box sx={{ mr: -1 }}>
              <Box
                sx={{
                  width: 10,
                  height: 10,
                  borderRadius: '50%',
                  bgcolor: isConnected ? 'success.main' : 'error.main',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  position: 'relative',
                  '&::after': {
                    content: '""',
                    position: 'absolute',
                    width: '100%',
                    height: '100%',
                    borderRadius: '50%',
                    bgcolor: isConnected ? 'success.main' : 'error.main',
                    opacity: 0.5,
                    animation: isConnected ? 'pulse 2s infinite' : 'none'
                  },
                  '@keyframes pulse': {
                    '0%': {
                      transform: 'scale(1)',
                      opacity: 0.5
                    },
                    '100%': {
                      transform: 'scale(2)',
                      opacity: 0
                    }
                  }
                }}
              />
            </Box>
            
            <TextField
              fullWidth
              variant="outlined"
              placeholder={isConnected ? "输入您的问题..." : "请先连接服务器..."}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              multiline
              rows={1}
              maxRows={3}
              disabled={!isConnected}
              InputProps={{
                disableUnderline: true,
                sx: { 
                  bgcolor: isConnected ? '#f5f5f5' : '#f0f0f0', 
                  borderRadius: 2,
                  opacity: isConnected ? 1 : 0.7
                }
              }}
            />
            <Button
              variant="contained"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading || !isConnected}
              endIcon={<SendIcon />}
              sx={{ minWidth: '56px', height: '56px', borderRadius: '50%' }}
            >
              {isLoading ? <CircularProgress size={24} color="inherit" /> : null}
            </Button>
          </Box>
          <Box sx={{ mt: 2 }}>
            <Typography variant="caption" color="textSecondary">
              提示：您可以咨询关于科研成果转化的问题，如"什么是科研成果转化"、"如何使用分析系统"等
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* 快捷操作提示 */}
      <Box sx={{ mt: 4, textAlign: 'center' }}>
        <Typography variant="body2" color="textSecondary">
          需要更详细的分析？可以尝试以下关键词：
        </Typography>
        <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
          {[
            '如何使用这个系统',
            '什么是科研成果转化',
            '可以分析哪些类型的科研成果',
            '分析结果有多准确',
            '如何提高转化成功率'
          ].map((keyword) => (
            <Button
              key={keyword}
              variant="outlined"
              size="small"
              onClick={() => {
                setInputMessage(keyword)
              }}
              disabled={!isConnected}
              sx={{ 
                fontSize: '0.75rem', 
                borderRadius: 1,
                opacity: isConnected ? 1 : 0.7
              }}
            >
              {keyword}
            </Button>
          ))}
        </Box>
      </Box>
    </Container>
  )
}

export default ChatPage
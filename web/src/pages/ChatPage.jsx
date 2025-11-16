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
  useTheme
} from '@mui/material'
import SendIcon from '@mui/icons-material/Send'
import MessageIcon from '@mui/icons-material/Message'
import HelpIcon from '@mui/icons-material/Help'
import { mockChatResponses } from '../config/mockData'

function ChatPage() {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

  // 初始欢迎消息
  useEffect(() => {
    const welcomeMessage = {
      id: 1,
      text: '您好！我是科研成果转化分析智能体，很高兴为您提供服务。您可以咨询关于科研成果转化的问题，或者点击"开始分析"获取详细的成果评估。',
      sender: 'bot'
    }
    setMessages([welcomeMessage])
  }, [])

  // 处理发送消息
  const handleSendMessage = () => {
    if (!inputMessage.trim()) return

    // 添加用户消息
    const userMessage = {
      id: Date.now(),
      text: inputMessage.trim(),
      sender: 'user'
    }
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    // 模拟AI响应延迟
    setTimeout(() => {
      // 根据用户输入查找最匹配的响应
      let botResponseText = mockChatResponses['默认']
      
      // 尝试找到精确匹配
      Object.keys(mockChatResponses).forEach(key => {
        if (inputMessage.toLowerCase().includes(key.toLowerCase())) {
          botResponseText = mockChatResponses[key]
        }
      })

      // 添加AI响应
      const botMessage = {
        id: Date.now() + 1,
        text: botResponseText,
        sender: 'bot'
      }
      setMessages(prev => [...prev, botMessage])
      setIsLoading(false)
    }, 800)
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
          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="输入您的问题..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              multiline
              rows={1}
              maxRows={3}
              InputProps={{
                disableUnderline: true,
                sx: { bgcolor: '#f5f5f5', borderRadius: 2 }
              }}
            />
            <Button
              variant="contained"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
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
          {Object.keys(mockChatResponses).filter(key => key !== '默认').map((keyword) => (
            <Button
              key={keyword}
              variant="outlined"
              size="small"
              onClick={() => {
                setInputMessage(keyword)
              }}
              sx={{ fontSize: '0.75rem', borderRadius: 1 }}
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
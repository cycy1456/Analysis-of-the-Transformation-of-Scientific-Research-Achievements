import React, { useState } from 'react'
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  RadioGroup,
  Radio,
  FormControlLabel,
  FormControl,
  FormLabel,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Snackbar
} from '@mui/material'
import UploadIcon from '@mui/icons-material/Upload'
import SendIcon from '@mui/icons-material/Send'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { API_ENDPOINTS, getApiUrl, API_TIMEOUT, USE_MOCK_DATA } from '../config/apiConfig'

function AnalysisPage() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    field: '',
    maturity: '实验室',
    keywords: '',
    teamSize: '',
    investmentNeeds: '',
    patentStatus: '已有专利',
    expectedOutcome: '技术转让'
  })

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue)
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleFileUpload = (e) => {
    // 模拟文件上传处理
    console.log('File uploaded:', e.target.files[0]?.name)
    setSuccess('文件上传成功')
    setTimeout(() => setSuccess(''), 3000)
  }

  const validateForm = () => {
    if (!formData.title.trim()) {
      setError('请输入成果名称')
      return false
    }
    if (!formData.description.trim()) {
      setError('请输入成果描述')
      return false
    }
    if (!formData.field.trim()) {
      setError('请输入所属领域')
      return false
    }
    return true
  }

  const handleSubmit = async () => {
    if (!validateForm()) return

    setLoading(true)
    setError('')

    try {
      // 构建请求数据
      const requestData = {
        title: formData.title,
        description: formData.description,
        field: formData.field,
        maturity: formData.maturity,
        keywords: formData.keywords,
        teamSize: formData.teamSize,
        investmentNeeds: formData.investmentNeeds,
        patentStatus: formData.patentStatus,
        expectedOutcome: formData.expectedOutcome
      };

      let session_id;
      
      if (USE_MOCK_DATA) {
        // 使用模拟数据
        console.log('使用模拟数据进行演示');
        session_id = `mock-${Date.now()}`;
        // 模拟延迟
        await new Promise(resolve => setTimeout(resolve, 1000));
      } else {
        // 实际API调用
        const apiUrl = getApiUrl(API_ENDPOINTS.ANALYZE);
        const response = await axios.post(apiUrl, requestData, {
          timeout: API_TIMEOUT,
          headers: {
            'Content-Type': 'application/json'
          }
        });
        session_id = response.data.session_id;
      }

      // 导航到结果页面
      navigate(`/result/${session_id}`);
    } catch (err) {
      setError('分析过程中出现错误，请重试')
      console.error('分析错误:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Button 
          variant="outlined" 
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
        >
          返回首页
        </Button>
      </Box>

      <Typography variant="h4" component="h1" gutterBottom>
        科研成果分析
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        填写以下信息，让我们为您的科研成果提供专业的转化分析和建议
      </Typography>

      <Paper elevation={3} sx={{ p: 4, mb: 6 }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{ mb: 4 }}
        >
          <Tab label="基本信息" />
          <Tab label="技术详情" />
          <Tab label="市场与转化" />
          <Tab label="上传文件" />
        </Tabs>

        {activeTab === 0 && (
          <Box>
            <TextField
              fullWidth
              label="成果名称"
              name="title"
              value={formData.title}
              onChange={handleChange}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="成果描述"
              name="description"
              value={formData.description}
              onChange={handleChange}
              margin="normal"
              required
              multiline
              rows={4}
            />
            <TextField
              fullWidth
              label="所属领域"
              name="field"
              value={formData.field}
              onChange={handleChange}
              margin="normal"
              required
              placeholder="例如：人工智能、生物医药、新能源等"
            />
            <FormControl component="fieldset" margin="normal">
              <FormLabel component="legend">技术成熟度</FormLabel>
              <RadioGroup 
                row 
                name="maturity" 
                value={formData.maturity} 
                onChange={handleChange}
              >
                <FormControlLabel value="实验室" control={<Radio />} label="实验室" />
                <FormControlLabel value="小试" control={<Radio />} label="小试" />
                <FormControlLabel value="中试" control={<Radio />} label="中试" />
                <FormControlLabel value="产业化" control={<Radio />} label="产业化" />
              </RadioGroup>
            </FormControl>
          </Box>
        )}

        {activeTab === 1 && (
          <Box>
            <TextField
              fullWidth
              label="关键词"
              name="keywords"
              value={formData.keywords}
              onChange={handleChange}
              margin="normal"
              placeholder="请输入3-5个关键词，用逗号分隔"
            />
            <TextField
              fullWidth
              label="团队规模"
              name="teamSize"
              value={formData.teamSize}
              onChange={handleChange}
              margin="normal"
              placeholder="例如：5人，10人团队等"
            />
            <FormControl component="fieldset" margin="normal">
              <FormLabel component="legend">专利情况</FormLabel>
              <RadioGroup 
                row 
                name="patentStatus" 
                value={formData.patentStatus} 
                onChange={handleChange}
              >
                <FormControlLabel value="已有专利" control={<Radio />} label="已有专利" />
                <FormControlLabel value="申请中" control={<Radio />} label="申请中" />
                <FormControlLabel value="暂无专利" control={<Radio />} label="暂无专利" />
              </RadioGroup>
            </FormControl>
          </Box>
        )}

        {activeTab === 2 && (
          <Box>
            <TextField
              fullWidth
              label="资金需求"
              name="investmentNeeds"
              value={formData.investmentNeeds}
              onChange={handleChange}
              margin="normal"
              placeholder="例如：100万，500万等"
            />
            <FormControl component="fieldset" margin="normal">
              <FormLabel component="legend">预期转化方式</FormLabel>
              <RadioGroup 
                name="expectedOutcome" 
                value={formData.expectedOutcome} 
                onChange={handleChange}
              >
                <FormControlLabel value="技术转让" control={<Radio />} label="技术转让" />
                <FormControlLabel value="合作开发" control={<Radio />} label="合作开发" />
                <FormControlLabel value="自主创业" control={<Radio />} label="自主创业" />
                <FormControlLabel value="授权使用" control={<Radio />} label="授权使用" />
              </RadioGroup>
            </FormControl>
          </Box>
        )}

        {activeTab === 3 && (
          <Box sx={{ textAlign: 'center' }}>
            <Box
              sx={{
                border: '2px dashed #ccc',
                borderRadius: 2,
                p: 6,
                mb: 4,
                cursor: 'pointer',
                '&:hover': {
                  borderColor: 'primary.main',
                  backgroundColor: 'primary.light'
                }
              }}
              onClick={() => document.getElementById('fileInput').click()}
            >
              <UploadIcon fontSize="large" color="primary" />
              <Typography variant="h6" gutterBottom>
                点击上传文件
              </Typography>
              <Typography variant="body2" color="text.secondary">
                支持PDF、Word、PPT等格式，最大50MB
              </Typography>
              <input
                id="fileInput"
                type="file"
                style={{ display: 'none' }}
                onChange={handleFileUpload}
              />
            </Box>
            <Typography variant="body2" color="text.secondary">
              上传文件可帮助我们提供更精准的分析结果
            </Typography>
          </Box>
        )}

        <Box sx={{ display: 'flex', gap: 2, mt: 4, justifyContent: 'space-between' }}>
          {activeTab > 0 && (
            <Button 
              variant="outlined" 
              onClick={() => setActiveTab(activeTab - 1)}
            >
              上一步
            </Button>
          )}
          <Box sx={{ ml: 'auto' }}>
            {activeTab < 3 ? (
              <Button 
                variant="contained" 
                onClick={() => setActiveTab(activeTab + 1)}
              >
                下一步
              </Button>
            ) : (
              <Button 
                variant="contained" 
                onClick={handleSubmit}
                disabled={loading}
                endIcon={<SendIcon />}
                sx={{ px: 4 }}
              >
                {loading ? (
                  <>
                    <CircularProgress size={24} sx={{ mr: 1 }} />
                    分析中...
                  </>
                ) : (
                  '开始分析'
                )}
              </Button>
            )}
          </Box>
        </Box>
      </Paper>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError('')}
      >
        <Alert onClose={() => setError('')} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>

      <Snackbar
        open={!!success}
        autoHideDuration={3000}
        onClose={() => setSuccess('')}
      >
        <Alert onClose={() => setSuccess('')} severity="success" sx={{ width: '100%' }}>
          {success}
        </Alert>
      </Snackbar>
    </Container>
  )
}

export default AnalysisPage
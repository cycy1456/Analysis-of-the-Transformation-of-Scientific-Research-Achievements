import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Container,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Paper
} from '@mui/material'
import ArrowRightIcon from '@mui/icons-material/ArrowRight'
import FileUploadIcon from '@mui/icons-material/FileUpload'
import DescriptionIcon from '@mui/icons-material/Description'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import LightbulbIcon from '@mui/icons-material/Lightbulb'

function HomePage() {
  const navigate = useNavigate()

  const handleStartAnalysis = () => {
    navigate('/analysis')
  }

  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      {/* 页面标题 */}
      <Box textAlign="center" sx={{ mb: 8 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          科研成果转化分析智能体
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          自动化分析工具，助力科研成果快速转化为市场价值
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={handleStartAnalysis}
          endIcon={<ArrowRightIcon />}
          sx={{ mt: 4 }}
        >
          开始分析
        </Button>
      </Box>

      {/* 功能特点 */}
      <Grid container spacing={4} sx={{ mb: 12 }}>
        <Grid item xs={12} md={3}>
          <Card raised sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent>
              <Box sx={{ 
                width: 60, 
                height: 60, 
                borderRadius: '50%', 
                bgcolor: 'primary.light', 
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mb: 3
              }}>
                <FileUploadIcon fontSize="large" />
              </Box>
              <Typography variant="h6" gutterBottom>
                文档识别
              </Typography>
              <Typography color="text.secondary">
                智能识别和解析科研文档内容，提取关键信息和数据
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card raised sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent>
              <Box sx={{ 
                width: 60, 
                height: 60, 
                borderRadius: '50%', 
                bgcolor: 'secondary.light', 
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mb: 3
              }}>
                <DescriptionIcon fontSize="large" />
              </Box>
              <Typography variant="h6" gutterBottom>
                专利查询
              </Typography>
              <Typography color="text.secondary">
                自动查询相关领域专利情况，提供知识产权保护建议
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card raised sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent>
              <Box sx={{ 
                width: 60, 
                height: 60, 
                borderRadius: '50%', 
                bgcolor: 'success.light', 
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mb: 3
              }}>
                <TrendingUpIcon fontSize="large" />
              </Box>
              <Typography variant="h6" gutterBottom>
                市场分析
              </Typography>
              <Typography color="text.secondary">
                深入分析市场潜力和竞争格局，评估转化可行性
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card raised sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent>
              <Box sx={{ 
                width: 60, 
                height: 60, 
                borderRadius: '50%', 
                bgcolor: 'warning.light', 
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mb: 3
              }}>
                <LightbulbIcon fontSize="large" />
              </Box>
              <Typography variant="h6" gutterBottom>
                转化建议
              </Typography>
              <Typography color="text.secondary">
                提供个性化的转化策略和实施路径，最大化商业价值
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 工作流程 */}
      <Paper elevation={3} sx={{ p: 6, mb: 8 }}>
        <Typography variant="h4" component="h2" gutterBottom sx={{ mb: 4 }}>
          简单三步，完成分析
        </Typography>
        <Grid container spacing={6}>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Box sx={{ 
                width: 80, 
                height: 80, 
                borderRadius: '50%', 
                bgcolor: 'primary.main', 
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mx: 'auto',
                mb: 3,
                fontSize: 28,
                fontWeight: 'bold'
              }}>
                1
              </Box>
              <Typography variant="h6" gutterBottom>
                输入信息
              </Typography>
              <Typography color="text.secondary">
                填写科研成果基本信息，上传相关文档
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Box sx={{ 
                width: 80, 
                height: 80, 
                borderRadius: '50%', 
                bgcolor: 'secondary.main', 
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mx: 'auto',
                mb: 3,
                fontSize: 28,
                fontWeight: 'bold'
              }}>
                2
              </Box>
              <Typography variant="h6" gutterBottom>
                自动分析
              </Typography>
              <Typography color="text.secondary">
                系统自动执行分析流程，生成详细报告
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Box sx={{ 
                width: 80, 
                height: 80, 
                borderRadius: '50%', 
                bgcolor: 'success.main', 
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mx: 'auto',
                mb: 3,
                fontSize: 28,
                fontWeight: 'bold'
              }}>
                3
              </Box>
              <Typography variant="h6" gutterBottom>
                获取结果
              </Typography>
              <Typography color="text.secondary">
                查看分析结果和转化建议，下载完整报告
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* CTA */}
      <Box textAlign="center">
        <Button
          variant="contained"
          size="large"
          onClick={handleStartAnalysis}
          endIcon={<ArrowRightIcon />}
          sx={{ 
            py: 1.5, 
            px: 6, 
            fontSize: 16 
          }}
        >
          立即开始分析
        </Button>
      </Box>
    </Container>
  )
}

export default HomePage
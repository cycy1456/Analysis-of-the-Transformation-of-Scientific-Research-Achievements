import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Button,
  Divider,
  Grid,
  Card,
  CardContent,
  CardHeader
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API_ENDPOINTS, getApiUrl, API_TIMEOUT, USE_MOCK_DATA } from '../config/apiConfig';

function ResultPage() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(0);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshInterval, setRefreshInterval] = useState(null);

  // 模拟数据（用于演示）
  const getMockResult = () => ({
    session_id: sessionId,
    status: 'completed',
    market_analysis: {
      market_size: '该领域市场规模预计达到100亿元，年增长率约15%',
      competition: '市场竞争格局清晰，目前有3-5家主要竞争对手',
      commercial_potential: '高潜力，预计3年内可实现产业化',
      detailed_analysis: '基于市场调研和行业趋势分析，该技术在医疗健康领域具有广阔的应用前景，尤其是在精准医疗和个性化治疗方面。'
    },
    patent_analysis: {
      protection_strategy: '建议申请PCT国际专利，扩大保护范围',
      risk_assessment: '低风险，未发现核心技术侵权风险',
      detailed_analysis: '专利检索显示，该技术路线具有创新性，与现有专利存在明显区别，建议围绕核心技术构建专利池。'
    },
    transfer_strategy: {
      recommended_path: '技术转让',
      timeline: '建议6-12个月完成技术转让',
      key_factors: '核心技术的成熟度和团队支持是关键成功因素',
      detailed_strategy: '建议采用分阶段技术转让模式，第一阶段提供核心技术授权，第二阶段提供技术支持和人才培训。'
    },
    summary: '综合评估显示，该科研成果具有较高的市场价值和转化潜力。建议通过技术转让的方式实现产业化，预计3年内可产生显著的经济效益和社会效益。'
  });

  // 获取分析结果
  const fetchResult = async () => {
    try {
      setError(null);
      
      let result;
      if (USE_MOCK_DATA || !sessionId || sessionId.startsWith('mock-')) {
        // 使用模拟数据
        console.log('使用模拟分析结果进行演示');
        await new Promise(resolve => setTimeout(resolve, 1000));
        result = getMockResult();
      } else {
        // 实际API调用
        const apiUrl = getApiUrl(`${API_ENDPOINTS.RESULT}/${sessionId}`);
        const response = await axios.get(apiUrl, {
          timeout: API_TIMEOUT
        });
        result = response.data;
      }

      setAnalysisResult(result);

      // 如果分析仍在进行中，继续轮询
      if (result.status === 'processing') {
        if (!refreshInterval) {
          const interval = setInterval(fetchResult, 3000); // 每3秒刷新一次
          setRefreshInterval(interval);
        }
      } else {
        // 分析完成或出错，停止轮询
        if (refreshInterval) {
          clearInterval(refreshInterval);
          setRefreshInterval(null);
        }
        setLoading(false);
      }
    } catch (err) {
      console.error('获取分析结果失败:', err);
      setError('获取分析结果失败，请稍后重试');
      setLoading(false);
      
      // 停止轮询
      if (refreshInterval) {
        clearInterval(refreshInterval);
        setRefreshInterval(null);
      }
    }
  };

  useEffect(() => {
    fetchResult();

    // 清理函数
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, [sessionId]);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleBackToHome = () => {
    navigate('/');
  };

  const handleNewAnalysis = () => {
    navigate('/analysis');
  };

  // 渲染内容区域
  const renderContent = () => {
    if (loading) {
      return (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" py={8}>
          <CircularProgress size={60} thickness={4} />
          <Typography variant="h6" mt={4} color="textSecondary">
            正在分析中，请稍候...
          </Typography>
          <Typography variant="body2" mt={2} color="textSecondary">
            分析过程可能需要1-2分钟时间
          </Typography>
        </Box>
      );
    }

    if (error) {
      return (
        <Alert severity="error" sx={{ my: 4 }}>
          {error}
        </Alert>
      );
    }

    if (!analysisResult || analysisResult.status === 'error') {
      return (
        <Alert severity="error" sx={{ my: 4 }}>
          {analysisResult?.error || '分析过程中出现错误，请稍后重试'}
        </Alert>
      );
    }

    return (
      <Box>
        {/* 结果概览 */}
        <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            分析结果概览
          </Typography>
          <Typography variant="body1" paragraph>
            {analysisResult.summary || '暂无分析总结'}
          </Typography>
        </Paper>

        {/* 详细结果标签页 */}
        <Box sx={{ width: '100%', bgcolor: 'background.paper' }}>
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            variant="scrollable"
            scrollButtons="auto"
            sx={{ mb: 3 }}
          >
            <Tab label="市场分析" />
            <Tab label="专利分析" />
            <Tab label="转化策略" />
          </Tabs>

          {/* 市场分析内容 */}
          {activeTab === 0 && (
            <Box sx={{ p: 2 }}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardHeader title="市场规模" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.market_analysis?.market_size || '暂无数据'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardHeader title="竞争分析" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.market_analysis?.competition || '暂无数据'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12}>
                  <Card>
                    <CardHeader title="详细分析" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.market_analysis?.detailed_analysis || '暂无详细分析'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}

          {/* 专利分析内容 */}
          {activeTab === 1 && (
            <Box sx={{ p: 2 }}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardHeader title="保护策略" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.patent_analysis?.protection_strategy || '暂无数据'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardHeader title="风险评估" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.patent_analysis?.risk_assessment || '暂无数据'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12}>
                  <Card>
                    <CardHeader title="详细分析" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.patent_analysis?.detailed_analysis || '暂无详细分析'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}

          {/* 转化策略内容 */}
          {activeTab === 2 && (
            <Box sx={{ p: 2 }}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardHeader title="推荐路径" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.transfer_strategy?.recommended_path || '暂无数据'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardHeader title="时间线" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.transfer_strategy?.timeline || '暂无数据'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12}>
                  <Card>
                    <CardHeader title="详细策略" />
                    <CardContent>
                      <Typography variant="body1">
                        {analysisResult.transfer_strategy?.detailed_strategy || '暂无详细策略'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}
        </Box>
      </Box>
    );
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        科研成果分析结果
      </Typography>
      
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="subtitle1" color="textSecondary">
          会话ID: {sessionId}
        </Typography>
      </Box>

      {renderContent()}

      <Box sx={{ mt: 6, display: 'flex', justifyContent: 'center', gap: 2 }}>
        <Button variant="outlined" onClick={handleBackToHome}>
          返回首页
        </Button>
        <Button variant="contained" onClick={handleNewAnalysis}>
          开始新分析
        </Button>
      </Box>
    </Container>
  );
}

export default ResultPage;
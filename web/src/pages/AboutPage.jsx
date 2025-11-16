import React from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import SettingsIcon from '@mui/icons-material/Settings';

function AboutPage() {
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        关于科研成果转化智能体
      </Typography>

      {/* 简介部分 */}
      <Paper elevation={2} sx={{ p: 4, mb: 6 }}>
        <Typography variant="body1" paragraph>
          科研成果转化智能体是一款基于人工智能技术的创新工具，旨在帮助科研人员、高校和研究机构快速评估科研成果的市场潜力、专利状况和转化路径。
        </Typography>
        <Typography variant="body1" paragraph>
          本平台通过先进的AI分析算法，为用户提供全面、客观的科研成果评估，助力科研成果从实验室走向市场，实现知识的价值转化。
        </Typography>
      </Paper>

      {/* 功能特点 */}
      <Typography variant="h5" gutterBottom sx={{ mb: 4 }}>
        功能特点
      </Typography>
      
      <Grid container spacing={4} sx={{ mb: 8 }}>
        <Grid item xs={12} md={6}>
          <Card elevation={1}>
            <CardHeader 
              avatar={<LightbulbIcon color="primary" />}
              title="市场潜力分析"
            />
            <CardContent>
              <Typography variant="body2" color="textSecondary">
                基于海量市场数据和行业趋势，对科研成果的市场规模、竞争格局和商业化潜力进行深入分析。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={1}>
            <CardHeader 
              avatar={<FileCopyIcon color="primary" />}
              title="专利状况评估"
            />
            <CardContent>
              <Typography variant="body2" color="textSecondary">
                分析相关技术领域的专利布局，提供知识产权风险评估和保护策略建议。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={1}>
            <CardHeader 
              avatar={<TrendingUpIcon color="primary" />}
              title="转化路径规划"
            />
            <CardContent>
              <Typography variant="body2" color="textSecondary">
                根据技术成熟度和市场需求，制定个性化的成果转化策略，包括技术转让、产学研合作等多种模式。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card elevation={1}>
            <CardHeader 
              avatar={<SettingsIcon color="primary" />}
              title="智能分析引擎"
            />
            <CardContent>
              <Typography variant="body2" color="textSecondary">
                利用先进的自然语言处理和机器学习技术，实现对科研成果的智能评估和分析。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 技术架构 */}
      <Paper elevation={2} sx={{ p: 4, mb: 6 }}>
        <Typography variant="h5" gutterBottom>
          技术架构
        </Typography>
        <Divider sx={{ mb: 3 }} />
        <Typography variant="subtitle1" sx={{ mb: 2 }}>
          核心技术组件：
        </Typography>
        <Grid container spacing={2}>
          <Grid item>
            <Chip label="React" color="primary" variant="outlined" />
          </Grid>
          <Grid item>
            <Chip label="FastAPI" color="primary" variant="outlined" />
          </Grid>
          <Grid item>
            <Chip label="MUI" color="primary" variant="outlined" />
          </Grid>
          <Grid item>
            <Chip label="Python" color="primary" variant="outlined" />
          </Grid>
          <Grid item>
            <Chip label="人工智能" color="primary" variant="outlined" />
          </Grid>
        </Grid>
      </Paper>

      {/* 使用指南 */}
      <Paper elevation={2} sx={{ p: 4, mb: 6 }}>
        <Typography variant="h5" gutterBottom>
          使用指南
        </Typography>
        <Divider sx={{ mb: 3 }} />
        <List>
          <ListItem>
            <ListItemIcon><InfoIcon fontSize="small" /></ListItemIcon>
            <ListItemText primary="填写基本信息" secondary="提供科研成果的标题、描述和所属领域" />
          </ListItem>
          <ListItem>
            <ListItemIcon><InfoIcon fontSize="small" /></ListItemIcon>
            <ListItemText primary="完善技术详情" secondary="描述技术成熟度、关键词和专利状况" />
          </ListItem>
          <ListItem>
            <ListItemIcon><InfoIcon fontSize="small" /></ListItemIcon>
            <ListItemText primary="设置转化目标" secondary="选择预期的转化方式和投资需求" />
          </ListItem>
          <ListItem>
            <ListItemIcon><InfoIcon fontSize="small" /></ListItemIcon>
            <ListItemText primary="提交分析请求" secondary="系统将进行全面分析并生成报告" />
          </ListItem>
        </List>
      </Paper>

      {/* 免责声明 */}
      <Paper elevation={1} sx={{ p: 3 }}>
        <Typography variant="subtitle1" color="textSecondary" gutterBottom>
          免责声明
        </Typography>
        <Typography variant="body2" color="textSecondary">
          本平台提供的分析结果仅供参考，不构成投资建议或商业决策依据。用户在进行科研成果转化时，应结合自身实际情况和专业评估做出决策。
        </Typography>
      </Paper>
    </Container>
  );
}

export default AboutPage;
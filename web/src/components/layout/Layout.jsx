import React from 'react'
import { Outlet } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Container,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  useMediaQuery,
  useTheme
} from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import HomeIcon from '@mui/icons-material/Home'
import FileUploadIcon from '@mui/icons-material/FileUpload'
import BarChartIcon from '@mui/icons-material/BarChart'
import InfoIcon from '@mui/icons-material/Info'
import MessageIcon from '@mui/icons-material/Message'
import { Link } from 'react-router-dom'

function Layout({ children }) {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const [mobileOpen, setMobileOpen] = React.useState(false)

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const menuItems = [
    { text: '首页', icon: <HomeIcon />, path: '/' },
    { text: '开始分析', icon: <FileUploadIcon />, path: '/analysis' },
    { text: '分析结果', icon: <BarChartIcon />, path: '/result' },
    { text: '在线咨询', icon: <MessageIcon />, path: '/chat' },
    { text: '关于我们', icon: <InfoIcon />, path: '/about' }
  ]

  const drawer = (
    <div>
      <Box sx={{ display: 'flex', alignItems: 'center', p: 2 }}>
        <Typography variant="h6" component="div">
          科研成果分析
        </Typography>
      </Box>
      <List>
        {menuItems.map((item, index) => (
          <ListItem 
            button 
            key={item.text}
            component={Link}
            to={item.path}
            onClick={() => setMobileOpen(false)}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </div>
  )

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* 顶部导航栏 */}
      <AppBar position="static">
        <Toolbar>
          {isMobile && (
            <IconButton
              edge="start"
              color="inherit"
              aria-label="menu"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            科研成果转化分析智能体
          </Typography>
          {!isMobile && (
            <Box sx={{ display: 'flex', gap: 2 }}>
              {menuItems.map((item) => (
                <Link
                  key={item.text}
                  to={item.path}
                  style={{ color: 'white', textDecoration: 'none' }}
                >
                  <Box sx={{ px: 2, py: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                    {item.icon}
                    <span>{item.text}</span>
                  </Box>
                </Link>
              ))}
            </Box>
          )}
        </Toolbar>
      </AppBar>

      {/* 移动端抽屉 */}
      <Box component="nav" sx={{ width: { md: 0 }, flexShrink: { md: 0 } }} aria-label="mailbox folders">
        <Drawer
          variant={isMobile ? "temporary" : "permanent"}
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
          }}
        >
          {drawer}
        </Drawer>
      </Box>

      {/* 主要内容 */}
      <Box component="main" sx={{ flexGrow: 1, py: 4 }}>
        <Container maxWidth="lg">
          <Outlet />
          {children}
        </Container>
      </Box>

      {/* 页脚 */}
      <Box component="footer" sx={{ bgcolor: 'primary.main', color: 'white', py: 3 }}>
        <Container maxWidth="lg">
          <Typography variant="body2" align="center">
            © {new Date().getFullYear()} 科研成果转化分析智能体 - 为科技创新赋能
          </Typography>
        </Container>
      </Box>
    </Box>
  )
}

export default Layout
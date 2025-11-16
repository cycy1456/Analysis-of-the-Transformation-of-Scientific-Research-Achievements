import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import HomePage from './pages/HomePage'
import AnalysisPage from './pages/AnalysisPage'
import ResultPage from './pages/ResultPage'
import AboutPage from './pages/AboutPage'
import ChatPage from './pages/ChatPage'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/result/:sessionId?" element={<ResultPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="*" element={<div style={{ padding: '2rem', textAlign: 'center' }}>页面不存在</div>} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
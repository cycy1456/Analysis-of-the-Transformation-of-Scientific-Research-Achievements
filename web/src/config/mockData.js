// 模拟数据配置

// 模拟分析结果数据
export const mockAnalysisResult = {
  status: 'success',
  sessionId: 'mock-session-123456',
  summary: '您的科研成果具有良好的市场转化潜力，建议通过合作开发模式推进产业化进程。',
  market_analysis: {
    market_size: '该领域市场规模预计在未来5年内将达到200亿元，年复合增长率约为15%。',
    competition: '市场竞争适中，主要竞争对手有3-5家，尚未形成垄断格局。',
    detailed_analysis: '根据您提供的信息，该技术在多个应用场景具有广阔前景。目前市场对该类技术的需求正在快速增长，特别是在智能制造、医疗健康等领域。建议重点关注这些高潜力市场，并根据目标客户需求优化产品功能。'
  },
  patent_analysis: {
    existing_patents: '已检索到相关专利约50项，主要集中在核心技术实现方面。',
    risk_assessment: '知识产权风险中等，建议进一步完善专利布局。',
    suggestions: '建议围绕核心技术点扩展专利保护范围，特别是应用层面的创新点。'
  },
  transformation_strategy: {
    recommended_approach: '合作开发',
    partnership_options: '可考虑与行业龙头企业建立战略合作，共同推进技术产业化。',
    implementation_steps: '1. 完善技术文档和样品\n2. 接触潜在合作伙伴\n3. 制定详细的合作方案\n4. 签署合作协议\n5. 共同推进产品开发和市场推广'
  }
};

// 模拟聊天响应数据
export const mockChatResponses = {
  '你好': '您好！我是科研成果转化分析智能体，很高兴为您提供服务。请问您有什么科研成果需要分析吗？',
  '如何使用这个系统': '使用本系统非常简单，您只需点击"开始分析"按钮，然后按照引导填写科研成果的相关信息，包括标题、描述、所属领域等，最后点击提交即可获得分析报告。',
  '什么是科研成果转化': '科研成果转化是指将科学研究和技术开发所产生的具有实用价值的成果转化为现实生产力的过程，包括技术转让、合作开发、自主创业等多种方式。',
  '可以分析哪些类型的科研成果': '本系统可以分析多种类型的科研成果，包括但不限于：信息技术、生物医药、新材料、新能源、智能制造等领域的技术创新成果。',
  '分析结果有多准确': '系统基于大量数据分析和行业经验提供评估，但最终决策仍需结合实际情况综合考虑。分析结果仅供参考，建议在做出重要决策前咨询专业人士。',
  '默认': '感谢您的提问！我是科研成果转化分析智能体。如果您想获得科研成果的转化分析，请点击上方导航栏的"开始分析"按钮，按照系统引导填写相关信息。'  
};

// 模拟API响应函数
export const mockApiResponse = (endpoint, data = {}) => {
  // 模拟网络延迟
  return new Promise((resolve) => {
    setTimeout(() => {
      if (endpoint.includes('/analyze')) {
        resolve({
          success: true,
          sessionId: 'mock-session-' + Date.now(),
          message: '分析请求已提交，请等待分析结果'
        });
      } else if (endpoint.includes('/result')) {
        resolve(mockAnalysisResult);
      } else if (endpoint.includes('/health')) {
        resolve({
          status: 'ok',
          message: '服务正常运行'
        });
      } else if (endpoint.includes('/config')) {
        resolve({
          features: ['分析报告', '市场评估', '专利分析', '转化策略'],
          version: '1.0.0'
        });
      }
    }, 1000); // 1秒延迟，模拟网络请求
  });
};

export default {
  mockAnalysisResult,
  mockChatResponses,
  mockApiResponse
};
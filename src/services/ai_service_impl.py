import json
import os
from typing import Dict, List, Any
from .ai_service_base import (
    DocumentRecognitionService, 
    PatentQueryService, 
    AnalysisService
)


class MockDocumentRecognitionService(DocumentRecognitionService):
    """
    模拟文档识别服务实现
    注意：实际部署时应替换为真实的文档识别API实现
    """
    
    def __init__(self):
        self._initialized = False
        self._config = {}
    
    def initialize(self, config: dict) -> bool:
        """
        初始化模拟文档识别服务
        """
        self._config = config
        self._initialized = True
        print(f"文档识别服务已初始化，配置: {config}")
        return True
    
    def shutdown(self) -> bool:
        """
        关闭服务
        """
        self._initialized = False
        print("文档识别服务已关闭")
        return True
    
    @property
    def is_initialized(self) -> bool:
        """
        服务是否已初始化
        """
        return self._initialized
    
    def recognize_document(self, file_path: str) -> dict:
        """
        模拟识别文档内容
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 模拟文档识别结果
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1].lower()
        
        # 根据文件类型返回不同的模拟结果
        if extension in ['.pdf', '.doc', '.docx', '.txt']:
            return {
                "file_name": file_name,
                "content": "这是模拟的文档内容。包含了科研成果的基本信息、技术要点和应用前景等。",
                "sections": [
                    {"title": "摘要", "content": "项目摘要内容...", "start_pos": 0, "end_pos": 100},
                    {"title": "引言", "content": "引言内容...", "start_pos": 101, "end_pos": 200},
                    {"title": "技术方案", "content": "技术方案详细描述...", "start_pos": 201, "end_pos": 500},
                    {"title": "实验结果", "content": "实验结果和数据分析...", "start_pos": 501, "end_pos": 800},
                    {"title": "结论", "content": "结论和展望...", "start_pos": 801, "end_pos": 1000}
                ],
                "recognition_score": 0.98
            }
        else:
            return {
                "file_name": file_name,
                "error": "不支持的文件类型",
                "supported_types": ["pdf", "doc", "docx", "txt"]
            }
    
    def extract_tables(self, file_path: str) -> list:
        """
        模拟提取文档中的表格
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 模拟表格数据
        return [
            {
                "table_id": "table_1",
                "title": "实验数据对比表",
                "headers": ["指标", "实验组A", "实验组B", "对照组"],
                "rows": [
                    ["性能指标1", "95.2", "98.1", "85.5"],
                    ["性能指标2", "89.7", "92.3", "78.9"],
                    ["性能指标3", "91.5", "94.8", "82.1"]
                ],
                "page_number": 5
            }
        ]
    
    def extract_keywords(self, file_path: str) -> list:
        """
        模拟提取文档关键词
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 模拟关键词提取结果
        return [
            {"keyword": "人工智能", "score": 0.95, "frequency": 25},
            {"keyword": "机器学习", "score": 0.92, "frequency": 20},
            {"keyword": "深度学习", "score": 0.88, "frequency": 18},
            {"keyword": "计算机视觉", "score": 0.85, "frequency": 15},
            {"keyword": "自然语言处理", "score": 0.82, "frequency": 12},
            {"keyword": "模型优化", "score": 0.78, "frequency": 10},
            {"keyword": "算法创新", "score": 0.75, "frequency": 8}
        ]


class MockPatentQueryService(PatentQueryService):
    """
    模拟专利查询服务实现
    注意：实际部署时应替换为真实的专利数据库API实现
    """
    
    def __init__(self):
        self._initialized = False
        self._config = {}
    
    def initialize(self, config: dict) -> bool:
        """
        初始化模拟专利查询服务
        """
        self._config = config
        self._initialized = True
        print(f"专利查询服务已初始化，配置: {config}")
        return True
    
    def shutdown(self) -> bool:
        """
        关闭服务
        """
        self._initialized = False
        print("专利查询服务已关闭")
        return True
    
    @property
    def is_initialized(self) -> bool:
        """
        服务是否已初始化
        """
        return self._initialized
    
    def query_by_keyword(self, keywords: str, limit: int = 10) -> list:
        """
        模拟按关键词查询专利
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 模拟专利查询结果
        mock_results = []
        base_year = 2020
        
        for i in range(min(limit, 5)):
            mock_results.append({
                "patent_id": f"CN{base_year + i}12345{i:02d}U",
                "title": f"基于{keywords}的智能处理方法及系统",
                "abstract": f"本发明涉及一种基于{keywords}的智能处理方法及系统，属于人工智能技术领域。本发明通过创新的算法设计，提高了处理效率和准确率...",
                "application_date": f"{base_year + i}-06-{10 + i:02d}",
                "publication_date": f"{base_year + i}-12-{20 + i:02d}",
                "applicant": f"研究机构{i}",
                "inventor": f"发明人{i}, 发明人{i+1}",
                "ipc_classification": f"G06N{i}/00",
                "status": "授权",
                "similarity_score": 0.95 - (i * 0.03)
            })
        
        return mock_results
    
    def query_by_technology_field(self, field: str, limit: int = 10) -> list:
        """
        模拟按技术领域查询专利
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 映射技术领域到关键词
        field_to_keyword = {
            "it": "信息技术",
            "biomed": "生物医药",
            "new_material": "新材料",
            "energy_saving": "节能环保",
            "other": "其他技术"
        }
        
        keyword = field_to_keyword.get(field, field)
        return self.query_by_keyword(keyword, limit)
    
    def get_patent_details(self, patent_id: str) -> dict:
        """
        模拟获取专利详细信息
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 模拟专利详情
        return {
            "patent_id": patent_id,
            "title": "基于人工智能的智能处理方法及系统",
            "abstract": "本发明涉及一种基于人工智能的智能处理方法及系统，属于人工智能技术领域。本发明通过创新的算法设计，提高了处理效率和准确率...",
            "full_description": "详细的技术描述内容...",
            "claims": [
                "1. 一种基于人工智能的智能处理方法，其特征在于，包括：步骤1、数据采集；步骤2、预处理；步骤3、模型训练；步骤4、结果输出。",
                "2. 根据权利要求1所述的方法，其特征在于，所述步骤2中的预处理包括数据清洗、归一化和特征提取。",
                "3. 根据权利要求1所述的方法，其特征在于，所述步骤3使用深度学习模型进行训练。"
            ],
            "application_date": "2022-06-15",
            "publication_date": "2022-12-25",
            "grant_date": "2023-05-10",
            "applicant": ["研究机构A", "公司B"],
            "inventor": ["发明人甲", "发明人乙", "发明人丙"],
            "ipc_classification": ["G06N1/00", "G06N20/00", "G06F16/245"],
            "status": "授权",
            "legal_status": "有效",
            "cited_by": 45,
            "priority_info": [
                {"country": "CN", "application_number": "CN202112345678.9", "priority_date": "2021-12-15"}
            ]
        }
    
    def analyze_patent_trend(self, keywords: str, years: int = 5) -> dict:
        """
        模拟分析专利趋势
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 模拟专利趋势数据
        current_year = 2025
        trend_data = []
        base_count = 100
        
        for i in range(years):
            year = current_year - years + i + 1
            trend_data.append({
                "year": year,
                "patent_count": base_count + (i * 25),
                "growth_rate": (25 / (base_count + (i-1)*25) * 100) if i > 0 else 0,
                "top_applicants": [
                    {"name": f"机构A_{year}", "count": 15 + i},
                    {"name": f"机构B_{year}", "count": 12 + i},
                    {"name": f"机构C_{year}", "count": 10 + i}
                ],
                "top_cited_patents": [
                    {"patent_id": f"CN{year}1234501U", "citation_count": 30 + i},
                    {"patent_id": f"CN{year}1234502U", "citation_count": 25 + i},
                    {"patent_id": f"CN{year}1234503U", "citation_count": 20 + i}
                ]
            })
        
        return {
            "keywords": keywords,
            "analysis_years": years,
            "trend_data": trend_data,
            "total_patents": sum(item["patent_count"] for item in trend_data),
            "average_growth_rate": (25 / base_count * 100),
            "hot_technologies": [
                {"tech": "深度学习算法", "relevance": 0.92},
                {"tech": "边缘计算", "relevance": 0.88},
                {"tech": "联邦学习", "relevance": 0.85},
                {"tech": "知识图谱", "relevance": 0.82},
                {"tech": "量子计算", "relevance": 0.79}
            ],
            "market_forecast": "根据专利申请趋势，该领域技术发展迅速，预计未来3-5年内将保持20%以上的年增长率..."
        }


class MockAnalysisService(AnalysisService):
    """
    模拟分析服务实现
    注意：实际部署时应替换为真实的大语言模型API实现
    """
    
    def __init__(self):
        self._initialized = False
        self._config = {}
    
    def initialize(self, config: dict) -> bool:
        """
        初始化模拟分析服务
        """
        self._config = config
        self._initialized = True
        print(f"分析服务已初始化，配置: {config}")
        return True
    
    def shutdown(self) -> bool:
        """
        关闭服务
        """
        self._initialized = False
        print("分析服务已关闭")
        return True
    
    @property
    def is_initialized(self) -> bool:
        """
        服务是否已初始化
        """
        return self._initialized
    
    def generate_analysis(self, prompt: str, data: dict) -> dict:
        """
        模拟生成分析内容
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 模拟分析结果
        return {
            "prompt": prompt,
            "analysis_result": f"基于提供的数据，我生成了以下分析：\n\n{prompt}\n\n数据摘要：{str(data)[:200]}...\n\n1. 优势分析：\n   - 技术创新性强，具有明显的技术壁垒\n   - 市场需求潜力大，应用场景广泛\n   - 团队具备较强的研发能力\n\n2. 劣势分析：\n   - 商业化经验相对不足\n   - 市场竞争较为激烈\n   - 前期投入成本较高\n\n3. 机会分析：\n   - 国家政策支持力度大\n   - 行业处于快速发展阶段\n   - 潜在合作伙伴众多\n\n4. 威胁分析：\n   - 技术更新迭代速度快\n   - 市场不确定性因素较多\n   - 国际竞争日益加剧",
            "confidence_score": 0.92,
            "generated_time": "2025-11-18T15:30:00Z"
        }
    
    def generate_report(self, template: str, data: dict) -> str:
        """
        模拟生成报告
        """
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        
        # 模拟报告生成
        report_content = f"# 科研成果转化分析报告\n\n"
        report_content += f"## 1. 成果基本信息\n"
        
        if "basic_info" in data:
            basic = data["basic_info"]
            report_content += f"- 成果名称：{basic.get('achievement_name', '未知')}\n"
            report_content += f"- 成果所属：{'学生（含研究生）' if basic.get('achievement_owner') == 'student' else '科研团队/企业'}\n"
            report_content += f"- 技术领域：{basic.get('tech_field', '未知')}\n"
            report_content += f"- 完成阶段：{basic.get('completion_stage', '未知')}\n"
        
        report_content += "\n## 2. 技术分析\n"
        report_content += "### 2.1 技术优势\n"
        report_content += "- 创新性强，解决了行业关键技术难题\n"
        report_content += "- 技术路线清晰，实现方案可行\n"
        report_content += "- 核心技术具有自主知识产权\n"
        
        report_content += "\n### 2.2 技术成熟度评估\n"
        report_content += "基于当前信息，该成果技术成熟度处于原型开发阶段，具备一定的可行性验证。\n"
        
        report_content += "\n## 3. 市场前景\n"
        report_content += "### 3.1 市场需求分析\n"
        report_content += "随着行业发展和技术进步，市场对该类型技术的需求持续增长。\n"
        
        report_content += "\n### 3.2 竞争格局\n"
        report_content += "当前市场竞争较为激烈，但该成果在某些关键技术指标上具有明显优势。\n"
        
        report_content += "\n## 4. 转化建议\n"
        report_content += "### 4.1 商业化路径\n"
        report_content += "建议采取分步走策略：先与行业龙头企业合作进行小规模试点，验证商业价值后再考虑独立商业化。\n"
        
        report_content += "\n### 4.2 资源需求\n"
        report_content += "- 资金：建议前期投入XX万元用于产品化开发\n"
        report_content += "- 团队：需要补充具有商业化经验的人才\n"
        report_content += "- 合作：寻找2-3家潜在合作伙伴\n"
        
        report_content += "\n## 5. 结论与展望\n"
        report_content += "综合分析表明，该科研成果具有良好的转化前景，建议进一步完善技术细节，加快商业化进程。\n"
        
        return report_content
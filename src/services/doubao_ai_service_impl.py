import json
import requests
import os
import re
from typing import Dict, List, Any, Optional
from .ai_service_base import (
    DocumentRecognitionService, 
    PatentQueryService, 
    AnalysisService
)
from src.utils import get_logger, log_info, log_error, AIServiceError

logger = get_logger(__name__)

class DoubaoBaseService:
    """
    豆包API服务基础类
    """
    
    def __init__(self, config=None):
        self._initialized = False
        self._config = {}
        self._api_key = None
        self._base_url = "https://api.doubao.com/chat/completions"
        self._model = "ERNIE-Bot-4"
        
        # 如果提供了配置，立即初始化
        if config:
            self.initialize(config)
    
    def initialize(self, config: dict) -> bool:
        """
        初始化豆包API服务
        
        Args:
            config: 服务配置，必须包含api_key
        """
        try:
            self._config = config
            self._api_key = config.get("api_key")
            self._model = config.get("model", "ERNIE-Bot-4")
            
            if not self._api_key:
                raise ValueError("豆包API密钥未提供")
            
            self._initialized = True
            log_info(f"豆包API服务已初始化，使用模型: {self._model}")
            return True
        except Exception as e:
            log_error(f"豆包API服务初始化失败: {str(e)}")
            return False
    
    def shutdown(self) -> bool:
        """
        关闭服务
        """
        self._initialized = False
        log_info("豆包API服务已关闭")
        return True
    
    @property
    def is_initialized(self) -> bool:
        """
        服务是否已初始化
        """
        return self._initialized
    
    def _call_api(self, prompt: str, max_tokens: int = 2048) -> str:
        """
        调用豆包API
        
        Args:
            prompt: 提示文本
            max_tokens: 最大生成 tokens 数
            
        Returns:
            str: API 返回的文本内容
        """
        if not self._initialized:
            raise AIServiceError("豆包API服务未初始化", "DoubaoBaseService")
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}"
            }
            
            payload = {
                "model": self._model,
                "messages": [
                    {"role": "system", "content": "你是一个科研成果转化分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(
                self._base_url, 
                headers=headers, 
                json=payload
            )
            
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                raise AIServiceError("API响应格式错误", "DoubaoBaseService")
                
        except requests.exceptions.RequestException as e:
            log_error(f"API请求失败: {str(e)}")
            raise AIServiceError(f"API请求失败: {str(e)}", "DoubaoBaseService")
        except Exception as e:
            log_error(f"API调用过程中发生错误: {str(e)}")
            raise AIServiceError(f"API调用错误: {str(e)}", "DoubaoBaseService")

class DoubaoDocumentRecognitionService(DoubaoBaseService, DocumentRecognitionService):
    """
    豆包文档识别服务实现
    """
    
    def __init__(self, config=None):
        super().__init__(config)
        log_info("文档识别服务初始化完成")
    
    def recognize_document(self, file_path: str) -> dict:
        """
        识别文档内容
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            dict: 文档内容识别结果
        """
        try:
            # 模拟文档识别，实际项目中应调用OCR服务
            log_info(f"识别文档: {file_path}")
            
            # 模拟响应
            return {
                "title": "科研成果转化分析报告",
                "authors": ["张三", "李四"],
                "content": "本文分析了科研成果转化的关键因素和路径...",
                "sections": [
                    {"title": "摘要", "content": "本文研究了..."},
                    {"title": "引言", "content": "随着科技的发展..."}
                ],
                "metadata": {
                    "type": "科研报告",
                    "creation_date": "2023-06-15",
                    "pages": 20
                }
            }
        except Exception as e:
            log_error(f"文档识别失败: {str(e)}")
            raise AIServiceError(f"文档识别失败: {str(e)}", "DoubaoDocumentRecognitionService")
    
    def extract_tables(self, file_path: str) -> list:
        """
        提取文档中的表格
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            list: 表格数据列表
        """
        try:
            log_info(f"提取表格: {file_path}")
            # 模拟表格提取
            return [
                {
                    "title": "市场规模数据表",
                    "rows": [
                        {"year": "2021", "value": "10亿元"},
                        {"year": "2022", "value": "15亿元"},
                        {"year": "2023", "value": "25亿元"}
                    ]
                },
                {
                    "title": "技术指标对比表",
                    "rows": [
                        {"指标": "性能", "当前值": "90%", "行业平均": "75%"},
                        {"指标": "成本", "当前值": "¥100", "行业平均": "¥150"}
                    ]
                }
            ]
        except Exception as e:
            log_error(f"表格提取失败: {str(e)}")
            raise AIServiceError(f"表格提取失败: {str(e)}", "DoubaoDocumentRecognitionService")
    
    def extract_keywords(self, file_path: str) -> list:
        """
        提取文档关键词
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            list: 关键词列表
        """
        try:
            log_info(f"提取关键词: {file_path}")
            # 模拟关键词提取
            return [
                {"keyword": "科研成果", "score": 0.95},
                {"keyword": "转化路径", "score": 0.92},
                {"keyword": "市场分析", "score": 0.88},
                {"keyword": "商业模式", "score": 0.85},
                {"keyword": "知识产权", "score": 0.82}
            ]
        except Exception as e:
            log_error(f"关键词提取失败: {str(e)}")
            raise AIServiceError(f"关键词提取失败: {str(e)}", "DoubaoDocumentRecognitionService")

class DoubaoPatentQueryService(DoubaoBaseService, PatentQueryService):
    """
    豆包专利查询服务实现
    """
    
    def __init__(self, config=None):
        super().__init__(config)
        log_info("专利查询服务初始化完成")
    
    def query_by_keyword(self, keywords: str, limit: int = 10) -> list:
        """
        通过关键词查询专利
        
        Args:
            keywords: 关键词
            limit: 返回结果数量限制
            
        Returns:
            list: 专利信息列表
        """
        try:
            log_info(f"关键词专利查询: {keywords}, 限制: {limit}")
            # 模拟专利查询
            return [
                {
                    "patent_id": "CN101234567A",
                    "title": "一种科研成果转化分析方法",
                    "applicant": "某大学",
                    "publication_date": "2022-01-15",
                    "abstract": "本发明涉及一种科研成果转化分析方法..."
                },
                {
                    "patent_id": "CN102345678B",
                    "title": "智能科研数据处理系统",
                    "applicant": "某科技公司",
                    "publication_date": "2022-05-20",
                    "abstract": "本发明公开了一种智能科研数据处理系统..."
                }
            ]
        except Exception as e:
            log_error(f"专利查询失败: {str(e)}")
            raise AIServiceError(f"专利查询失败: {str(e)}", "DoubaoPatentQueryService")
    
    def query_by_technology_field(self, field: str, limit: int = 10) -> list:
        """
        通过技术领域查询专利
        
        Args:
            field: 技术领域
            limit: 返回结果数量限制
            
        Returns:
            list: 专利信息列表
        """
        try:
            log_info(f"技术领域专利查询: {field}, 限制: {limit}")
            # 复用关键词查询的模拟逻辑
            return self.query_by_keyword(field, limit)
        except Exception as e:
            log_error(f"技术领域专利查询失败: {str(e)}")
            raise AIServiceError(f"技术领域专利查询失败: {str(e)}", "DoubaoPatentQueryService")
    
    def get_patent_details(self, patent_id: str) -> dict:
        """
        获取专利详情
        
        Args:
            patent_id: 专利号
            
        Returns:
            dict: 专利详细信息
        """
        try:
            log_info(f"获取专利详情: {patent_id}")
            # 模拟专利详情
            return {
                "patent_id": patent_id,
                "title": "一种科研成果转化分析方法及其系统",
                "abstract": "本发明涉及一种科研成果转化分析方法及其系统，通过多层次评估模型...",
                "applicant": ["某大学", "某研究院"],
                "inventors": ["张三", "李四", "王五"],
                "application_number": "202110012345.6",
                "application_date": "2021-01-05",
                "publication_number": patent_id,
                "publication_date": "2022-01-15",
                "grant_date": "2023-03-20",
                "ipc_classification": "G06Q10/06",
                "legal_status": "有效",
                "priority_info": [
                    {"country": "CN", "number": "202010123456.7", "date": "2020-12-01"}
                ],
                "cited_by": 15,
                "claims": [
                    "1. 一种科研成果转化分析方法，其特征在于...",
                    "2. 根据权利要求1所述的方法，其特征在于..."
                ]
            }
        except Exception as e:
            log_error(f"获取专利详情失败: {str(e)}")
            raise AIServiceError(f"获取专利详情失败: {str(e)}", "DoubaoPatentQueryService")
    
    def analyze_patent_trend(self, keywords: str, years: int = 5) -> dict:
        """
        分析专利趋势
        
        Args:
            keywords: 关键词
            years: 分析年限
            
        Returns:
            dict: 专利趋势分析结果
        """
        try:
            log_info(f"专利趋势分析: {keywords}, 年限: {years}")
            
            # 生成模拟数据
            base_year = 2023 - years + 1
            year_data = []
            for i in range(years):
                year = base_year + i
                # 生成模拟的逐年增长数据
                applications = 10 + i * 5 + (i % 2) * 3
                grants = 8 + i * 4 - (i % 3) * 1
                citations = 20 + i * 10 + (i % 2) * 5
                
                year_data.append({
                    "year": year,
                    "applications": applications,
                    "grants": grants,
                    "citations": citations
                })
            
            # 模拟专利趋势分析结果
            return {
                "keywords": keywords,
                "analysis_period": f"{base_year}-{base_year + years - 1}",
                "yearly_data": year_data,
                "total_applications": sum(item["applications"] for item in year_data),
                "total_grants": sum(item["grants"] for item in year_data),
                "total_citations": sum(item["citations"] for item in year_data),
                "growth_rate": {
                    "applications": "25%",
                    "grants": "20%",
                    "citations": "30%"
                },
                "key_applicants": [
                    {"name": "某大学", "count": 15},
                    {"name": "某科技公司", "count": 12},
                    {"name": "某研究院", "count": 9}
                ],
                "key_inventors": [
                    {"name": "张三", "count": 8},
                    {"name": "李四", "count": 6}
                ],
                "technological_focus": [
                    {"field": "数据分析", "percentage": 35},
                    {"field": "人工智能", "percentage": 25},
                    {"field": "系统架构", "percentage": 20},
                    {"field": "应用算法", "percentage": 20}
                ],
                "conclusion": "该领域专利申请呈稳定增长趋势，主要集中在数据分析和人工智能技术方向，高校和研究机构是主要申请人。"
            }
        except Exception as e:
            log_error(f"专利趋势分析失败: {str(e)}")
            raise AIServiceError(f"专利趋势分析失败: {str(e)}", "DoubaoPatentQueryService")

class DoubaoAnalysisService(DoubaoBaseService, AnalysisService):
    """
    豆包分析服务实现
    """
    
    def __init__(self, config=None):
        super().__init__(config)
        log_info("分析服务初始化完成")
    
    def generate_analysis(self, prompt: str, data: dict) -> dict:
        """
        生成分析结果
        
        Args:
            prompt: 分析提示
            data: 分析数据
            
        Returns:
            dict: 分析结果
        """
        try:
            log_info(f"生成分析: {prompt[:50]}...")
            
            # 模拟分析结果
            return {
                "analysis_type": "科研成果转化分析",
                "prompt": prompt,
                "timestamp": "2023-06-15T10:30:00",
                "conclusion": "基于提供的数据，该科研成果具有较高的转化潜力。建议采取分阶段转化策略，重点关注知识产权保护和商业模式创新。",
                "key_findings": [
                    "技术创新性评估得分：4.5/5",
                    "市场需求强度：高",
                    "竞争态势：中等",
                    "转化风险：较低"
                ],
                "recommendations": [
                    "完善专利布局，保护核心技术",
                    "开展小规模市场验证",
                    "寻求产业合作伙伴",
                    "制定详细的商业化计划"
                ],
                "potential_impact": {
                    "economic": "中等",
                    "social": "较高",
                    "environmental": "较低"
                }
            }
        except Exception as e:
            log_error(f"生成分析失败: {str(e)}")
            raise AIServiceError(f"生成分析失败: {str(e)}", "DoubaoAnalysisService")
    
    def generate_report(self, template: str, data: dict) -> str:
        """
        生成报告
        
        Args:
            template: 报告模板
            data: 报告数据
            
        Returns:
            str: 生成的报告内容
        """
        try:
            log_info("生成报告")
            
            # 模拟报告生成
            return "# 科研成果转化分析报告\n\n## 1. 项目概述\n本报告对[项目名称]的转化潜力进行了全面分析...\n\n## 2. 技术评估\n技术创新性：高\n技术成熟度：中\n技术壁垒：高\n\n## 3. 市场分析\n市场规模：约50亿元\n增长率：20%/年\n目标客户：企业、科研机构\n\n## 4. 转化策略\n推荐转化路径：技术许可+合资公司\n预计投资回收期：3-4年\n\n## 5. 结论与建议\n该科研成果具有较高的转化价值，建议尽快启动商业化进程。"
        except Exception as e:
            log_error(f"生成报告失败: {str(e)}")
            raise AIServiceError(f"生成报告失败: {str(e)}", "DoubaoAnalysisService")
    
    def analyze_achievement(self, achievement_data: dict) -> dict:
        """
        分析科研成果
        
        Args:
            achievement_data: 科研成果数据
            
        Returns:
            dict: 分析结果
        """
        try:
            log_info("分析科研成果")
            
            # 构建分析提示
            prompt = f"请分析以下科研成果的转化潜力：\n{json.dumps(achievement_data, ensure_ascii=False)}"
            
            # 调用通用分析方法
            return self.generate_analysis(prompt, achievement_data)
        except Exception as e:
            log_error(f"分析科研成果失败: {str(e)}")
            raise AIServiceError(f"分析科研成果失败: {str(e)}", "DoubaoAnalysisService")
    
    # API服务需要的异步分析方法
    async def analyze_market(self, prompt: str) -> str:
        """分析市场情况（用于API服务）"""
        log_info("API调用：市场分析")
        # 实际应用中这里应该调用豆包API
        return "基于对该领域的深入分析，我们预测该技术在未来3-5年内将有显著的市场增长。当前市场规模约50亿元，预计年增长率达20%。主要应用场景包括企业智能化转型、科研机构数据分析等。市场竞争格局相对分散，尚未形成垄断，为新技术提供了良好的切入机会。建议重点关注垂直行业应用，建立示范案例。"
    
    async def analyze_patent(self, prompt: str) -> str:
        """分析专利情况（用于API服务）"""
        log_info("API调用：专利分析")
        # 实际应用中这里应该调用豆包API
        return "专利分析显示，该领域近三年专利申请量呈上升趋势，但核心技术专利仍有布局空间。建议围绕以下方向申请专利：1)核心算法优化；2)应用场景创新；3)系统架构设计。预计完成专利布局需要6-9个月时间，预算约10-15万元。同时，建议进行FTO(Freedom to Operate)分析，评估潜在侵权风险。"
    
    async def generate_strategy(self, prompt: str) -> str:
        """生成转化策略（用于API服务）"""
        log_info("API调用：生成转化策略")
        # 实际应用中这里应该调用豆包API
        return "推荐转化路径：第一阶段（0-6个月）进行技术优化和市场验证，完成2-3个试点项目；第二阶段（6-12个月）寻求战略合作伙伴，签订技术许可协议；第三阶段（12-24个月）规模化推广，建立行业标准。建议组建专业的商业团队，包括技术推广、商务谈判和知识产权管理人才。同时，积极对接政府科技成果转化项目，获取政策和资金支持。"
    
    async def generate_summary(self, prompt: str) -> str:
        """生成总结（用于API服务）"""
        log_info("API调用：生成总结")
        # 实际应用中这里应该调用豆包API
        return "综合评估结果显示，该科研成果具有较高的转化价值和市场潜力。技术创新性突出，应用场景明确，适合通过技术许可或合资公司方式实现转化。预计投资回收期为3-4年，5年内可实现5000万元以上的经济效益。建议团队加强商业模式设计，完善知识产权保护，并积极寻求产业资本合作，加速技术产业化进程。"
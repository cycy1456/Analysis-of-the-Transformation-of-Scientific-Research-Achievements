"""API路由定义"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import json
import datetime
from ..core.workflow_engine import WorkflowEngine
from ..services import get_ai_service
from ..services.doubao_ai_service_impl import DoubaoAnalysisService
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# 定义请求和响应模型
class AnalysisRequest(BaseModel):
    title: str
    description: str
    field: str
    maturity: str = "实验室"
    keywords: str = ""
    teamSize: str = ""
    investmentNeeds: str = ""
    patentStatus: str = "已有专利"
    expectedOutcome: str = "技术转让"

class AnalysisResponse(BaseModel):
    session_id: str
    status: str = "processing"
    message: str = "分析已开始"

class AnalysisResult(BaseModel):
    session_id: str
    status: str
    market_analysis: Optional[dict] = None
    patent_analysis: Optional[dict] = None
    transfer_strategy: Optional[dict] = None
    summary: Optional[str] = None
    error: Optional[str] = None

# 初始化豆包AI服务
analysis_service = DoubaoAnalysisService()
analysis_service.initialize({"api_key": "mock_api_key"})  # 实际部署时应从配置中读取

# 模拟数据库存储分析请求和结果
session_store = {}

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_scientific_achievement(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """分析科研成果"""
    try:
        # 生成会话ID
        session_id = str(uuid.uuid4())
        
        # 存储请求信息
        session_store[session_id] = {
            "status": "processing",
            "request": request.model_dump(),
            "result": None,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        logger.info(f"创建分析会话 {session_id}: {request.title}")
        
        # 异步启动分析过程
        background_tasks.add_task(perform_analysis, session_id, request)
        
        return AnalysisResponse(
            session_id=session_id,
            status="processing",
            message="分析已开始，稍后查询结果"
        )
        
    except Exception as e:
        logger.error(f"分析请求处理错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理分析请求时发生错误: {str(e)}")

async def perform_analysis(session_id: str, request: AnalysisRequest):
    """后台执行实际分析的函数"""
    try:
        logger.info(f"开始分析会话 {session_id}")
        
        # 构建分析输入
        analysis_input = {
            "title": request.title,
            "description": request.description,
            "field": request.field,
            "maturity": request.maturity,
            "keywords": request.keywords.split(",") if request.keywords else [],
            "team_size": request.teamSize,
            "investment_needs": request.investmentNeeds,
            "patent_status": request.patentStatus,
            "expected_outcome": request.expectedOutcome
        }
        
        # 调用豆包AI服务进行各项分析
        market_analysis = await analysis_service.analyze_market(
            f"分析'{request.title}'在{request.field}领域的市场潜力，考虑{request.keywords}等关键词"
        )
        
        patent_analysis = await analysis_service.analyze_patent(
            f"分析{request.field}领域的专利情况，成果名称：{request.title}，专利状态：{request.patentStatus}"
        )
        
        transfer_strategy = await analysis_service.generate_strategy(
            f"为{request.title}制定转化策略，考虑{request.maturity}的技术成熟度和{request.expectedOutcome}的预期转化方式"
        )
        
        summary = await analysis_service.generate_summary(
            f"总结{request.title}的分析，包括市场前景、专利情况和转化策略"
        )
        
        # 构建分析结果
        result = {
            "market_analysis": {
                "market_size": "根据豆包AI分析，该成果在相关领域具有市场潜力",
                "competition": "竞争分析已完成",
                "commercial_potential": "商业化潜力评估已完成",
                "detailed_analysis": market_analysis
            },
            "patent_analysis": {
                "protection_strategy": "专利保护建议已生成",
                "risk_assessment": "知识产权风险分析已完成",
                "detailed_analysis": patent_analysis
            },
            "transfer_strategy": {
                "recommended_path": request.expectedOutcome,
                "timeline": "转化时间线已规划",
                "key_factors": "关键成功因素已识别",
                "detailed_strategy": transfer_strategy
            },
            "summary": summary,
            "completed_at": datetime.datetime.now().isoformat()
        }
        
        # 更新会话状态
        session_store[session_id]["status"] = "completed"
        session_store[session_id]["result"] = result
        session_store[session_id]["completed_at"] = datetime.datetime.now().isoformat()
        
        logger.info(f"分析完成会话 {session_id}")
        
    except Exception as e:
        error_msg = str(e)
        session_store[session_id]["status"] = "error"
        session_store[session_id]["error"] = error_msg
        session_store[session_id]["completed_at"] = datetime.datetime.now().isoformat()
        logger.error(f"分析错误会话 {session_id}: {error_msg}")

@router.get("/result/{session_id}", response_model=AnalysisResult)
async def get_analysis_result(session_id: str):
    """获取分析结果"""
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    session = session_store[session_id]
    
    return AnalysisResult(
        session_id=session_id,
        status=session["status"],
        market_analysis=session["result"].get("market_analysis") if session["result"] else None,
        patent_analysis=session["result"].get("patent_analysis") if session["result"] else None,
        transfer_strategy=session["result"].get("transfer_strategy") if session["result"] else None,
        summary=session["result"].get("summary") if session["result"] else None,
        error=session.get("error")
    )

# 注意：simulate_analysis 函数已被 perform_analysis 函数替代，该函数直接使用豆包AI服务
# 不再需要模拟分析，而是通过BackgroundTasks异步执行实际分析

@router.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "scientific-achievement-agent-api"}

@router.get("/config")
async def get_config():
    """获取API配置信息"""
    return {
        "api_version": "1.0.0",
        "supported_methods": ["analyze", "result", "health", "config"],
        "docs_url": "/docs"
    }
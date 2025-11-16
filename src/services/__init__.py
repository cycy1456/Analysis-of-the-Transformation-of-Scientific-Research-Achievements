from .ai_service_base import (
    AIServiceBase,
    DocumentRecognitionService,
    PatentQueryService,
    AnalysisService
)

from .ai_service_impl import (
    MockDocumentRecognitionService,
    MockPatentQueryService,
    MockAnalysisService
)

from .doubao_ai_service_impl import (
    DoubaoDocumentRecognitionService,
    DoubaoPatentQueryService,
    DoubaoAnalysisService
)


def get_document_recognition_service(config: dict = None) -> DocumentRecognitionService:
    """
    获取文档识别服务实例
    
    Args:
        config: 豆包API配置参数（可选）
        
    Returns:
        DocumentRecognitionService: 文档识别服务实例
    """
    # 使用豆包API服务
    service = DoubaoDocumentRecognitionService(config)
    return service


def get_patent_query_service(config: dict = None) -> PatentQueryService:
    """
    获取专利查询服务实例
    
    Args:
        config: 豆包API配置参数（可选）
        
    Returns:
        PatentQueryService: 专利查询服务实例
    """
    # 使用豆包API服务
    service = DoubaoPatentQueryService(config)
    return service


def get_analysis_service(config: dict = None) -> AnalysisService:
    """
    获取分析服务实例
    
    Args:
        config: 豆包API配置参数（可选）
        
    Returns:
        AnalysisService: 分析服务实例
    """
    # 使用豆包API服务
    service = DoubaoAnalysisService(config)
    return service


__all__ = [
    # 基类
    'AIServiceBase',
    'DocumentRecognitionService',
    'PatentQueryService',
    'AnalysisService',
    
    # 实现类
    'MockDocumentRecognitionService',
    'MockPatentQueryService',
    'MockAnalysisService',
    'DoubaoDocumentRecognitionService',
    'DoubaoPatentQueryService',
    'DoubaoAnalysisService',
    
    # 工厂函数
    'get_document_recognition_service',
    'get_patent_query_service',
    'get_analysis_service'
]
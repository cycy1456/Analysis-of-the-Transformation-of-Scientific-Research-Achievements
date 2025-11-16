from abc import ABC, abstractmethod


class AIServiceBase(ABC):
    """
    AI服务基类，所有AI服务接口都应继承此类
    """
    
    @abstractmethod
    def initialize(self, config: dict) -> bool:
        """
        初始化服务
        
        Args:
            config: 服务配置参数
            
        Returns:
            bool: 初始化是否成功
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """
        关闭服务
        
        Returns:
            bool: 关闭是否成功
        """
        pass
    
    @property
    def is_initialized(self) -> bool:
        """
        服务是否已初始化
        
        Returns:
            bool: 初始化状态
        """
        pass


class DocumentRecognitionService(AIServiceBase):
    """
    文档识别服务接口
    """
    
    @abstractmethod
    def recognize_document(self, file_path: str) -> dict:
        """
        识别文档内容
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            dict: 识别结果，包含文本内容、章节结构等
        """
        pass
    
    @abstractmethod
    def extract_tables(self, file_path: str) -> list:
        """
        提取文档中的表格
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            list: 表格数据列表
        """
        pass
    
    @abstractmethod
    def extract_keywords(self, file_path: str) -> list:
        """
        提取文档关键词
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            list: 关键词列表
        """
        pass


class PatentQueryService(AIServiceBase):
    """
    专利查询服务接口
    """
    
    @abstractmethod
    def query_by_keyword(self, keywords: str, limit: int = 10) -> list:
        """
        按关键词查询专利
        
        Args:
            keywords: 关键词
            limit: 返回结果数量限制
            
        Returns:
            list: 专利信息列表
        """
        pass
    
    @abstractmethod
    def query_by_technology_field(self, field: str, limit: int = 10) -> list:
        """
        按技术领域查询专利
        
        Args:
            field: 技术领域
            limit: 返回结果数量限制
            
        Returns:
            list: 专利信息列表
        """
        pass
    
    @abstractmethod
    def get_patent_details(self, patent_id: str) -> dict:
        """
        获取专利详细信息
        
        Args:
            patent_id: 专利ID
            
        Returns:
            dict: 专利详细信息
        """
        pass
    
    @abstractmethod
    def analyze_patent_trend(self, keywords: str, years: int = 5) -> dict:
        """
        分析专利趋势
        
        Args:
            keywords: 关键词
            years: 分析年限
            
        Returns:
            dict: 专利趋势分析结果
        """
        pass


class AnalysisService(AIServiceBase):
    """
    文本分析服务接口，用于生成报告和分析内容
    """
    
    @abstractmethod
    def generate_analysis(self, prompt: str, data: dict) -> dict:
        """
        生成分析内容
        
        Args:
            prompt: 分析提示
            data: 用于分析的数据
            
        Returns:
            dict: 分析结果
        """
        pass
    
    @abstractmethod
    def generate_report(self, template: str, data: dict) -> str:
        """
        生成报告
        
        Args:
            template: 报告模板
            data: 报告数据
            
        Returns:
            str: 生成的报告内容
        """
        pass
"""
自定义异常类定义
"""


class ScientificAchievementError(Exception):
    """
    科研成果转化分析智能体的基础异常类
    所有其他异常都应该继承自此类
    """
    
    def __init__(self, message: str, error_code: str = "GENERAL_ERROR", 
                 details: dict = None):
        """
        初始化基础异常
        
        Args:
            message: 错误消息
            error_code: 错误代码
            details: 错误详情（可选）
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """
        返回异常的字符串表示
        """
        return f"[{self.error_code}] {self.message}"


class WorkflowError(ScientificAchievementError):
    """
    工作流相关异常
    """
    
    def __init__(self, message: str, error_code: str = "WORKFLOW_ERROR", 
                 workflow_id: str = None, node_id: str = None, details: dict = None):
        """
        初始化工作流异常
        
        Args:
            message: 错误消息
            error_code: 错误代码
            workflow_id: 工作流ID（可选）
            node_id: 节点ID（可选）
            details: 错误详情（可选）
        """
        details = details or {}
        if workflow_id:
            details['workflow_id'] = workflow_id
        if node_id:
            details['node_id'] = node_id
        
        super().__init__(message, error_code, details)


class ConfigurationError(ScientificAchievementError):
    """
    配置相关异常
    """
    
    def __init__(self, message: str, error_code: str = "CONFIG_ERROR", 
                 config_path: str = None, details: dict = None):
        """
        初始化配置异常
        
        Args:
            message: 错误消息
            error_code: 错误代码
            config_path: 配置文件路径（可选）
            details: 错误详情（可选）
        """
        details = details or {}
        if config_path:
            details['config_path'] = config_path
        
        super().__init__(message, error_code, details)


class NodeExecutionError(WorkflowError):
    """
    节点执行异常
    """
    
    def __init__(self, message: str, node_id: str, node_type: str = None,
                 error_code: str = "NODE_EXECUTION_ERROR", details: dict = None):
        """
        初始化节点执行异常
        
        Args:
            message: 错误消息
            node_id: 节点ID
            node_type: 节点类型（可选）
            error_code: 错误代码
            details: 错误详情（可选）
        """
        details = details or {}
        if node_type:
            details['node_type'] = node_type
        
        super().__init__(message, error_code, node_id=node_id, details=details)


class AIServiceError(ScientificAchievementError):
    """
    AI服务相关异常
    """
    
    def __init__(self, message: str, service_name: str = None, 
                 error_code: str = "AI_SERVICE_ERROR", details: dict = None):
        """
        初始化AI服务异常
        
        Args:
            message: 错误消息
            service_name: 服务名称（可选）
            error_code: 错误代码
            details: 错误详情（可选）
        """
        details = details or {}
        if service_name:
            details['service_name'] = service_name
        
        super().__init__(message, error_code, details)


class DocumentRecognitionError(AIServiceError):
    """
    文档识别异常
    """
    
    def __init__(self, message: str, file_path: str = None, 
                 error_code: str = "DOC_RECOGNITION_ERROR", details: dict = None):
        """
        初始化文档识别异常
        
        Args:
            message: 错误消息
            file_path: 文件路径（可选）
            error_code: 错误代码
            details: 错误详情（可选）
        """
        details = details or {}
        if file_path:
            details['file_path'] = file_path
        
        super().__init__(message, "DocumentRecognitionService", error_code, details)


class PatentQueryError(AIServiceError):
    """
    专利查询异常
    """
    
    def __init__(self, message: str, query_params: dict = None, 
                 error_code: str = "PATENT_QUERY_ERROR", details: dict = None):
        """
        初始化专利查询异常
        
        Args:
            message: 错误消息
            query_params: 查询参数（可选）
            error_code: 错误代码
            details: 错误详情（可选）
        """
        details = details or {}
        if query_params:
            details['query_params'] = query_params
        
        super().__init__(message, "PatentQueryService", error_code, details)


class InputValidationError(ScientificAchievementError):
    """
    输入验证异常
    """
    
    def __init__(self, message: str, field_name: str = None, 
                 field_value: any = None, error_code: str = "INPUT_VALIDATION_ERROR", 
                 details: dict = None):
        """
        初始化输入验证异常
        
        Args:
            message: 错误消息
            field_name: 字段名称（可选）
            field_value: 字段值（可选）
            error_code: 错误代码
            details: 错误详情（可选）
        """
        details = details or {}
        if field_name:
            details['field_name'] = field_name
        if field_value is not None:
            details['field_value'] = field_value
        
        super().__init__(message, error_code, details)


class FileOperationError(ScientificAchievementError):
    """
    文件操作异常
    """
    
    def __init__(self, message: str, file_path: str = None, operation: str = None,
                 error_code: str = "FILE_OPERATION_ERROR", details: dict = None):
        """
        初始化文件操作异常
        
        Args:
            message: 错误消息
            file_path: 文件路径（可选）
            operation: 操作类型（可选）如 "read", "write", "delete" 等
            error_code: 错误代码
            details: 错误详情（可选）
        """
        details = details or {}
        if file_path:
            details['file_path'] = file_path
        if operation:
            details['operation'] = operation
        
        super().__init__(message, error_code, details)


class ServiceNotInitializedError(ScientificAchievementError):
    """
    服务未初始化异常
    """
    
    def __init__(self, service_name: str, error_code: str = "SERVICE_NOT_INITIALIZED", 
                 details: dict = None):
        """
        初始化服务未初始化异常
        
        Args:
            service_name: 服务名称
            error_code: 错误代码
            details: 错误详情（可选）
        """
        message = f"服务 '{service_name}' 尚未初始化"
        details = details or {}
        details['service_name'] = service_name
        
        super().__init__(message, error_code, details)


class WorkflowExecutionError(ScientificAchievementError):
    """
    工作流执行异常
    """
    
    def __init__(self, message: str, workflow_id: str, execution_id: str = None,
                 error_code: str = "WORKFLOW_EXECUTION_ERROR", details: dict = None):
        """
        初始化工作流执行异常
        
        Args:
            message: 错误消息
            workflow_id: 工作流ID
            execution_id: 执行ID（可选）
            error_code: 错误代码
            details: 错误详情（可选）
        """
        details = details or {}
        details['workflow_id'] = workflow_id
        if execution_id:
            details['execution_id'] = execution_id
        
        super().__init__(message, error_code, details)
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class UIBase(ABC):
    """
    用户界面基类，定义了用户交互的统一接口
    所有界面实现（如命令行界面、Web界面等）都应该继承此类
    """
    
    @abstractmethod
    def display_message(self, message: str) -> None:
        """
        显示消息给用户
        
        Args:
            message: 要显示的消息内容
        """
        pass
    
    @abstractmethod
    def display_error(self, error_message: str) -> None:
        """
        显示错误消息给用户
        
        Args:
            error_message: 错误消息内容
        """
        pass
    
    @abstractmethod
    def display_form(self, title: str, form_config: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        显示表单并收集用户输入
        
        Args:
            title: 表单标题
            form_config: 表单配置列表，每个配置项包含表单字段的定义
            
        Returns:
            Dict[str, Any]: 用户输入的数据
        """
        pass
    
    @abstractmethod
    def display_progress(self, current: int, total: int, description: str = "") -> None:
        """
        显示进度条
        
        Args:
            current: 当前进度
            total: 总进度
            description: 进度描述
        """
        pass
    
    @abstractmethod
    def display_report(self, title: str, content: str, report_format: str = "text") -> None:
        """
        显示报告内容
        
        Args:
            title: 报告标题
            content: 报告内容
            report_format: 报告格式（如text、pdf等）
        """
        pass
    
    @abstractmethod
    def confirm_action(self, message: str) -> bool:
        """
        确认操作
        
        Args:
            message: 确认消息
            
        Returns:
            bool: 用户是否确认（True/False）
        """
        pass
    
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """
        获取用户输入的文本
        
        Args:
            prompt: 输入提示
            
        Returns:
            str: 用户输入的文本
        """
        pass
    
    @abstractmethod
    def display_menu(self, title: str, options: List[str]) -> int:
        """
        显示菜单并获取用户选择
        
        Args:
            title: 菜单标题
            options: 菜单选项列表
            
        Returns:
            int: 用户选择的选项索引（从0开始）
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """
        清空屏幕
        """
        pass
    
    def initialize(self) -> bool:
        """
        初始化界面
        
        Returns:
            bool: 初始化是否成功
        """
        return True
    
    def shutdown(self) -> bool:
        """
        关闭界面
        
        Returns:
            bool: 关闭是否成功
        """
        return True


class FormFieldType:
    """
    表单字段类型常量
    """
    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    SELECT = "select"
    RATING = "rating"
    FILE = "file"
import logging
import os
import datetime
from typing import Optional


class Logger:
    """
    日志管理器
    """
    
    # 日志级别映射
    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    def __init__(self, name: str = "scientific_achievement_agent", 
                 log_file: Optional[str] = None,
                 level: str = "info",
                 console_output: bool = True,
                 log_dir: str = "logs"):
        """
        初始化日志管理器
        
        Args:
            name: 日志名称
            log_file: 日志文件路径，None表示自动生成
            level: 日志级别
            console_output: 是否输出到控制台
            log_dir: 日志目录
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LOG_LEVELS.get(level.lower(), logging.INFO))
        self.logger.propagate = False  # 避免重复日志
        
        # 清空已有的处理器
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # 文件处理器
        if log_file is None:
            # 自动生成日志文件名
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")
        else:
            # 确保日志目录存在
            log_file_dir = os.path.dirname(log_file)
            if log_file_dir:
                os.makedirs(log_file_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        self.log_file = log_file
        self.log_dir = log_dir
    
    def debug(self, message: str) -> None:
        """
        记录调试日志
        
        Args:
            message: 日志消息
        """
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """
        记录信息日志
        
        Args:
            message: 日志消息
        """
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """
        记录警告日志
        
        Args:
            message: 日志消息
        """
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False) -> None:
        """
        记录错误日志
        
        Args:
            message: 日志消息
            exc_info: 是否包含异常信息
        """
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False) -> None:
        """
        记录严重错误日志
        
        Args:
            message: 日志消息
            exc_info: 是否包含异常信息
        """
        self.logger.critical(message, exc_info=exc_info)
    
    def set_level(self, level: str) -> None:
        """
        设置日志级别
        
        Args:
            level: 日志级别
        """
        self.logger.setLevel(self.LOG_LEVELS.get(level.lower(), logging.INFO))
    
    def get_log_file(self) -> str:
        """
        获取日志文件路径
        
        Returns:
            str: 日志文件路径
        """
        return self.log_file


# 创建全局日志实例
global_logger = Logger()


def get_logger(name: Optional[str] = None) -> Logger:
    """
    获取日志实例
    
    Args:
        name: 日志名称，如果为None则返回全局日志实例
        
    Returns:
        Logger: 日志实例
    """
    if name is None:
        return global_logger
    else:
        return Logger(name)


def debug(message: str) -> None:
    """
    全局调试日志函数
    """
    global_logger.debug(message)


def info(message: str) -> None:
    """
    全局信息日志函数
    """
    global_logger.info(message)


def warning(message: str) -> None:
    """
    全局警告日志函数
    """
    global_logger.warning(message)


def error(message: str, exc_info: bool = False) -> None:
    """
    全局错误日志函数
    """
    global_logger.error(message, exc_info=exc_info)


def critical(message: str, exc_info: bool = False) -> None:
    """
    全局严重错误日志函数
    """
    global_logger.critical(message, exc_info=exc_info)
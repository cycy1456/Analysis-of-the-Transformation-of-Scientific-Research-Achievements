"""
科研成果转化分析智能体 - 使用示例

此脚本演示如何以编程方式使用科研成果转化分析智能体
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.workflow_engine import WorkflowEngine
from src.config.config_loader import ConfigLoader
from src.ui import get_ui
from src.utils import get_logger, log_info, ScientificAchievementError

# 获取日志记录器
logger = get_logger('example')

def run_analysis(config_path=None):
    """
    运行科研成果转化分析
    
    Args:
        config_path: 可选，配置文件路径
    
    Returns:
        bool: 是否成功完成分析
    """
    try:
        log_info("开始科研成果转化分析示例...")
        
        # 加载配置
        if config_path:
            workflow_config = ConfigLoader.load_from_file(config_path)
        else:
            workflow_config = ConfigLoader.load_from_file()
        
        # 添加豆包API配置
        doubao_config = {
            "api_key": "95ece695-1aea-4add-b131-31b2fd72fec5",
            "model": "ERNIE-Bot-4"
        }
        workflow_config["ai_service"] = doubao_config
        log_info("豆包API配置添加成功")
        
        # 创建工作流引擎
        engine = WorkflowEngine(workflow_config)
        
        # 创建命令行界面
        ui = get_ui("cli")
        
        # 执行工作流
        result = engine.execute(ui)
        
        # 获取工作流变量
        workflow_variables = engine.get_variables()
        log_info(f"分析完成，结果: {result}")
        log_info(f"工作流变量: {workflow_variables}")
        
        return True
        
    except ScientificAchievementError as e:
        log_info(f"分析过程中出现错误: {e}")
        return False
    except Exception as e:
        log_info(f"发生未预期的错误: {str(e)}", exc_info=True)
        return False


def main():
    """
    示例主函数
    """
    print("科研成果转化分析智能体使用示例")
    print("==================================")
    
    # 运行分析
    success = run_analysis()
    
    if success:
        print("\n示例分析成功完成！")
    else:
        print("\n示例分析失败！")


if __name__ == "__main__":
    main()
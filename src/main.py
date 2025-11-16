"""
科研成果转化分析智能体 - 主入口文件
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.workflow_engine import WorkflowEngine
from src.config.config_loader import ConfigLoader
from src.ui import get_ui
from src.utils import get_logger, log_info, log_error, ScientificAchievementError

# 获取日志记录器
logger = get_logger(__name__)

def main():
    """
    主函数，启动科研成果转化分析智能体
    """
    try:
        log_info("正在启动科研成果转化分析智能体...")
        
        # 获取默认配置路径
        config_path = ConfigLoader.get_default_config_path()
        log_info(f"使用配置文件: {config_path}")
        
        # 加载配置
        workflow_config = ConfigLoader.load_from_file(config_path)
        
        # 添加豆包API配置
        doubao_config = {
            "api_key": "95ece695-1aea-4add-b131-31b2fd72fec5",
            "model": "ERNIE-Bot-4"
        }
        workflow_config["ai_service"] = doubao_config
        log_info("豆包API配置添加成功")
        
        # 创建工作流引擎
        engine = WorkflowEngine(workflow_config)
        
        # 创建用户界面
        ui = get_ui("cli")
        
        # 启动工作流
        log_info("工作流引擎初始化完成，开始执行工作流...")
        print("已配置豆包1.6 API服务")
        engine.execute(ui)
        
        log_info("科研成果转化分析完成！")
        
    except ScientificAchievementError as e:
        log_error(f"科研成果转化分析过程中出现错误: {e}")
        print(f"\n错误: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        log_info("用户中断操作")
        print("\n操作已中断")
        sys.exit(0)
    except Exception as e:
        log_error(f"发生未预期的错误: {str(e)}", exc_info=True)
        print(f"\n发生未预期的错误: {str(e)}")
        sys.exit(1)
    finally:
        # 清理资源
        try:
            if 'ui' in locals():
                ui.close()
        except:
            pass


if __name__ == "__main__":
    main()
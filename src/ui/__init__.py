from .ui_base import UIBase, FormFieldType
from .cli_ui import CLIUI


def get_ui(ui_type: str = "cli", **kwargs) -> UIBase:
    """
    获取用户界面实例
    
    Args:
        ui_type: 界面类型，目前支持 "cli"
        **kwargs: 界面初始化参数
        
    Returns:
        UIBase: 用户界面实例
    """
    if ui_type.lower() == "cli":
        ui = CLIUI()
        ui.initialize()
        return ui
    else:
        raise ValueError(f"不支持的界面类型: {ui_type}")


__all__ = [
    'UIBase',
    'FormFieldType',
    'CLIUI',
    'get_ui'
]
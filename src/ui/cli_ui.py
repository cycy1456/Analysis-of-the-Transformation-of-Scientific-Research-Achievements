import os
import sys
from typing import Dict, Any, List, Optional
from .ui_base import UIBase, FormFieldType


class CLIUI(UIBase):
    """
    命令行界面实现
    """
    
    def __init__(self):
        self._initialized = False
        self._line_length = 80
    
    def initialize(self) -> bool:
        """
        初始化命令行界面
        """
        self._initialized = True
        # 获取终端宽度
        try:
            columns, _ = os.get_terminal_size()
            self._line_length = columns - 2
        except OSError:
            pass
        
        self.display_message("==== 科研成果转化分析智能体 ====\n")
        return True
    
    def shutdown(self) -> bool:
        """
        关闭命令行界面
        """
        self._initialized = False
        print("\n感谢使用科研成果转化分析智能体！")
        return True
    
    def display_message(self, message: str) -> None:
        """
        显示普通消息
        """
        print(f"{message}")
    
    def display_error(self, error_message: str) -> None:
        """
        显示错误消息
        """
        print(f"\033[91m错误: {error_message}\033[0m")
    
    def display_form(self, title: str, form_config: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        显示表单并收集用户输入
        """
        self.display_separator()
        print(f"{title}\n")
        
        result = {}
        
        for field in form_config:
            key = field.get("key")
            label = field.get("label", key)
            field_type = field.get("type", FormFieldType.TEXT)
            required = field.get("required", False)
            placeholder = field.get("placeholder", "")
            
            while True:
                print(f"{label}:{required and ' *' or ''} {placeholder and f'[{placeholder}]' or ''}")
                
                if field_type == FormFieldType.TEXT:
                    value = self._get_text_input()
                elif field_type == FormFieldType.TEXTAREA:
                    value = self._get_textarea_input()
                elif field_type == FormFieldType.NUMBER:
                    value = self._get_number_input()
                elif field_type == FormFieldType.RADIO:
                    value = self._get_radio_input(field.get("options", []))
                elif field_type == FormFieldType.CHECKBOX:
                    value = self._get_checkbox_input(field.get("options", []))
                elif field_type == FormFieldType.SELECT:
                    value = self._get_select_input(field.get("options", []))
                elif field_type == FormFieldType.RATING:
                    value = self._get_rating_input()
                elif field_type == FormFieldType.FILE:
                    value = self._get_file_input()
                else:
                    value = self._get_text_input()
                
                if required and not value:
                    self.display_error("此项为必填项，请重新输入")
                    continue
                
                result[key] = value
                break
            
            print()  # 添加空行
        
        self.display_separator()
        return result
    
    def display_progress(self, current: int, total: int, description: str = "") -> None:
        """
        显示进度条
        """
        bar_length = 50
        progress = current / total
        filled_length = int(bar_length * progress)
        
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        percent = progress * 100
        
        # 使用\r覆盖当前行
        sys.stdout.write(f'\r[{bar}] {percent:.1f}% {description}')
        sys.stdout.flush()
        
        if current >= total:
            print()  # 完成时换行
    
    def display_report(self, title: str, content: str, report_format: str = "text") -> None:
        """
        显示报告内容
        """
        self.display_separator()
        print(f"{title}")
        self.display_separator()
        print(content)
        self.display_separator()
        
        # 如果不是文本格式，提示用户
        if report_format != "text":
            self.display_message(f"报告已按{report_format}格式生成")
    
    def confirm_action(self, message: str) -> bool:
        """
        确认操作
        """
        while True:
            response = input(f"{message} (y/n): ").lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                self.display_error("请输入 y 或 n")
    
    def get_input(self, prompt: str) -> str:
        """
        获取用户输入的文本
        """
        return input(prompt)
    
    def display_menu(self, title: str, options: List[str]) -> int:
        """
        显示菜单并获取用户选择
        """
        self.display_separator()
        print(f"{title}\n")
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        print()
        
        while True:
            try:
                choice = int(input(f"请选择 [1-{len(options)}]: "))
                if 1 <= choice <= len(options):
                    return choice - 1  # 返回索引（从0开始）
                else:
                    self.display_error(f"请输入1-{len(options)}之间的数字")
            except ValueError:
                self.display_error("请输入有效的数字")
    
    def clear(self) -> None:
        """
        清空屏幕
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_separator(self) -> None:
        """
        显示分隔线
        """
        print("=" * self._line_length)
    
    # 私有辅助方法
    def _get_text_input(self) -> str:
        """
        获取文本输入
        """
        return input().strip()
    
    def _get_textarea_input(self) -> str:
        """
        获取多行文本输入
        输入空行结束输入
        """
        print("请输入内容（空行结束）：")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        return "\n".join(lines)
    
    def _get_number_input(self) -> float:
        """
        获取数字输入
        """
        while True:
            try:
                value = input().strip()
                if not value:
                    return 0
                return float(value)
            except ValueError:
                self.display_error("请输入有效的数字")
    
    def _get_radio_input(self, options: List[Dict[str, Any]]) -> str:
        """
        获取单选输入
        """
        for i, option in enumerate(options, 1):
            print(f"{i}. {option.get('label')}")
        
        while True:
            try:
                choice = int(input(f"请选择 [1-{len(options)}]: "))
                if 1 <= choice <= len(options):
                    return options[choice - 1].get('value')
                else:
                    self.display_error(f"请输入1-{len(options)}之间的数字")
            except ValueError:
                self.display_error("请输入有效的数字")
    
    def _get_checkbox_input(self, options: List[Dict[str, Any]]) -> List[str]:
        """
        获取多选输入
        """
        for i, option in enumerate(options, 1):
            print(f"{i}. {option.get('label')}")
        
        print("请输入选择的选项编号（多个用逗号分隔）：")
        
        while True:
            try:
                input_str = input().strip()
                if not input_str:
                    return []
                
                selected_indices = [int(x.strip()) for x in input_str.split(',')]
                invalid = False
                
                for idx in selected_indices:
                    if idx < 1 or idx > len(options):
                        self.display_error(f"选项 {idx} 无效")
                        invalid = True
                        break
                
                if invalid:
                    continue
                
                return [options[idx - 1].get('value') for idx in selected_indices]
            except ValueError:
                self.display_error("请输入有效的数字")
    
    def _get_select_input(self, options: List[Dict[str, Any]]) -> str:
        """
        获取下拉选择输入（命令行中显示为列表选择）
        """
        return self._get_radio_input(options)
    
    def _get_rating_input(self, max_rating: int = 5) -> int:
        """
        获取评分输入
        """
        print(f"请输入评分（1-{max_rating}）：")
        
        while True:
            try:
                rating = int(input())
                if 1 <= rating <= max_rating:
                    return rating
                else:
                    self.display_error(f"请输入1-{max_rating}之间的数字")
            except ValueError:
                self.display_error("请输入有效的数字")
    
    def _get_file_input(self) -> str:
        """
        获取文件路径输入
        """
        while True:
            file_path = input("请输入文件路径：").strip()
            
            if not file_path:
                return ""
            
            # 检查文件是否存在
            if os.path.isfile(file_path):
                return file_path
            else:
                self.display_error(f"文件不存在：{file_path}")
                # 询问是否继续
                if not self.confirm_action("是否使用其他路径？"):
                    return ""
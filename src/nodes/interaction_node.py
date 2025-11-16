from .node_base import Node

class InteractionNode(Node):
    """
    交互节点，用于与用户交互，收集用户输入
    """
    def __init__(self, node_config):
        super().__init__(node_config)
        if self.type != 'interaction':
            raise ValueError("节点类型必须是'interaction'")
        self.form_config = self.config.get('form', [])
        self.message = self.config.get('message', '')
        self.outputs = node_config.get('outputs', [])
    
    def execute(self, workflow_engine, input_data=None):
        """
        执行交互节点逻辑
        
        Args:
            workflow_engine: 工作流引擎实例
            input_data: 输入数据（如果有）
            
        Returns:
            执行结果，包含表单配置和需要用户输入的信息
        """
        # 处理消息中的变量引用，如 {{basic_info.achievement_name}}
        processed_message = self._process_message(workflow_engine, self.message)
        
        return {
            'next_node': None,  # 交互节点需要等待用户输入后才能确定下一步
            'node': self.node_config,
            'node_type': self.type,
            'form_config': self.form_config,
            'message': processed_message,
            'outputs': self.outputs,
            'requires_input': True
        }
    
    def process_input(self, workflow_engine, form_data):
        """
        处理用户输入的数据
        
        Args:
            workflow_engine: 工作流引擎实例
            form_data: 用户提交的表单数据
            
        Returns:
            处理结果，包含下一个节点ID
        """
        # 验证表单数据
        is_valid, errors = self._validate_form_data(form_data)
        if not is_valid:
            return {
                'success': False,
                'errors': errors,
                'message': "表单验证失败"
            }
        
        # 保存输出变量
        if self.outputs and len(self.outputs) == 1:
            workflow_engine.set_variable(self.outputs[0], form_data)
        
        return {
            'success': True,
            'next_node': self.get_next_node_id(),
            'message': "表单提交成功"
        }
    
    def _process_message(self, workflow_engine, message):
        """
        处理消息中的变量引用
        
        Args:
            workflow_engine: 工作流引擎实例
            message: 原始消息
            
        Returns:
            处理后的消息
        """
        import re
        pattern = r'\{\{([^\}]+)\}\}'
        
        def replace_var(match):
            var_path = match.group(1).strip()
            # 获取变量值
            value = workflow_engine.get_variable(var_path.split('.')[0])
            
            # 处理嵌套变量，如 basic_info.achievement_name
            if '.' in var_path and value is not None:
                parts = var_path.split('.')
                for part in parts[1:]:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        value = f"{{未知变量: {var_path}}}"
                        break
            
            return str(value) if value is not None else f"{{未设置: {var_path}}}"
        
        return re.sub(pattern, replace_var, message)
    
    def _validate_form_data(self, form_data):
        """
        验证表单数据
        
        Args:
            form_data: 表单数据
            
        Returns:
            (is_valid, errors) - (是否有效，错误信息)
        """
        errors = []
        
        for field in self.form_config:
            field_key = field.get('key')
            field_required = field.get('required', False)
            field_type = field.get('type')
            
            # 检查必填字段
            if field_required and (field_key not in form_data or form_data[field_key] is None or form_data[field_key] == ''):
                errors.append(f"字段 '{field.get('label')}' 是必填项")
            
            # 检查字段类型
            if field_key in form_data and form_data[field_key] is not None:
                value = form_data[field_key]
                if field_type == 'number' and not isinstance(value, (int, float)):
                    errors.append(f"字段 '{field.get('label')}' 必须是数字")
                elif field_type == 'checkbox' and not isinstance(value, list):
                    errors.append(f"字段 '{field.get('label')}' 必须是复选框数组")
        
        return len(errors) == 0, errors
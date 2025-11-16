from .node_base import Node

class ConditionNode(Node):
    """
    条件节点，根据条件表达式判断工作流的执行路径
    """
    def __init__(self, node_config):
        super().__init__(node_config)
        if self.type != 'condition':
            raise ValueError("节点类型必须是'condition'")
        self.conditions = self.config.get('conditions', [])
    
    def execute(self, workflow_engine, input_data=None):
        """
        执行条件节点逻辑
        
        Args:
            workflow_engine: 工作流引擎实例
            input_data: 输入数据
            
        Returns:
            执行结果，包含根据条件判断得出的下一个节点ID
        """
        # 评估条件，获取下一个节点ID
        next_node_id = self._evaluate_conditions(workflow_engine)
        
        return {
            'next_node': next_node_id,
            'node': self.node_config,
            'node_type': self.type,
            'message': f"条件判断完成，下一节点: {next_node_id}"
        }
    
    def _evaluate_conditions(self, workflow_engine):
        """
        评估所有条件，返回满足条件的第一个下一个节点ID
        
        Args:
            workflow_engine: 工作流引擎实例
            
        Returns:
            下一个节点ID
        """
        for condition in self.conditions:
            expression = condition.get('expression')
            next_node = condition.get('next')
            
            if self._evaluate_expression(workflow_engine, expression):
                return next_node
        
        # 如果没有条件满足，返回默认的next
        return self.get_next_node_id()
    
    def _evaluate_expression(self, workflow_engine, expression):
        """
        评估表达式
        
        Args:
            workflow_engine: 工作流引擎实例
            expression: 表达式字符串
            
        Returns:
            表达式的计算结果(True/False)
        """
        try:
            # 替换变量引用 {{var_name}} 为实际值
            import re
            pattern = r'\{\{([^\}]+)\}\}'
            
            def replace_var(match):
                var_path = match.group(1).strip()
                # 获取变量值
                value = workflow_engine.get_variable(var_path.split('.')[0])
                
                # 处理嵌套变量，如 basic_info.achievement_owner
                if '.' in var_path and value is not None:
                    parts = var_path.split('.')
                    for part in parts[1:]:
                        if isinstance(value, dict) and part in value:
                            value = value[part]
                        else:
                            value = None
                            break
                
                # 对于列表类型的数据，需要特殊处理
                if isinstance(value, list):
                    return repr(value)
                return repr(str(value) if value is not None else '')
            
            # 替换 contains 操作符
            expression = expression.replace(' contains ', ' in ')
            expression = expression.replace('not contains', 'not in')
            
            # 替换变量引用
            eval_expression = re.sub(pattern, replace_var, expression)
            
            # 评估表达式
            # 注意：这里使用eval可能存在安全风险，实际生产环境应使用更安全的表达式解析方式
            return eval(eval_expression, {'__builtins__': {}})
        except Exception as e:
            print(f"表达式评估错误: {e}")
            return False
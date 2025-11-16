from src.services import (
    get_document_recognition_service,
    get_patent_query_service,
    get_analysis_service
)
from src.utils import get_logger, log_info, log_error

logger = get_logger(__name__)

class WorkflowEngine:
    """
    工作流引擎核心类，负责管理和执行工作流
    """
    def __init__(self, workflow_config=None):
        """
        初始化工作流引擎
        
        Args:
            workflow_config: 工作流配置字典
        """
        self.workflow_config = workflow_config or {}
        self.nodes = {}
        self.variables = {}
        self.current_node = None
        self.ai_services = {}
        self.ui = None
        self.is_initialized = False
        
        if workflow_config:
            self.initialize_nodes()
            self.initialize_variables()
    
    def initialize_nodes(self):
        """
        初始化工作流中的所有节点
        """
        for node in self.workflow_config.get('nodes', []):
            node_id = node.get('id')
            self.nodes[node_id] = node
    
    def initialize_variables(self):
        """
        初始化工作流变量
        """
        for var in self.workflow_config.get('variables', []):
            var_name = var.get('name')
            self.variables[var_name] = None
    
    def start(self):
        """
        启动工作流
        
        Returns:
            第一个节点的ID
        """
        start_node = None
        for node in self.nodes.values():
            if node.get('type') == 'start':
                start_node = node
                break
        
        if not start_node:
            raise ValueError("未找到启动节点")
        
        self.current_node = start_node
        return start_node.get('id')
    
    def execute_node(self, node_id, input_data=None):
        """
        执行指定节点
        
        Args:
            node_id: 节点ID
            input_data: 输入数据
            
        Returns:
            执行结果字典，包含下一个节点ID和节点配置
        """
        if node_id not in self.nodes:
            raise ValueError(f"节点 {node_id} 不存在")
        
        node = self.nodes[node_id]
        self.current_node = node
        
        # 处理输入数据，更新变量
        if input_data:
            self._update_variables(input_data)
        
        # 根据节点类型执行不同的逻辑
        node_type = node.get('type')
        if node_type == 'start' or node_type == 'end':
            next_node_id = node.get('next', '')
            return {
                'next_node': next_node_id,
                'node': node,
                'node_type': node_type
            }
        
        elif node_type == 'interaction':
            # 交互节点，返回表单配置供用户填写
            return {
                'next_node': None,  # 交互节点需要等待用户输入后才能确定下一步
                'node': node,
                'node_type': node_type,
                'form_config': node.get('config', {}),
                'outputs': node.get('outputs', [])
            }
        
        elif node_type == 'condition':
            # 条件节点，根据条件判断确定下一步
            next_node_id = self._evaluate_condition(node)
            return {
                'next_node': next_node_id,
                'node': node,
                'node_type': node_type
            }
        
        else:
            raise ValueError(f"不支持的节点类型: {node_type}")
    
    def process_interaction_result(self, node_id, form_data):
        """
        处理交互节点的结果
        
        Args:
            node_id: 节点ID
            form_data: 表单数据
            
        Returns:
            下一个节点ID
        """
        if node_id not in self.nodes:
            raise ValueError(f"节点 {node_id} 不存在")
        
        node = self.nodes[node_id]
        if node.get('type') != 'interaction':
            raise ValueError(f"节点 {node_id} 不是交互节点")
        
        # 保存输出变量
        outputs = node.get('outputs', [])
        if outputs and len(outputs) == 1:
            self.variables[outputs[0]] = form_data
        
        # 返回下一个节点ID
        return node.get('next', '')
    
    def _update_variables(self, data):
        """
        更新工作流变量
        
        Args:
            data: 要更新的数据
        """
        for key, value in data.items():
            if key in self.variables:
                self.variables[key] = value
    
    def _evaluate_condition(self, node):
        """
        评估条件节点
        
        Args:
            node: 条件节点配置
            
        Returns:
            下一个节点ID
        """
        conditions = node.get('config', {}).get('conditions', [])
        
        for condition in conditions:
            expression = condition.get('expression')
            next_node = condition.get('next')
            
            # 这里使用简单的表达式解析，实际使用时可以使用更复杂的表达式引擎
            if self._evaluate_expression(expression):
                return next_node
        
        # 如果没有条件满足，返回默认的next
        return node.get('next', '')
    
    def _evaluate_expression(self, expression):
        """
        评估表达式
        
        Args:
            expression: 表达式字符串
            
        Returns:
            表达式的计算结果(True/False)
        """
        # 简单的表达式解析，支持变量访问和基本的比较操作
        # 注意：这里使用eval可能存在安全风险，实际使用时应该使用更安全的表达式解析方式
        try:
            # 替换变量引用 {{var_name}} 为 self.variables['var_name']
            import re
            pattern = r'\{\{([^\}]+)\}\}'
            def replace_var(match):
                var_name = match.group(1).strip()
                if '.' in var_name:
                    # 处理嵌套变量，如 {{basic_info.achievement_owner}}
                    parts = var_name.split('.')
                    value = self.variables.get(parts[0])
                    for part in parts[1:]:
                        if isinstance(value, dict):
                            value = value.get(part)
                        else:
                            value = None
                            break
                    return repr(value)
                else:
                    return repr(self.variables.get(var_name))
            
            # 替换 contains 操作符
            expression = expression.replace(' contains ', ' in ')
            expression = expression.replace('not contains', 'not in')
            
            # 替换变量引用
            eval_expression = re.sub(pattern, replace_var, expression)
            
            # 评估表达式
            return eval(eval_expression, {'__builtins__': {}})
        except Exception as e:
            print(f"表达式评估错误: {e}")
            return False
    
    def get_variable(self, var_name):
        """
        获取工作流变量的值
        
        Args:
            var_name: 变量名
            
        Returns:
            变量值
        """
        return self.variables.get(var_name)
    
    def set_variable(self, var_name, value):
        """
        设置工作流变量的值
        
        Args:
            var_name: 变量名
            value: 变量值
        """
        self.variables[var_name] = value
    
    def get_current_state(self):
        """
        获取当前工作流状态
        
        Returns:
            当前状态字典
        """
        return {
            'current_node_id': self.current_node.get('id') if self.current_node else None,
            'variables': self.variables.copy(),
            'nodes': self.nodes
        }
    
    def initialize(self, config=None):
        """
        初始化工作流引擎和AI服务
        
        Args:
            config: 完整配置字典，包含豆包API配置等
        """
        try:
            config = config or {}
            self.workflow_config = config.get('workflow', {})
            self.initialize_nodes()
            self.initialize_variables()
            
            # 初始化AI服务，直接传入配置
            log_info("正在初始化AI服务...")
            self.ai_services['document_recognition'] = get_document_recognition_service(config)
            self.ai_services['patent_query'] = get_patent_query_service(config)
            self.ai_services['analysis'] = get_analysis_service(config)
            
            self.is_initialized = True
            log_info("工作流引擎初始化完成")
            return True
        except Exception as e:
            log_error(f"工作流引擎初始化失败: {str(e)}")
            return False
    
    def shutdown(self):
        """
        关闭工作流引擎，释放资源
        """
        try:
            # 关闭AI服务
            for service_name, service in self.ai_services.items():
                if hasattr(service, 'shutdown'):
                    service.shutdown()
            log_info("工作流引擎已关闭")
        except Exception as e:
            log_error(f"关闭工作流引擎时出错: {str(e)}")
    
    def run(self, ui):
        """
        运行工作流
        
        Args:
            ui: 用户界面实例
        """
        self.ui = ui
        
        try:
            # 启动工作流
            current_node_id = self.start()
            
            while current_node_id:
                # 执行当前节点
                result = self.execute_node(current_node_id)
                
                if result['node_type'] == 'end':
                    # 结束节点，退出循环
                    ui.display_message("工作流执行完成！")
                    break
                
                elif result['node_type'] == 'interaction':
                    # 交互节点，显示表单并获取用户输入
                    form_config = result.get('form_config', {})
                    message = result.get('message', '')
                    
                    if message:
                        ui.display_message(message)
                    
                    # 显示表单并获取输入
                    form_data = ui.display_form(form_config)
                    
                    # 处理交互结果，获取下一个节点
                    current_node_id = self.process_interaction_result(current_node_id, form_data)
                
                else:
                    # 普通节点，直接获取下一个节点
                    current_node_id = result.get('next_node')
                    
        except Exception as e:
            log_error(f"工作流执行出错: {str(e)}")
            ui.display_error(f"执行出错: {str(e)}")
    
    def get_ai_service(self, service_name):
        """
        获取AI服务实例
        
        Args:
            service_name: 服务名称 ('document_recognition', 'patent_query', 'analysis')
            
        Returns:
            对应的AI服务实例
        """
        return self.ai_services.get(service_name)
    
    def execute(self, ui):
        """
        兼容旧版API的执行方法
        """
        self.run(ui)
        return True
    
    def get_variables(self):
        """
        兼容旧版API的获取变量方法
        """
        return self.variables
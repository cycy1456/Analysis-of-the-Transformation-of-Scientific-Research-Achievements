from .node_base import Node

class StartNode(Node):
    """
    开始节点，工作流的入口点
    """
    def __init__(self, node_config):
        super().__init__(node_config)
        if self.type != 'start':
            raise ValueError("节点类型必须是'start'")
    
    def execute(self, workflow_engine, input_data=None):
        """
        执行开始节点逻辑
        
        Args:
            workflow_engine: 工作流引擎实例
            input_data: 输入数据（开始节点通常不需要输入）
            
        Returns:
            执行结果，包含下一个节点ID和节点信息
        """
        return {
            'next_node': self.get_next_node_id(),
            'node': self.node_config,
            'node_type': self.type,
            'message': f"工作流已启动: {self.name}"
        }
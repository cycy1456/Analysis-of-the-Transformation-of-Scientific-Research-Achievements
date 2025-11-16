from .node_base import Node

class EndNode(Node):
    """
    结束节点，工作流的结束点
    """
    def __init__(self, node_config):
        super().__init__(node_config)
        if self.type != 'end':
            raise ValueError("节点类型必须是'end'")
    
    def execute(self, workflow_engine, input_data=None):
        """
        执行结束节点逻辑
        
        Args:
            workflow_engine: 工作流引擎实例
            input_data: 输入数据
            
        Returns:
            执行结果，包含结束信息
        """
        return {
            'next_node': None,  # 结束节点没有下一个节点
            'node': self.node_config,
            'node_type': self.type,
            'message': f"工作流已结束: {self.name}",
            'workflow_completed': True
        }
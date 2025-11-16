class Node:
    """
    节点基类，所有具体节点类型的父类
    """
    def __init__(self, node_config):
        """
        初始化节点
        
        Args:
            node_config: 节点配置字典
        """
        self.node_config = node_config
        self.id = node_config.get('id')
        self.type = node_config.get('type')
        self.name = node_config.get('name')
        self.next = node_config.get('next', '')
        self.position = node_config.get('position', [0, 0])
        self.config = node_config.get('config', {})
    
    def execute(self, workflow_engine, input_data=None):
        """
        执行节点逻辑
        
        Args:
            workflow_engine: 工作流引擎实例
            input_data: 输入数据
            
        Returns:
            执行结果
        """
        raise NotImplementedError("子类必须实现execute方法")
    
    def get_next_node_id(self):
        """
        获取下一个节点ID
        
        Returns:
            下一个节点ID
        """
        return self.next
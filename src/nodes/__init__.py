from .node_base import Node
from .start_node import StartNode
from .end_node import EndNode
from .interaction_node import InteractionNode
from .condition_node import ConditionNode

# 创建节点类型映射
def get_node_class(node_type):
    """
    根据节点类型获取对应的节点类
    
    Args:
        node_type: 节点类型字符串
        
    Returns:
        节点类
    """
    node_classes = {
        'start': StartNode,
        'end': EndNode,
        'interaction': InteractionNode,
        'condition': ConditionNode
    }
    return node_classes.get(node_type)

__all__ = ['Node', 'StartNode', 'EndNode', 'InteractionNode', 'ConditionNode', 'get_node_class']
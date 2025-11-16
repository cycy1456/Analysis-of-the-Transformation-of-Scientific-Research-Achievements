import json
import os
from typing import Dict, Any

class ConfigLoader:
    """
    配置加载器，负责从文件加载工作流配置
    """
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        从文件加载配置
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
            
        Raises:
            FileNotFoundError: 配置文件不存在
            json.JSONDecodeError: 配置文件格式错误
            ValueError: 配置验证失败
        """
        # 检查文件是否存在
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        # 读取并解析JSON文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 验证配置
        ConfigLoader._validate_config(config)
        
        return config
    
    @staticmethod
    def _validate_config(config: Dict[str, Any]) -> None:
        """
        验证配置的有效性
        
        Args:
            config: 配置字典
            
        Raises:
            ValueError: 配置验证失败
        """
        # 检查必要字段
        required_fields = ['name', 'nodes']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"配置缺少必要字段: {field}")
        
        # 检查节点配置
        nodes = config.get('nodes', [])
        if not isinstance(nodes, list) or len(nodes) == 0:
            raise ValueError("配置中的nodes必须是非空数组")
        
        # 检查是否有且只有一个开始节点
        start_nodes = [node for node in nodes if node.get('type') == 'start']
        if len(start_nodes) != 1:
            raise ValueError(f"配置必须包含且只包含一个开始节点，当前有: {len(start_nodes)}")
        
        # 检查节点ID唯一性
        node_ids = []
        for node in nodes:
            node_id = node.get('id')
            if not node_id:
                raise ValueError("节点缺少id字段")
            if node_id in node_ids:
                raise ValueError(f"节点ID重复: {node_id}")
            node_ids.append(node_id)
        
        # 检查节点类型
        valid_node_types = ['start', 'end', 'interaction', 'condition']
        for node in nodes:
            node_type = node.get('type')
            if node_type not in valid_node_types:
                raise ValueError(f"无效的节点类型: {node_type}，节点ID: {node.get('id')}")
        
        # 检查交互节点的配置
        for node in nodes:
            if node.get('type') == 'interaction':
                config_data = node.get('config', {})
                if 'form' not in config_data:
                    raise ValueError(f"交互节点缺少form配置，节点ID: {node.get('id')}")
                if not isinstance(config_data['form'], list):
                    raise ValueError(f"交互节点的form必须是数组，节点ID: {node.get('id')}")
        
        # 检查条件节点的配置
        for node in nodes:
            if node.get('type') == 'condition':
                config_data = node.get('config', {})
                if 'conditions' not in config_data:
                    raise ValueError(f"条件节点缺少conditions配置，节点ID: {node.get('id')}")
                if not isinstance(config_data['conditions'], list):
                    raise ValueError(f"条件节点的conditions必须是数组，节点ID: {node.get('id')}")
                # 检查条件配置
                for condition in config_data['conditions']:
                    if 'expression' not in condition:
                        raise ValueError(f"条件缺少expression字段，节点ID: {node.get('id')}")
                    if 'next' not in condition:
                        raise ValueError(f"条件缺少next字段，节点ID: {node.get('id')}")
        
        # 检查节点引用的有效性
        for node in nodes:
            if node.get('type') != 'end':  # 结束节点没有next
                next_node = node.get('next')
                if next_node and next_node not in node_ids:
                    raise ValueError(f"节点引用了不存在的下一个节点: {next_node}，当前节点ID: {node.get('id')}")
        
        print("配置验证成功")
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str) -> None:
        """
        保存配置到文件
        
        Args:
            config: 配置字典
            config_path: 配置文件路径
        """
        # 确保目录存在
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"配置已保存到: {config_path}")
    
    @staticmethod
    def get_default_config_path() -> str:
        """
        获取默认配置文件路径
        
        Returns:
            默认配置文件路径
        """
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(current_dir, 'config', 'workflow_config.json')
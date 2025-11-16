"""
科研成果转化分析智能体 - AI服务使用示例

此脚本演示如何直接使用豆包API的文档识别和专利查询等服务
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services import (
    get_document_recognition_service,
    get_patent_query_service,
    get_analysis_service
)
from src.utils import get_logger, log_info

# 获取日志记录器
logger = get_logger('ai_service_example')

# 豆包API配置
DOUBAO_CONFIG = {
    "api_key": "95ece695-1aea-4add-b131-31b2fd72fec5",
    "model": "ERNIE-Bot-4"
}

def demo_document_recognition():
    """
    演示文档识别服务（使用豆包API）
    """
    print("\n=== 文档识别服务演示 ===")
    try:
        # 获取文档识别服务实例（使用豆包API）
        doc_service = get_document_recognition_service(DOUBAO_CONFIG)
        
        # 注意：当前使用的是模拟服务，无需真实文件
        # 在实际应用中，需要提供真实的文件路径
        mock_file_path = "path/to/your/research_paper.pdf"
        
        log_info(f"识别文档: {mock_file_path}")
        print(f"正在使用豆包API识别文档: {mock_file_path}")
        
        # 调用文档识别服务
        result = doc_service.recognize_document(mock_file_path)
        
        print("\n识别结果:")
        print(f"标题: {result.get('title', '未识别')}")
        print(f"作者: {result.get('authors', '未识别')}")
        print(f"摘要: {result.get('abstract', '未识别')}")
        print(f"关键词: {', '.join(result.get('keywords', []))}")
        print(f"主要发现: {result.get('key_findings', '未识别')}")
        
        return result
        
    except Exception as e:
        print(f"文档识别失败: {str(e)}")
        return None

def demo_patent_query():
    """
    演示专利查询服务（使用豆包API）
    """
    print("\n=== 专利查询服务演示 ===")
    try:
        # 获取专利查询服务实例（使用豆包API）
        patent_service = get_patent_query_service(DOUBAO_CONFIG)
        
        # 构建查询参数
        query_params = {
            'keywords': "人工智能 机器学习 自然语言处理",
            'applicant': None,  # 可选：申请人名称
            'inventor': None,   # 可选：发明人
            'start_date': "2020-01-01",
            'end_date': "2023-12-31",
            'limit': 5
        }
        
        log_info(f"查询专利，关键词: {query_params['keywords']}")
        print(f"正在使用豆包API查询专利，关键词: {query_params['keywords']}")
        
        # 调用专利查询服务
        results = patent_service.query_patents(query_params)
        
        print(f"\n查询结果 (共找到 {len(results)} 条相关专利):")
        for i, patent in enumerate(results, 1):
            print(f"\n{i}. 专利名称: {patent.get('title', '未知')}")
            print(f"   专利号: {patent.get('patent_number', '未知')}")
            print(f"   申请日期: {patent.get('application_date', '未知')}")
            print(f"   申请人: {patent.get('applicant', '未知')}")
            print(f"   摘要: {patent.get('abstract', '未知')[:100]}...")
        
        return results
        
    except Exception as e:
        print(f"专利查询失败: {str(e)}")
        return None

def demo_analysis_service():
    """
    演示分析服务（使用豆包API）
    """
    print("\n=== 分析服务演示 ===")
    try:
        # 获取分析服务实例（使用豆包API）
        analysis_service = get_analysis_service(DOUBAO_CONFIG)
        
        # 准备分析数据
        analysis_data = {
            'title': "基于深度学习的医学图像分析系统",
            'field': "人工智能 医学影像",
            'description': "本系统利用深度学习技术对医学影像进行自动分析，辅助医生进行诊断。",
            'maturity': "prototype",
            'has_patent': True,
            'patent_status': "applied",
            'target_audience': "医院、诊所、医学研究机构"
        }
        
        log_info(f"分析科研成果: {analysis_data['title']}")
        print(f"正在使用豆包API分析科研成果: {analysis_data['title']}")
        
        # 调用分析服务
        analysis_result = analysis_service.analyze_achievement(analysis_data)
        
        print("\n分析结果:")
        print(f"转化潜力评分: {analysis_result.get('conversion_potential_score', '未评分')}/10")
        print(f"\n优势:")
        for advantage in analysis_result.get('advantages', []):
            print(f"- {advantage}")
        
        print(f"\n风险:")
        for risk in analysis_result.get('risks', []):
            print(f"- {risk}")
        
        print(f"\n建议:")
        for suggestion in analysis_result.get('suggestions', []):
            print(f"- {suggestion}")
        
        return analysis_result
        
    except Exception as e:
        print(f"分析失败: {str(e)}")
        return None

def main():
    """
    AI服务示例主函数
    """
    print("科研成果转化分析智能体 - AI服务使用示例")
    print("================================================")
    print("本示例展示如何直接使用系统中的AI服务组件")
    print("注意：当前使用的是模拟服务，实际应用时可替换为真实服务实现")
    
    # 演示文档识别服务
    doc_result = demo_document_recognition()
    
    # 演示专利查询服务
    patent_results = demo_patent_query()
    
    # 演示分析服务
    analysis_result = demo_analysis_service()
    
    print("\n================================================")
    print("AI服务示例演示完成！")
    print("提示：在实际应用中，您需要实现真实的服务接口来连接到实际的AI服务API")


if __name__ == "__main__":
    main()
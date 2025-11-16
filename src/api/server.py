"""FastAPI服务器配置"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio
from typing import Dict

from .routes import router
from ..config.config_loader import load_config
from ..utils.logger import get_logger
from ..services import get_analysis_service

logger = get_logger(__name__)
config = load_config()

# 连接管理器类
class ConnectionManager:
    def __init__(self):
        # 存储活动连接
        self.active_connections: Dict[str, WebSocket] = {}
        # 存储对话历史
        self.conversation_history: Dict[str, list] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.conversation_history[client_id] = []
        logger.info(f"客户端 {client_id} 已连接")
        
        # 发送欢迎消息
        welcome_message = {
            "sender": "bot",
            "text": "您好！我是科研成果转化分析智能体，很高兴为您提供服务。您可以咨询关于科研成果转化的问题，或者获取详细的成果评估。",
            "timestamp": asyncio.get_event_loop().time()
        }
        await websocket.send_json(welcome_message)
        self.conversation_history[client_id].append(welcome_message)
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.conversation_history:
            del self.conversation_history[client_id]
        logger.info(f"客户端 {client_id} 已断开连接")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    def add_to_history(self, client_id: str, message: dict):
        if client_id in self.conversation_history:
            self.conversation_history[client_id].append(message)
            # 限制历史记录长度，避免内存占用过大
            if len(self.conversation_history[client_id]) > 50:
                self.conversation_history[client_id] = self.conversation_history[client_id][-50:]

manager = ConnectionManager()

def create_app():
    """创建FastAPI应用实例"""
    app = FastAPI(
        title="科研成果转化分析API",
        description="为科研成果提供市场分析、专利评估和转化策略的智能服务API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # 配置CORS中间件，允许前端跨域访问
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:5173",
            "https://yourusername.github.io",
            "/"
        ],  # 在生产环境中应该限制具体的域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 初始化服务
    analysis_service = get_analysis_service()
    
    # WebSocket 端点
    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: str):
        await manager.connect(websocket, client_id)
        
        try:
            while True:
                # 接收客户端消息
                data = await websocket.receive_text()
                logger.info(f"收到客户端 {client_id} 的消息: {data}")
                
                # 构建用户消息对象
                user_message = {
                    "sender": "user",
                    "text": data,
                    "timestamp": asyncio.get_event_loop().time()
                }
                
                # 添加到对话历史
                manager.add_to_history(client_id, user_message)
                
                # 发送确认消息给客户端（回显）
                await manager.send_personal_message(user_message, websocket)
                
                # 准备AI响应
                await manager.send_personal_message({"sender": "bot", "is_typing": True}, websocket)
                
                try:
                    # 获取对话历史上下文
                    history = manager.conversation_history.get(client_id, [])
                    context = "\n".join([f"{msg['sender']}: {msg['text']}" for msg in history])
                    
                    # 调用分析服务获取智能体响应
                    # 这里根据实际服务接口调整参数
                    response_text = await asyncio.to_thread(
                        analysis_service.analyze_text,
                        data,  # 用户当前消息
                        context=context  # 对话历史上下文
                    )
                    
                    # 如果没有得到有效响应，使用默认回复
                    if not response_text or response_text.strip() == "":
                        response_text = "抱歉，我无法理解您的问题。请尝试用不同的方式表述，或者提出关于科研成果转化的具体问题。"
                    
                except Exception as e:
                    logger.error(f"处理消息时出错: {str(e)}")
                    response_text = "抱歉，处理您的请求时发生了错误。请稍后再试。"
                
                # 构建AI响应消息
                bot_message = {
                    "sender": "bot",
                    "text": response_text,
                    "timestamp": asyncio.get_event_loop().time()
                }
                
                # 添加到对话历史
                manager.add_to_history(client_id, bot_message)
                
                # 发送AI响应
                await manager.send_personal_message({"sender": "bot", "is_typing": False}, websocket)
                await manager.send_personal_message(bot_message, websocket)
                
        except WebSocketDisconnect:
            manager.disconnect(client_id)
        except Exception as e:
            logger.error(f"WebSocket错误: {str(e)}")
            manager.disconnect(client_id)
    
    # 注册路由
    app.include_router(router, prefix="/api")
    
    # 根路径
    @app.get("/")
    async def root():
        return {
            "message": "欢迎使用科研成果转化分析API",
            "docs": "/docs",
            "api_version": "1.0.0"
        }
    
    # 健康检查端点
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    # 启动事件
    @app.on_event("startup")
    async def startup_event():
        logger.info("API服务启动成功")
        logger.info(f"文档地址: http://localhost:{config.get('api', {}).get('port', 8000)}/docs")
    
    # 关闭事件
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("API服务正在关闭")
    
    return app

# 创建应用实例
app = create_app()

def run_server():
    """启动API服务器"""
    api_config = config.get('api', {})
    port = api_config.get('port', 8000)
    host = api_config.get('host', '0.0.0.0')
    reload = api_config.get('reload', False)
    
    logger.info(f"启动API服务器: {host}:{port}")
    
    uvicorn.run(
        "src.api.server:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    run_server()
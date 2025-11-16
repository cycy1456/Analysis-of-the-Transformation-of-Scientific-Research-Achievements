"""FastAPI服务器配置"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .routes import router
from ..config.config_loader import load_config
from ..utils.logger import get_logger

logger = get_logger(__name__)
config = load_config()

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
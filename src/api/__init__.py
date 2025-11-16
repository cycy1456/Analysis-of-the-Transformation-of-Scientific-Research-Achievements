"""API模块，提供RESTful接口服务"""

from .routes import router
from .server import create_app

__all__ = ['router', 'create_app']
#!/bin/bash

# 科研成果转化智能体部署脚本
# 用于自动化构建前端应用并部署到GitHub Pages

set -e  # 遇到错误时停止执行

echo "========================================"
echo "科研成果转化智能体部署脚本"
echo "========================================"

# 检查当前目录
CURRENT_DIR=$(pwd)
echo "当前工作目录: $CURRENT_DIR"

# 确保在项目根目录
if [ ! -d "web" ] || [ ! -f "src/main.py" ]; then
  echo "错误: 请在项目根目录执行此脚本"
  exit 1
fi

# 进入前端目录
cd web
echo "进入前端目录: $(pwd)"

# 检查依赖是否安装
if [ ! -d "node_modules" ]; then
  echo "正在安装前端依赖..."
  npm install
else
  echo "更新前端依赖..."
  npm update
fi

# 构建前端应用
echo "构建前端应用..."
npm run build

# 检查构建是否成功
if [ ! -d "dist" ]; then
  echo "错误: 前端构建失败，dist目录不存在"
  exit 1
fi

# 部署到GitHub Pages
echo "部署到GitHub Pages..."
npm run deploy

# 检查部署是否成功
if [ $? -eq 0 ]; then
  echo "========================================"
  echo "✅ 部署成功!"
  echo "========================================"
  echo "应用已部署到 GitHub Pages"
  echo "访问地址: https://<your-github-username>.github.io/scientific-achievement-agent/"
  echo ""
  echo "注意: 请将 <your-github-username> 替换为您的GitHub用户名"
  echo "========================================"
else
  echo "========================================"
  echo "❌ 部署失败!"
  echo "========================================"
  echo "请检查错误信息并重试"
  exit 1
fi

# 返回项目根目录
cd ..
echo "已返回项目根目录: $(pwd)"

# 提示后端部署信息
echo ""
echo "========================================"
echo "后端部署建议:"
echo "========================================"
echo "1. 后端API服务可以部署到云服务提供商，如:"
echo "   - Vercel Functions"
echo "   - Netlify Functions"
echo "   - AWS Lambda + API Gateway"
echo "   - Google Cloud Functions"
echo "   - 阿里云函数计算"
echo ""
echo "2. 部署前请确保:"
echo "   - 配置正确的API密钥"
echo "   - 设置适当的环境变量"
echo "   - 配置CORS以允许前端访问"
echo ""
echo "3. 更新前端配置:"
echo "   - 修改 web/src/config/apiConfig.js 中的 API_BASE_URL 为您的后端API地址"
echo "========================================"
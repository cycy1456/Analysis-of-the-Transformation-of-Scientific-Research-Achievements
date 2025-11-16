# 科研成果转化智能体部署脚本（Windows PowerShell版本）
# 用于自动化构建前端应用并部署到GitHub Pages

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "科研成果转化智能体部署脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 检查当前目录
$CurrentDir = Get-Location
Write-Host "当前工作目录: $CurrentDir" -ForegroundColor Green

# 确保在项目根目录
if (!(Test-Path -Path ".\web" -PathType Container) -or !(Test-Path -Path ".\src\main.py" -PathType Leaf)) {
    Write-Host "错误: 请在项目根目录执行此脚本" -ForegroundColor Red
    exit 1
}

# 进入前端目录
Set-Location -Path ".\web"
Write-Host "进入前端目录: $(Get-Location)" -ForegroundColor Green

# 检查Node.js是否安装
try {
    $nodeVersion = node -v
    Write-Host "Node.js版本: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: 未找到Node.js，请先安装Node.js" -ForegroundColor Red
    exit 1
}

# 检查npm是否安装
try {
    $npmVersion = npm -v
    Write-Host "npm版本: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: 未找到npm，请先安装npm" -ForegroundColor Red
    exit 1
}

# 检查依赖是否安装
if (!(Test-Path -Path ".\node_modules" -PathType Container)) {
    Write-Host "正在安装前端依赖..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "错误: 安装依赖失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "更新前端依赖..." -ForegroundColor Yellow
    npm update
    if ($LASTEXITCODE -ne 0) {
        Write-Host "错误: 更新依赖失败" -ForegroundColor Red
        exit 1
    }
}

# 构建前端应用
Write-Host "构建前端应用..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 前端构建失败" -ForegroundColor Red
    exit 1
}

# 检查构建是否成功
if (!(Test-Path -Path ".\dist" -PathType Container)) {
    Write-Host "错误: 前端构建失败，dist目录不存在" -ForegroundColor Red
    exit 1
}

# 部署到GitHub Pages
Write-Host "部署到GitHub Pages..." -ForegroundColor Yellow
npm run deploy
if ($LASTEXITCODE -eq 0) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ 部署成功!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "应用已部署到 GitHub Pages" -ForegroundColor Green
    Write-Host "访问地址: https://<your-github-username>.github.io/scientific-achievement-agent/" -ForegroundColor Green
    Write-Host "" -ForegroundColor Green
    Write-Host "注意: 请将 <your-github-username> 替换为您的GitHub用户名" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ 部署失败!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "请检查错误信息并重试" -ForegroundColor Red
    exit 1
}

# 返回项目根目录
Set-Location -Path ".."
Write-Host "已返回项目根目录: $(Get-Location)" -ForegroundColor Green

# 提示后端部署信息
Write-Host "" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "后端部署建议:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. 后端API服务可以部署到云服务提供商，如:" -ForegroundColor Yellow
Write-Host "   - Vercel Functions" -ForegroundColor Yellow
Write-Host "   - Netlify Functions" -ForegroundColor Yellow
Write-Host "   - AWS Lambda + API Gateway" -ForegroundColor Yellow
Write-Host "   - Google Cloud Functions" -ForegroundColor Yellow
Write-Host "   - 阿里云函数计算" -ForegroundColor Yellow
Write-Host "" -ForegroundColor Cyan
Write-Host "2. 部署前请确保:" -ForegroundColor Yellow
Write-Host "   - 配置正确的API密钥" -ForegroundColor Yellow
Write-Host "   - 设置适当的环境变量" -ForegroundColor Yellow
Write-Host "   - 配置CORS以允许前端访问" -ForegroundColor Yellow
Write-Host "" -ForegroundColor Cyan
Write-Host "3. 更新前端配置:" -ForegroundColor Yellow
Write-Host "   - 修改 web/src/config/apiConfig.js 中的 API_BASE_URL 为您的后端API地址" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
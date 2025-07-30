#!/bin/bash

# 云主机到Serverless自动化部署脚本
# 使用方法: ./deploy.sh [platform] [stage]
# 平台选项: aws, aliyun, tencent, docker, local
# 环境选项: dev, test, prod

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    echo "用户管理API - Serverless部署脚本"
    echo ""
    echo "使用方法:"
    echo "  $0 [platform] [stage]"
    echo ""
    echo "平台选项:"
    echo "  aws      - 部署到AWS Lambda"
    echo "  aliyun   - 部署到阿里云函数计算"
    echo "  tencent  - 部署到腾讯云函数"
    echo "  docker   - 构建Docker镜像"
    echo "  local    - 本地开发服务器"
    echo ""
    echo "环境选项:"
    echo "  dev      - 开发环境"
    echo "  test     - 测试环境"
    echo "  prod     - 生产环境"
    echo ""
    echo "示例:"
    echo "  $0 aws prod    # 部署到AWS生产环境"
    echo "  $0 local dev   # 启动本地开发服务器"
    echo "  $0 docker      # 构建Docker镜像"
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装"
        exit 1
    fi
    
    # 检查pip
    if ! command -v pip &> /dev/null; then
        log_error "pip 未安装"
        exit 1
    fi
    
    log_success "系统依赖检查通过"
}

# 安装Python依赖
install_python_deps() {
    log_info "安装Python依赖..."
    
    if [ -f "deployment/requirements.txt" ]; then
        pip install -r deployment/requirements.txt
        log_success "Python依赖安装完成"
    else
        log_error "未找到requirements.txt文件"
        exit 1
    fi
}

# 运行测试
run_tests() {
    log_info "运行测试套件..."
    
    # 设置测试环境
    export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
    
    # 运行单元测试
    if [ -d "tests" ]; then
        python -m pytest tests/ -v --tb=short
        if [ $? -eq 0 ]; then
            log_success "所有测试通过"
        else
            log_error "测试失败，停止部署"
            exit 1
        fi
    else
        log_warning "未找到测试目录，跳过测试"
    fi
}

# 检查配置文件
check_config() {
    local platform=$1
    local stage=$2
    
    log_info "检查配置文件..."
    
    case $platform in
        "aws")
            if [ ! -f "deployment/serverless.yml" ]; then
                log_error "未找到serverless.yml配置文件"
                exit 1
            fi
            
            # 检查AWS CLI
            if ! command -v aws &> /dev/null; then
                log_warning "AWS CLI 未安装，建议安装以便配置凭证"
            fi
            ;;
        "aliyun")
            if [ ! -f "deployment/fun.yml" ]; then
                log_warning "未找到fun.yml配置文件，将使用默认配置"
            fi
            ;;
        "tencent")
            if [ ! -f "deployment/serverless-tencent.yml" ]; then
                log_warning "未找到腾讯云配置文件，将使用默认配置"
            fi
            ;;
        "docker")
            if [ ! -f "deployment/Dockerfile" ]; then
                log_error "未找到Dockerfile"
                exit 1
            fi
            ;;
    esac
    
    log_success "配置文件检查完成"
}

# AWS Lambda部署
deploy_aws() {
    local stage=$1
    
    log_info "部署到AWS Lambda ($stage环境)..."
    
    # 检查Serverless Framework
    if ! command -v serverless &> /dev/null; then
        log_info "安装Serverless Framework..."
        npm install -g serverless
    fi
    
    # 检查插件
    cd deployment
    if [ ! -d "node_modules" ]; then
        log_info "安装Serverless插件..."
        npm init -y
        npm install --save-dev serverless-python-requirements serverless-plugin-warmup
    fi
    
    # 部署
    log_info "执行部署..."
    serverless deploy --stage $stage --verbose
    
    if [ $? -eq 0 ]; then
        log_success "AWS Lambda部署成功"
        
        # 获取API端点
        API_URL=$(serverless info --stage $stage | grep "endpoints:" -A 1 | tail -n 1 | awk '{print $2}')
        if [ ! -z "$API_URL" ]; then
            log_info "API端点: $API_URL"
            
            # 健康检查
            log_info "执行健康检查..."
            if curl -s "$API_URL" > /dev/null; then
                log_success "健康检查通过"
            else
                log_warning "健康检查失败"
            fi
        fi
    else
        log_error "AWS Lambda部署失败"
        exit 1
    fi
    
    cd ..
}

# 阿里云函数计算部署
deploy_aliyun() {
    local stage=$1
    
    log_info "部署到阿里云函数计算 ($stage环境)..."
    
    # 检查Fun工具
    if ! command -v fun &> /dev/null; then
        log_info "安装Fun工具..."
        npm install @alicloud/fun -g
    fi
    
    cd deployment
    
    # 创建fun.yml（如果不存在）
    if [ ! -f "fun.yml" ]; then
        log_info "创建阿里云配置文件..."
        cat > fun.yml << EOF
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'Aliyun::Serverless-2018-04-03'
Resources:
  user-api:
    Type: 'Aliyun::Serverless::Service'
    Properties:
      Description: '用户管理API服务'
    api:
      Type: 'Aliyun::Serverless::Function'
      Properties:
        Handler: src.handler.aliyun_handler
        Runtime: python3.9
        CodeUri: '../'
        MemorySize: 256
        Timeout: 30
        Events:
          httpTrigger:
            Type: HTTP
            Properties:
              AuthType: ANONYMOUS
              Methods: ['GET', 'POST', 'PUT', 'DELETE']
EOF
    fi
    
    # 部署
    fun deploy
    
    if [ $? -eq 0 ]; then
        log_success "阿里云函数计算部署成功"
    else
        log_error "阿里云函数计算部署失败"
        exit 1
    fi
    
    cd ..
}

# 腾讯云函数部署
deploy_tencent() {
    local stage=$1
    
    log_info "部署到腾讯云函数 ($stage环境)..."
    
    # 检查Serverless Framework
    if ! command -v serverless &> /dev/null; then
        log_info "安装Serverless Framework..."
        npm install -g serverless
    fi
    
    cd deployment
    
    # 创建腾讯云配置文件（如果不存在）
    if [ ! -f "serverless-tencent.yml" ]; then
        log_info "创建腾讯云配置文件..."
        cat > serverless-tencent.yml << EOF
component: scf
name: user-api

inputs:
  name: user-management-api
  src: ../src
  handler: handler.tencent_handler
  runtime: Python3.6
  region: ap-guangzhou
  events:
    - apigw:
        parameters:
          protocols:
            - http
            - https
          serviceName: user-api
          description: 用户管理API
          environment: release
          endpoints:
            - path: /
              method: ANY
EOF
    fi
    
    # 部署
    serverless deploy --config serverless-tencent.yml
    
    if [ $? -eq 0 ]; then
        log_success "腾讯云函数部署成功"
    else
        log_error "腾讯云函数部署失败"
        exit 1
    fi
    
    cd ..
}

# Docker部署
deploy_docker() {
    local tag=${1:-latest}
    
    log_info "构建Docker镜像..."
    
    # 构建镜像
    docker build -t user-management-api:$tag -f deployment/Dockerfile .
    
    if [ $? -eq 0 ]; then
        log_success "Docker镜像构建成功"
        
        # 可选：推送到registry
        read -p "是否推送到Docker Registry? (y/N): " push_choice
        if [[ $push_choice =~ ^[Yy]$ ]]; then
            read -p "输入Registry地址 (如: your-registry.com/user-api): " registry_url
            if [ ! -z "$registry_url" ]; then
                docker tag user-management-api:$tag $registry_url:$tag
                docker push $registry_url:$tag
                log_success "镜像推送成功: $registry_url:$tag"
            fi
        fi
        
        # 运行容器（可选）
        read -p "是否立即运行容器? (y/N): " run_choice
        if [[ $run_choice =~ ^[Yy]$ ]]; then
            docker run -d -p 8000:8000 --name user-api user-management-api:$tag
            log_success "容器已启动: http://localhost:8000"
        fi
    else
        log_error "Docker镜像构建失败"
        exit 1
    fi
}

# 本地开发服务器
deploy_local() {
    log_info "启动本地开发服务器..."
    
    export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
    
    # 检查端口
    PORT=${PORT:-8000}
    if lsof -i :$PORT &> /dev/null; then
        log_warning "端口 $PORT 已被占用"
        read -p "是否使用其他端口? 输入端口号或回车使用8001: " new_port
        PORT=${new_port:-8001}
    fi
    
    log_info "启动服务器在端口 $PORT..."
    cd src
    python app.py --host 0.0.0.0 --port $PORT
}

# 部署后测试
post_deploy_test() {
    local api_url=$1
    
    if [ -z "$api_url" ]; then
        log_warning "未提供API URL，跳过部署后测试"
        return
    fi
    
    log_info "执行部署后测试..."
    
    # 基础健康检查
    if curl -s "$api_url" > /dev/null; then
        log_success "健康检查通过"
    else
        log_error "健康检查失败"
        return 1
    fi
    
    # API功能测试
    if [ -f "tests/load_test.py" ]; then
        log_info "执行API功能测试..."
        python tests/load_test.py --url "$api_url" --users 2 --duration 10
    fi
}

# 清理函数
cleanup() {
    log_info "清理临时文件..."
    
    # 清理缓存
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # 清理测试报告
    find . -name "*_test_*.json" -mtime +7 -delete 2>/dev/null || true
    
    log_success "清理完成"
}

# 主函数
main() {
    local platform=${1:-help}
    local stage=${2:-dev}
    
    # 显示帮助
    if [ "$platform" = "help" ] || [ "$platform" = "-h" ] || [ "$platform" = "--help" ]; then
        show_help
        exit 0
    fi
    
    log_info "开始部署流程..."
    log_info "平台: $platform"
    log_info "环境: $stage"
    
    # 检查依赖
    check_dependencies
    
    # 安装Python依赖
    install_python_deps
    
    # 检查配置
    check_config $platform $stage
    
    # 运行测试（生产环境必须通过测试）
    if [ "$stage" = "prod" ] || [ "$1" = "test" ]; then
        run_tests
    fi
    
    # 根据平台执行部署
    case $platform in
        "aws")
            deploy_aws $stage
            ;;
        "aliyun")
            deploy_aliyun $stage
            ;;
        "tencent")
            deploy_tencent $stage
            ;;
        "docker")
            deploy_docker $stage
            ;;
        "local")
            deploy_local
            ;;
        *)
            log_error "不支持的平台: $platform"
            show_help
            exit 1
            ;;
    esac
    
    # 清理
    cleanup
    
    log_success "部署流程完成！"
}

# 捕获中断信号
trap cleanup EXIT

# 执行主函数
main "$@" 
FROM public.ecr.aws/lambda/python:3.9

# 设置工作目录
WORKDIR ${LAMBDA_TASK_ROOT}

# 复制依赖文件
COPY deployment/requirements.txt .

# 安装系统依赖
RUN yum update -y && \
    yum install -y gcc python3-dev && \
    yum clean all

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ ./src/

# 设置Python路径
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}/src:${PYTHONPATH}"

# 设置环境变量
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO

# 设置处理器
CMD ["src.handler.lambda_handler"] 
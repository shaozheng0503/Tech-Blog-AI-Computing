#!/usr/bin/env python3
"""
用户管理API - Serverless项目安装配置
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取依赖文件
def read_requirements():
    requirements_path = os.path.join("deployment", "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    return []

setup(
    name="user-management-api-serverless",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="云主机JupyterLab开发转Serverless服务部署示例项目",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/user-management-api-serverless",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
        "Environment :: Web Environment",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "monitoring": [
            "boto3>=1.34.0",
            "psutil>=5.9.0",
            "prometheus-client>=0.17.0",
        ],
        "all": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0", 
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
            "boto3>=1.34.0",
            "psutil>=5.9.0",
            "prometheus-client>=0.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "user-api=src.app:main",
            "user-api-monitor=monitoring.performance_monitor:main",
            "user-api-test=tests.load_test:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.yml",
            "*.yaml", 
            "*.json",
            "*.txt",
            "*.md",
            "deployment/*",
            "config/*",
            "notebooks/*",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/your-username/user-management-api-serverless/issues",
        "Source": "https://github.com/your-username/user-management-api-serverless",
        "Documentation": "https://your-docs-site.com",
    },
    keywords=[
        "fastapi",
        "serverless", 
        "aws-lambda",
        "api",
        "microservices",
        "jupyter",
        "cloud",
        "python",
        "rest-api",
        "deployment",
    ],
) 

# 在共绩算力上部署并使用 CodeFormer

本指南详细阐述了在共绩算力平台上，高效部署与使用 CodeFormer 项目的技术方案。CodeFormer 通过先进的算法优化图像细节，提升清晰度，保持自然和真实的视觉效果。支持图片和视频的高清修复，操作简单，开源免费，适用于家庭相册修复、社交媒体照片优化以及专业图像处理等多种场景。

## 1. 在共绩算力上运行 CodeFormer

共绩算力平台提供预构建的 CodeFormer 容器镜像，用户无需本地复杂环境配置，可快速完成部署并启用服务。以下是详细部署步骤：

### 1.1 创建部署服务
登录共绩算力控制台，在控制台首页点击“弹性部署服务”进入管理页面。首次使用需确保账户已开通弹性部署服务权限。

![创建部署服务](placeholder.png)

### 1.2 选择 GPU 型号
根据实际需求选择 GPU 型号：
初次使用或调试阶段，推荐配置单张 NVIDIA RTX 4090 GPU。

![选择 GPU 型号](placeholder.png)

### 1.3 选择预制镜像
在“服务配置”模块切换至“预制服务”选项卡，搜索并选择 CodeFormer 官方镜像。

### 1.4 部署并访问服务
点击“部署服务”，平台将自动拉取镜像并启动容器。

![部署服务](placeholder.png)

部署完成后，在“快捷访问”中复制端口为 7860 的公网访问链接，后续是通过该地址调用服务。

![访问服务](placeholder.png)

## 2. 快速上手

### 2.1 系统使用说明

![系统使用说明](placeholder.png)

### 2.2 参考效果

![参考效果1](placeholder.png)
![参考效果2](placeholder.png)
![参考效果3](placeholder.png)

## 3. API 使用示例

您可以通过 API 调用 CodeFormer 服务进行图像修复。以下是一个 Python 示例脚本，演示了如何调用 API。

### 3.1 找到 API
拖动到页面最底部，可以看到 API 文档入口：

![API入口1](placeholder.png)
![API入口2](placeholder.png)

### 3.2 Python 调用脚本

下面的脚本 (`codeformer_api_example.py`) 展示了如何通过 `requests` 库调用 CodeFormer API。

**使用方法:**

1.  确保已安装 `requests` 库 (`pip install requests`)。
2.  修改脚本中的 `API_URL` 为您在共绩算力平台上部署的服务访问地址。
3.  修改 `input_image_path` 为您要修复的本地图片路径。
4.  运行脚本 `python codeformer_api_example.py`。
5.  修复后的图片将保存在脚本同级目录下，默认为 `restored_image.png`。

```python
import requests
import base64
import os
import mimetypes

# =============================================
# 重要提示：请替换为你的实际服务地址（云端或本地）
# =============================================
# 从您提供的信息中获取的 API 端点 URL
API_URL = "https://d07071835-codeformer070718-318-pry1oguz-7860.550c.cloud/run/predict"

def get_mime_type(filepath):
    """
    根据文件扩展名确定文件的 MIME 类型。
    """
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type if mime_type else 'application/octet-stream'

def encode_image_to_base64(filepath):
    """
    将图像文件编码为带有数据 URI 前缀的 base64 字符串。
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"图片文件未找到: {filepath}")
    
    mime_type = get_mime_type(filepath)
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    return f"data:{mime_type};base64,{encoded_string}"

def save_base64_to_image(base64_string, output_path):
    """
    解码 base64 字符串 (无论是否带有数据 URI) 并将其保存为图像文件。
    """
    # 如果存在数据 URI 前缀，则移除它
    if ',' in base64_string:
        _header, encoded_data = base64_string.split(',', 1)
    else:
        encoded_data = base64_string
        
    image_data = base64.b64decode(encoded_data)
    
    with open(output_path, "wb") as image_file:
        image_file.write(image_data)
    print(f"图像已成功保存至: {output_path}")

def main():
    """
    运行 CodeFormer API 请求的主函数。
    """
    # --- 配置区域 ---
    # 1. 【请修改】将 'path/to/your/input_image.jpg' 替换为您的输入图片路径
    input_image_path = "path/to/your/input_image.jpg"
    
    # 2. 【可修改】设置输出图片的文件名
    output_image_path = "restored_image.png"

    # 3. 【可修改】根据需要调整 API 参数
    background_enhance = True       # 是否增强背景
    face_upsample = True            # 是否对人脸进行超分辨率
    rescaling_factor = 2            # 缩放因子 (最高为 4)
    codeformer_fidelity = 0.5       # Codeformer 保真度 (0 表示更好的质量, 1 表示更好的人脸身份保留)
    # --- 配置结束 ---

    print("开始图像修复流程...")

    try:
        # 步骤 1: 将输入图像编码为 base64
        base64_image = encode_image_to_base64(input_image_path)
        print(f"成功编码图像: {input_image_path}")

        # 步骤 2: 准备 API 请求的 payload
        payload = {
            "data": [
                base64_image,
                background_enhance,
                face_upsample,
                rescaling_factor,
                codeformer_fidelity,
            ]
        }
        
        # 步骤 3: 发送 POST 请求
        print(f"正在向 CodeFormer API ({API_URL}) 发送请求...")
        response = requests.post(API_URL, json=payload, timeout=300) # 设置300秒超时
        response.raise_for_status()  # 如果请求失败 (例如 4xx 或 5xx 错误), 则会抛出异常

        print("请求成功，正在处理返回结果...")
        response_data = response.json()

        # 步骤 4: 提取并保存输出图像
        output_base64 = response_data["data"][0]
        save_base64_to_image(output_base64, output_image_path)
        
        # 可选: 打印 API 处理时长
        duration = response_data.get("duration")
        if duration:
            print(f"API 处理耗时 {duration:.2f} 秒。")

    except FileNotFoundError as e:
        print(f"错误: {e}")
        print("请确保 'input_image_path' 设置了正确的图片文件路径。")
    except requests.exceptions.RequestException as e:
        print(f"API 请求时发生错误: {e}")
    except (KeyError, IndexError) as e:
        print(f"处理 API 响应时出错，格式可能不正确: {e}")
        print("API 返回内容:", response.text if 'response' in locals() else 'N/A')
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    main()
``` 
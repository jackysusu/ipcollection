# 基于 Python 官方镜像构建镜像
FROM python:3

# 设置工作目录
WORKDIR /app

# 将项目文件复制到镜像中的工作目录
COPY app .

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 启动应用程序
CMD ["python", "./app.py"]


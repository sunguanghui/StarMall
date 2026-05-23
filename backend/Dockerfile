FROM python:3.10-slim

WORKDIR /app

# 替换 Debian 系统源为清华源 (兼容较新的 Bookworm 和旧版发行版)
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 全局配置 pip 使用清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装 gunicorn
RUN pip install gunicorn

COPY . .

# 暴露 28001 端口
EXPOSE 28001

# 启动 Flask 服务
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:28001", "app:app"]

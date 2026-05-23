# 第一阶段：Node 编译
FROM node:20-alpine AS builder
WORKDIR /app

# 替换 Alpine 系统源为清华源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

COPY package*.json ./

# 替换 npm 源为淘宝/阿里镜像并安装依赖
RUN npm config set registry https://registry.npmmirror.com && npm install

COPY . .
RUN npm run build

# 第二阶段：Nginx 部署
FROM nginx:alpine

# 同样替换 Nginx 运行环境的 Alpine 系统源（方便后续若需进容器安装调试工具）
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

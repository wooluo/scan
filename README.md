# AI驱动Web安全自动化渗透测试平台

## 项目简介
本项目是一个基于FastAPI+React的Web安全自动化渗透测试平台，集成了资产发现、端口探测、网站信息抓取、漏洞扫描等功能，支持JWT认证、API自动化测试、前端进度条展示、工具状态检测、全流程自动化、结构化结果展示、项目/任务归档，适配云端环境。

## 技术栈
- 后端：FastAPI、SQLAlchemy、MySQL/PostgreSQL、Celery（预留）、Nessus/AWVS集成
- 前端：React、Ant Design
- 工具集成：subfinder、naabu、httpx、nuclei
- 认证：JWT
- 部署：Docker、docker-compose

## 主要功能
- 资产发现（子域名收集）
- 端口探测
- 网站信息抓取（httpx）
- 漏洞扫描（nuclei、Nessus/AWVS）
- 一键全流程自动化扫描（支持进度与结构化结果）
- 项目/任务归档与管理
- 结果查询与结构化展示
- 工具状态检测
- JWT认证与权限控制
- API自动化测试脚本

## 快速开始
### 1. 克隆仓库
```bash
git clone <your-repo-url>
cd scan
```

### 2. 一键部署（推荐Docker）
确保已安装 Docker 和 docker-compose。
```bash
docker-compose up -d
```
- 默认后端监听 8000 端口，MySQL监听 3306。
- 前端开发环境可在 `frontend/` 目录下运行 `npm install && npm start`。

### 3. 初始化数据库
```bash
python3 app/models/init_db.py
```

### 4. 启动后端（如未用docker-compose）
```bash
uvicorn app.main:app --reload
```

### 5. 启动前端
```bash
cd frontend
npm install
npm start
```

## API文档
后端启动后访问：
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### 典型API
- `/auth/login`：登录获取JWT
- `/mcp/subfinder`：资产发现
- `/mcp/naabu`：端口探测
- `/mcp/httpxinfo`：网站信息抓取
- `/mcp/nuclei`：漏洞扫描
- `/mcp/workflow`：一键全流程自动化
- `/result/all`：查询所有扫描结果
- `/project/all`：查询所有项目
- `/scan/all`：查询所有任务

> 所有API需在Header中携带 `Authorization: Bearer <token>`

### 自动化测试
```bash
python3 test_api.py
```
覆盖登录、资产发现、端口探测、漏洞扫描、结果查询等典型用例。

## 目录结构
```
app/           # FastAPI后端
  api/         # 路由与API
  core/        # JWT等核心功能
  models/      # ORM模型与数据库
  services/    # 业务逻辑
frontend/      # React前端
```

## 常见问题
- **API 401未授权**：请确认已登录并在请求头携带有效JWT。
- **端口占用/数据库连接失败**：检查docker-compose服务状态，或修改端口配置。
- **工具未集成/命令行报错**：请确保subfinder、naabu、httpx、nuclei等工具已在环境中可用。
- **CORS跨域问题**：已在后端配置允许前端来源，如有特殊需求请调整CORS设置。

## 生产环境建议
- 数据库唯一索引、速率限制、Celery任务持久化、日志细化、API参数校验、异常处理、前端分页筛选等。

## 贡献与许可
欢迎PR和Issue！

MIT License

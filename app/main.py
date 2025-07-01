from fastapi import FastAPI
from app.api import scan, auth
from app.api import ai, report, mcp, mcp_service
from app.api import result
from app.api import project
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Web安全扫描平台", description="集成Nessus/AWVS的Web安全扫描平台API")

# 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://humble-space-bassoon-6qqwr5q5xgfx59x-3000.app.github.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由注册
routers = [
    (auth.router, "/auth", ["认证"]),
    (scan.router, "/scan", ["扫描"]),
    (ai.router, "/ai", ["AI决策"]),
    (report.router, "/report", ["报告导出"]),
    (mcp.router, "/mcp", ["MCP自动化渗透"]),
    (mcp_service.router, "/mcp", ["MCP服务管理"]),
    (result.router, "/result", ["结果查询"]),
    (project.router, "/project", ["项目管理"]),
]
for router, prefix, tags in routers:
    app.include_router(router, prefix=prefix, tags=tags)

@app.get("/")
def root():
    return {"msg": "Web安全扫描平台API运行中"}

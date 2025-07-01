from fastapi import APIRouter, HTTPException, Request
from app.core.jwt import create_access_token

router = APIRouter()

@router.post("/login")
async def login(request: Request):
    # 先尝试解析 x-www-form-urlencoded
    try:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
    except Exception:
        username = None
        password = None
    # 如果没有，尝试解析 JSON
    if not username or not password:
        try:
            data = await request.json()
            username = data.get("username")
            password = data.get("password")
        except Exception:
            pass
    print("收到登录请求：", username, password)
    if username == "admin" and password == "admin":
        access_token = create_access_token({"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="用户名或密码错误")

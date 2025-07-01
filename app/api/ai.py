from fastapi import APIRouter, Depends, HTTPException
from app.services.ai import classify_vulnerability, generate_poc
from app.services.task import ai_classify_task, poc_generate_task
from app.core.jwt import get_current_user

router = APIRouter()

@router.post("/classify")
def classify(request: dict, user=Depends(get_current_user)):
    http_request = request.get("http_request")
    if not http_request:
        raise HTTPException(status_code=400, detail="缺少http_request参数")
    # 支持异步任务
    # result = ai_classify_task.delay(http_request)
    # return {"task_id": result.id}
    return classify_vulnerability(http_request)

@router.post("/poc")
def generate(request: dict, user=Depends(get_current_user)):
    vuln_type = request.get("vuln_type")
    target = request.get("target")
    if not vuln_type or not target:
        raise HTTPException(status_code=400, detail="缺少参数")
    # result = poc_generate_task.delay(vuln_type, target)
    # return {"task_id": result.id}
    return {"poc": generate_poc(vuln_type, target)}

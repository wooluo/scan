from fastapi import APIRouter, Depends
from app.core.jwt import get_current_user

router = APIRouter()

@router.post("/nessus")
def nessus_scan(target: str, user=Depends(get_current_user)):
    # TODO: 调用Nessus扫描服务
    return {"msg": f"Nessus扫描已启动: {target}"}

@router.post("/awvs")
def awvs_scan(target: str, user=Depends(get_current_user)):
    # TODO: 调用AWVS扫描服务
    return {"msg": f"AWVS扫描已启动: {target}"}

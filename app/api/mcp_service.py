from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.services.mcp_service import get_services, get_service, create_service, update_service, delete_service, test_service
from app.core.jwt import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/service")
def list_services(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_services(db)

@router.post("/service")
def add_service(data: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_service(db, data)

@router.put("/service/{service_id}")
def edit_service(service_id: int, data: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = update_service(db, service_id, data)
    if not service:
        raise HTTPException(status_code=404, detail="服务不存在")
    return service

@router.delete("/service/{service_id}")
def remove_service(service_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ok = delete_service(db, service_id)
    if not ok:
        raise HTTPException(status_code=404, detail="服务不存在")
    return {"msg": "删除成功"}

@router.post("/service/{service_id}/test")
def test_service_api(service_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="服务不存在")
    return test_service(service)

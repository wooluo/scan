# MCP服务配置管理服务层
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.scan import McpService

def get_services(db: Session) -> List[McpService]:
    return db.query(McpService).all()

def get_service(db: Session, service_id: int) -> Optional[McpService]:
    return db.query(McpService).filter(McpService.id == service_id).first()

def create_service(db: Session, data: dict) -> McpService:
    service = McpService(**data)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def update_service(db: Session, service_id: int, data: dict) -> Optional[McpService]:
    service = get_service(db, service_id)
    if not service:
        return None
    for k, v in data.items():
        setattr(service, k, v)
    db.commit()
    db.refresh(service)
    return service

def delete_service(db: Session, service_id: int) -> bool:
    service = get_service(db, service_id)
    if not service:
        return False
    db.delete(service)
    db.commit()
    return True

def test_service(service: McpService) -> dict:
    # TODO: 实际测试监听端口可用性
    # 示例返回
    return {"status": "ok", "msg": f"{service.listen_ip}:{service.listen_port} 可用"}

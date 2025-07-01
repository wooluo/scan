from app.models.database import SessionLocal
from app.models.scan_project import Project, ScanTask

def query_projects():
    db = SessionLocal()
    try:
        return [dict(id=p.id, name=p.name, description=p.description, created_at=p.created_at) for p in db.query(Project).all()]
    finally:
        db.close()

def query_project_tasks(project_id):
    db = SessionLocal()
    try:
        return [dict(id=t.id, type=t.type, target=t.target, status=t.status, progress=t.progress, result_ref=t.result_ref, created_at=t.created_at) for t in db.query(ScanTask).filter_by(project_id=project_id).all()]
    finally:
        db.close()

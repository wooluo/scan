from app.models.database import SessionLocal
from app.models.scan_project import Project, ScanTask

def create_project(name, description=None):
    db = SessionLocal()
    try:
        exists = db.query(Project).filter_by(name=name).first()
        if not exists:
            proj = Project(name=name, description=description)
            db.add(proj)
            db.commit()
            return proj.id
        return exists.id
    finally:
        db.close()

def create_scan_task(project_id, type, target, status="pending", progress=0, result_ref=None):
    db = SessionLocal()
    try:
        task = ScanTask(project_id=project_id, type=type, target=target, status=status, progress=progress, result_ref=result_ref)
        db.add(task)
        db.commit()
        return task.id
    finally:
        db.close()


from fastapi import APIRouter, Depends
from app.core.jwt import get_current_user
from app.services.save_project import create_project, create_scan_task
from app.services.query_project import query_projects, query_project_tasks

router = APIRouter()

@router.post("/project")
def new_project(data: dict, user=Depends(get_current_user)):
    name = data.get("name")
    desc = data.get("description")
    if not name:
        return {"error": "项目名必填"}
    pid = create_project(name, desc)
    return {"project_id": pid}

@router.get("/projects")
def list_projects(user=Depends(get_current_user)):
    return query_projects()

@router.post("/project/task")
def new_task(data: dict, user=Depends(get_current_user)):
    pid = data.get("project_id")
    type = data.get("type")
    target = data.get("target")
    if not (pid and type and target):
        return {"error": "参数不全"}
    tid = create_scan_task(pid, type, target)
    return {"task_id": tid}

@router.get("/project/{project_id}/tasks")
def list_project_tasks(project_id: int, user=Depends(get_current_user)):
    return query_project_tasks(project_id)

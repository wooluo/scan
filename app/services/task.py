# 任务调度服务层（Celery任务）
from celery import Celery

celery_app = Celery('scanner', broker='redis://redis:6379/0')

@celery_app.task(acks_late=True, time_limit=3600, queue='ai')
def ai_classify_task(http_request):
    from app.services.ai import classify_vulnerability
    return classify_vulnerability(http_request)

@celery_app.task(acks_late=True, time_limit=3600, queue='poc')
def poc_generate_task(vuln_type, target):
    from app.services.ai import generate_poc
    return generate_poc(vuln_type, target)

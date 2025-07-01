from app.models.database import SessionLocal
from app.models.scan_result import ScanResult

def save_scan_result(domain, ip, port, title, http_status, vuln_info):
    db = SessionLocal()
    try:
        db_result = ScanResult(
            domain=domain,
            ip=ip,
            port=port,
            title=title,
            http_status=http_status,
            vuln_info=vuln_info
        )
        # 去重：同domain、ip、port只保留一条
        exists = db.query(ScanResult).filter_by(domain=domain, ip=ip, port=port).first()
        if not exists:
            db.add(db_result)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"[DB ERROR] {e}")
    finally:
        db.close()

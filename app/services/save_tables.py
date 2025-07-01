from app.models.database import SessionLocal
from app.models.scan_tables import Asset, PortScan, VulnScan
from app.models.scan_result import ScanResult

def save_asset(domain, subdomain):
    db = SessionLocal()
    try:
        # 去重：同domain、subdomain只保留一条
        exists = db.query(Asset).filter_by(domain=domain, subdomain=subdomain).first()
        if not exists:
            db_asset = Asset(domain=domain, subdomain=subdomain)
            db.add(db_asset)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"[DB ERROR] {e}")
    finally:
        db.close()

def save_port_scan(domain, ip, port, status):
    db = SessionLocal()
    try:
        exists = db.query(PortScan).filter_by(domain=domain, ip=ip, port=port).first()
        if not exists:
            db_port = PortScan(domain=domain, ip=ip, port=port, status=status)
            db.add(db_port)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"[DB ERROR] {e}")
    finally:
        db.close()

def save_vuln_scan(domain, ip, port, vuln_info):
    db = SessionLocal()
    try:
        exists = db.query(VulnScan).filter_by(domain=domain, ip=ip, port=port, vuln_info=vuln_info).first()
        if not exists:
            db_vuln = VulnScan(domain=domain, ip=ip, port=port, vuln_info=vuln_info)
            db.add(db_vuln)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"[DB ERROR] {e}")
    finally:
        db.close()

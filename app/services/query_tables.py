from app.models.database import SessionLocal
from app.models.scan_tables import Asset, PortScan, VulnScan
from app.models.scan_result import ScanResult

def query_assets(domain=None):
    db = SessionLocal()
    try:
        q = db.query(Asset)
        if domain:
            q = q.filter(Asset.domain == domain)
        return [dict(id=a.id, domain=a.domain, subdomain=a.subdomain, created_at=a.created_at) for a in q.all()]
    finally:
        db.close()

def query_port_scans(domain=None, ip=None):
    db = SessionLocal()
    try:
        q = db.query(PortScan)
        if domain:
            q = q.filter(PortScan.domain == domain)
        if ip:
            q = q.filter(PortScan.ip == ip)
        return [dict(id=p.id, domain=p.domain, ip=p.ip, port=p.port, status=p.status, created_at=p.created_at) for p in q.all()]
    finally:
        db.close()

def query_vuln_scans(domain=None, ip=None):
    db = SessionLocal()
    try:
        q = db.query(VulnScan)
        if domain:
            q = q.filter(VulnScan.domain == domain)
        if ip:
            q = q.filter(VulnScan.ip == ip)
        return [dict(id=v.id, domain=v.domain, ip=v.ip, port=v.port, vuln_info=v.vuln_info, created_at=v.created_at) for v in q.all()]
    finally:
        db.close()

def query_scan_results(domain=None, ip=None):
    db = SessionLocal()
    try:
        q = db.query(ScanResult)
        if domain:
            q = q.filter(ScanResult.domain == domain)
        if ip:
            q = q.filter(ScanResult.ip == ip)
        return [dict(id=r.id, domain=r.domain, ip=r.ip, port=r.port, title=r.title, http_status=r.http_status, vuln_info=r.vuln_info) for r in q.all()]
    finally:
        db.close()

from fastapi import APIRouter, Depends
from app.core.jwt import get_current_user
from app.services.query_tables import query_assets, query_port_scans, query_vuln_scans, query_scan_results

router = APIRouter()

@router.get("/assets")
def get_assets(domain: str = None, user=Depends(get_current_user)):
    return query_assets(domain)

@router.get("/portscans")
def get_port_scans(domain: str = None, ip: str = None, user=Depends(get_current_user)):
    return query_port_scans(domain, ip)

@router.get("/vulnscans")
def get_vuln_scans(domain: str = None, ip: str = None, user=Depends(get_current_user)):
    return query_vuln_scans(domain, ip)

@router.get("/scanresults")
def get_scan_results(domain: str = None, ip: str = None, user=Depends(get_current_user)):
    return query_scan_results(domain, ip)

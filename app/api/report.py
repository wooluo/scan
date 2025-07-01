from fastapi import APIRouter, Depends, Response, HTTPException
from app.services.report import export_pdf, export_csv
from app.core.jwt import get_current_user
from app.models.scan import VulnReport

router = APIRouter()

@router.post("/export/pdf")
def export_pdf_api(user=Depends(get_current_user)):
    # TODO: 查询当前用户可见报告
    reports = []  # VulnReport查询
    pdf_data = export_pdf(reports)
    return Response(content=pdf_data, media_type="application/pdf")

@router.post("/export/csv")
def export_csv_api(user=Depends(get_current_user)):
    reports = []
    csv_data = export_csv(reports)
    return Response(content=csv_data, media_type="text/csv")

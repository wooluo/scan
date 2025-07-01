# 报告导出服务层
from typing import List
from app.models.scan import VulnReport

def export_pdf(reports: List[VulnReport]) -> bytes:
    """导出PDF报告（Jinja2+PDF工具）"""
    # TODO: 实现Jinja2渲染+PDF生成
    return b"PDF_BINARY_DATA"

def export_csv(reports: List[VulnReport]) -> str:
    """导出CSV报告"""
    # TODO: 实现CSV导出
    return "vuln_type,ai_confidence\nSQLi,0.92\n"

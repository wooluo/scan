from sqlalchemy import Column, Integer, String, Text
from app.models.database import Base

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), index=True, nullable=False)
    ip = Column(String(64), index=True, nullable=False)
    port = Column(Integer, nullable=False)
    title = Column(String(255))
    http_status = Column(Integer)
    vuln_info = Column(Text)  # 存储漏洞信息，建议为JSON字符串或逗号分隔

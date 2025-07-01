from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.models.database import Base
from datetime import datetime

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), index=True, nullable=False)
    subdomain = Column(String(255), index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PortScan(Base):
    __tablename__ = "port_scans"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), index=True, nullable=False)
    ip = Column(String(64), index=True, nullable=False)
    port = Column(Integer, nullable=False)
    status = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)

class VulnScan(Base):
    __tablename__ = "vuln_scans"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), index=True, nullable=False)
    ip = Column(String(64), index=True, nullable=False)
    port = Column(Integer, nullable=False)
    vuln_info = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

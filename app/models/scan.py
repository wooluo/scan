from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum, LargeBinary
from sqlalchemy.sql import func
from app.models.database import Base
import enum
import uuid

class ScanTypeEnum(str, enum.Enum):
    domain = "domain"
    ip = "ip"
    vulnerability = "vulnerability"

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    target = Column(String(255), nullable=False)
    scan_type = Column(Enum(ScanTypeEnum), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class VulnerabilityResult(Base):
    __tablename__ = "vulnerability_results"
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    target = Column(String(255), nullable=False)
    vulnerability_id = Column(String(50))
    name = Column(String(255))
    description = Column(Text)
    severity = Column(String(20))
    solution = Column(Text)
    cvss_score = Column(Float)
    discovered_at = Column(DateTime, server_default=func.now())
    scanner = Column(String(20))

class VulnReport(Base):
    """团队协作与AI置信度报告表"""
    __tablename__ = "vuln_reports"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    target = Column(String(255))
    vuln_type = Column(String(50))
    ai_confidence = Column(Float)
    screenshot = Column(LargeBinary)
    assigned_to = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class KnowledgeEntry(Base):
    """知识库条目表（可对接Neo4j/ES等）"""
    __tablename__ = "knowledge_entries"
    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String(32), unique=True)
    title = Column(String(255))
    description = Column(Text)
    references = Column(Text)  # 可存储JSON字符串
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class McpService(Base):
    """MCP服务配置表"""
    __tablename__ = "mcp_services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)
    listen_ip = Column(String(64), nullable=False)
    listen_port = Column(Integer, nullable=False)
    status = Column(String(16), default="stopped")  # running/stopped/error
    description = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

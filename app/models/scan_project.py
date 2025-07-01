from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    tasks = relationship("ScanTask", back_populates="project")

class ScanTask(Base):
    __tablename__ = "scan_tasks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    type = Column(String(32))  # asset/port/vuln/workflow
    target = Column(String(255))
    status = Column(String(32), default="pending")
    progress = Column(Integer, default=0)
    result_ref = Column(String(255))  # 可存结果表主键或JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="tasks")

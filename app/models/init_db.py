from app.models.database import engine, Base
from app.models.scan_project import Project, ScanTask
from app.models.scan_tables import Asset, PortScan, VulnScan
from app.models.scan_result import ScanResult

def create_all_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all_tables()
    print("All tables created.")

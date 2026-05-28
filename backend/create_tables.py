import sys, os
backend_dir = r"C:/Users/pcl/AppData/Local/Temp/scriptmind-helper/backend"
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)
from app.database import Base, engine, create_tables
print("Creating tables...")
create_tables()
print("Done.")
from sqlalchemy import inspect
insp = inspect(engine)
tables = insp.get_table_names()
print(f"Tables: {tables}")
for t in tables:
    cols = [c['name'] for c in insp.get_columns(t)]
    print(f"  {t}: {cols}")

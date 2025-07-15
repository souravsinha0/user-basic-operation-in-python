from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL Database URL with custom port
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:sinha1998@localhost:3306/testdb?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(engine)

metadata = MetaData()
metadata.reflect(bind=engine)
    
tables = metadata.tables.keys()
    
print("List of tables:")
for table in tables:
    print(table)

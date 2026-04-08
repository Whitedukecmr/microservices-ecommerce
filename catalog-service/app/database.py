import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

MYSQL_USER = os.getenv("MYSQL_USER", "catalog_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "catalog_pass")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "catalog_db")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

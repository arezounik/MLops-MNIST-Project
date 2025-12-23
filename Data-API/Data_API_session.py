import pandas as pd
from torchvision import datasets, transforms
from urllib.parse import quote_plus
import torch
import os




#MySQL information for others

MYSQL_USER = os.getenv("MYSQL_USER", "wsl_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")   #####!!!!!!!!!! for Docker contanerization
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DB = os.getenv("MYSQL_DB", "mlops_db")



safe_password = quote_plus(MYSQL_PASSWORD)

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{safe_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

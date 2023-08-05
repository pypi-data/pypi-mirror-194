from sqlalchemy import create_engine
from .models import metadata
import os
from dotenv import load_dotenv


load_dotenv()
    
def get_engine():
    user = os.getenv('DB_USER')
    pw = os.getenv('DB_PASS')
    name = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    connstring = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{name}?charset=utf8"
    engine = create_engine(connstring, pool_size=5, pool_recycle=3600)
    return engine
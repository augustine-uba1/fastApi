from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
import time
from app.config import settings

# DEFINING THE DATABASE CONNECTION URL
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DEFINING THE DATABASE SESSION CONNECTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# USE THIS TO CONNECT USING RAW SQL
# while True:
#     try:
#         conn = psycopg.connect(host="localhost", port="5432", dbname="[databasename]",
#         user="[usermane]", password="[password]")

#         cursor = conn.cursor()
#         print("connection to database successful!!!!")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("Error:", error)
#         time.sleep(2)

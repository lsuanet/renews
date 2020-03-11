from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

DATABASE = os.getenv("PG_DATABASE")
USER = os.getenv("PG_USER")
PASSWORD = os.getenv("PG_PASSWORD")
HOST = os.getenv("PG_HOST")
PORT = int(os.getenv("PG_PORT"))

MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_PORT = int(os.getenv("MINIO_PORT"))
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

MINIO_ADDRESS = "%s:%s" % (MINIO_HOST, str(MINIO_PORT))

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (USER, PASSWORD, HOST, str(PORT), DATABASE)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from minio import Minio
from minio.error import ResponseError

DATABASE = "renews"
USER = "renews"
PASSWORD = "RA67x{hEXF9v?364&oTiQ}+%"
HOST = "localhost"
PORT = 5432

MINIO_HOST = "localhost"
MINIO_PORT = 9000
MINIO_ACCESS_KEY = "storage"
MINIO_SECRET_KEY = "k33HCiJLsYhchuTRR4!L*JHR"

MINIO_ADDRESS = "%s:%s" % (MINIO_HOST, str(MINIO_PORT))

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (USER, PASSWORD, HOST, str(PORT), DATABASE)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

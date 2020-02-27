from minio import Minio

from database import SessionLocal
from database import MINIO_ADDRESS, MINIO_ACCESS_KEY, MINIO_SECRET_KEY


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Dependency
def get_minio():
    try:
        minio = Minio(MINIO_ADDRESS,
                  access_key=MINIO_ACCESS_KEY,
                  secret_key=MINIO_SECRET_KEY,
                  secure=False)
        yield minio
    finally:
        pass
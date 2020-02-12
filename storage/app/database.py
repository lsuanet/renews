from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE = "renews"
USER = "renews"
PASSWORD = "RA67x{hEXF9v?364&oTiQ}+%"
HOST = "localhost"
PORT = "5432"

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (USER, PASSWORD, HOST, str(PORT), DATABASE)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
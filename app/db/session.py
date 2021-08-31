from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/coreyal"

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

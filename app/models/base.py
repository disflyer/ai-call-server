from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from app.core.config import settings

# 统一指定schema
metadata = MetaData(schema=settings.SCHEMA)

engine = create_engine(settings.DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=metadata) 
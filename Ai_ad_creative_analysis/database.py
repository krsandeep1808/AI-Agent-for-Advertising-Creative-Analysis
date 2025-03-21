from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./analysis.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PerformanceData(Base):
    __tablename__ = "performance_data"
    filename = Column(String, primary_key=True, index=True)
    ctr = Column(Float)
    conversion_rate = Column(Float)

Base.metadata.create_all(bind=engine)

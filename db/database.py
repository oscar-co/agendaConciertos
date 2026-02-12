from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://concerts_user:concerts_pass@localhost:5432/concerts"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

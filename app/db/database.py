from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- SQL Database (SQLite) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./loan_database.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- NoSQL Database (MongoDB) ---
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)

# Dependency to get a DB session for SQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get a MongoDB client
def get_mongo_client():
    return mongo_client
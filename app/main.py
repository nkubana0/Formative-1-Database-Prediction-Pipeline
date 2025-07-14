# app/main.py

from fastapi import FastAPI
from app.db import sql_models
from app.db.database import engine # <-- CHANGE THIS LINE
from app.routes import loan_routes

# Create all database tables based on the models
sql_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loan Prediction API",
    description="API for CRUD operations and loan prediction.",
    version="1.0.0"
)

# Include the router from loan_routes.py
app.include_router(loan_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Loan Prediction API!"}
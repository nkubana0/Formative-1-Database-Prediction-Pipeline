from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pymongo import MongoClient
import pandas as pd
import joblib

from app.crud import sql_crud, mongo_crud
from app.models import pydantic_schemas
from app.db.database import get_db, get_mongo_client

router = APIRouter()

@router.post("/applications/", response_model=pydantic_schemas.Person, tags=["Applications"])
def create_pending_application(
    application: pydantic_schemas.ApplicationCreate, 
    db: Session = Depends(get_db),
    mongo: MongoClient = Depends(get_mongo_client)
):
    """
    Receives a new loan application and creates records in both SQL and MongoDB
    with a status of 'Pending'.
    """
    try:
        # Create the record in the SQL database first to get the person/loan IDs
        person_with_loan = sql_crud.create_person_and_loan(db=db, application_data=application, predicted_status="Pending")
        
        # Get the new SQL loan_id
        new_loan_id = person_with_loan.loans[0].loan_id
        
        # Now create the document in MongoDB, passing the new loan_id for reference
        mongo_crud.create_application_document(mongo, application, "Pending", new_loan_id)
        
        return person_with_loan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/loans/{loan_id}", response_model=pydantic_schemas.Loan, tags=["Loans"])
def update_loan_status_in_both_dbs(
    loan_id: int, 
    loan_update: pydantic_schemas.LoanUpdate, 
    db: Session = Depends(get_db),
    mongo: MongoClient = Depends(get_mongo_client)
):
    """
    Updates the status of a loan in both the SQL and MongoDB databases.
    """
    # Update in SQL
    updated_sql_loan = sql_crud.update_loan_status(db=db, loan_id=loan_id, status=loan_update.loan_status)
    if updated_sql_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found in SQL database")
    
    # Update in MongoDB
    mongo_crud.update_document_status(mongo, loan_id, loan_update.loan_status)
    
    return updated_sql_loan

# You can keep your GET endpoints for checking data
@router.get("/persons/{person_id}", response_model=pydantic_schemas.Person, tags=["Persons"])
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = sql_crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person
# app/crud/sql_crud.py

from sqlalchemy.orm import Session
from app.db import sql_models
from app.models import pydantic_schemas

def get_person(db: Session, person_id: int):
    """
    Reads a single person by their ID from the SQL database.
    """
    return db.query(sql_models.Person).filter(sql_models.Person.person_id == person_id).first()

def create_person_and_loan(db: Session, application_data: pydantic_schemas.ApplicationCreate, predicted_status: str):
    """
    Creates a new person and a new loan record in the database.
    """
    # Create Person record
    person_data = {
        "age": application_data.age,
        "income": application_data.income,
        "employment_experience": application_data.employment_experience,
        "credit_score": application_data.credit_score,
        "credit_history_length": application_data.credit_history_length,
        "home_ownership_id": application_data.home_ownership_id,
        "gender_id": 1,
        "education_id": 1
    }
    db_person = sql_models.Person(**person_data)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)

    # Create Loan record
    loan_data = {
        "loan_amount": application_data.loan_amount,
        "loan_interest_rate": application_data.loan_interest_rate,
        "loan_percent_income": application_data.loan_amount / application_data.income if application_data.income > 0 else 0,
        "loan_status": predicted_status,
        "previous_loan_defaults": 0,
        "loan_intent_id": 1
    }
    db_loan = sql_models.Loan(**loan_data, person_id=db_person.person_id)
    db.add(db_loan)
    db.commit()
    db.refresh(db_person)

    return db_person

def update_loan_status(db: Session, loan_id: int, status: str):
    """
    Updates the status of an existing loan in the SQL database.
    """
    db_loan = db.query(sql_models.Loan).filter(sql_models.Loan.loan_id == loan_id).first()
    if not db_loan:
        return None
    db_loan.loan_status = status
    db.commit()
    db.refresh(db_loan)
    return db_loan
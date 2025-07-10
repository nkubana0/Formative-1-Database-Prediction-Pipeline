# app/crud/sql_crud.py

from sqlalchemy.orm import Session
from app.db import sql_models
from app.models import pydantic_schemas

# READ a single person by ID
def get_person(db: Session, person_id: int):
    return db.query(sql_models.Person).filter(sql_models.Person.person_id == person_id).first()

# READ multiple persons
def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(sql_models.Person).offset(skip).limit(limit).all()

# CREATE a new person
def create_person(db: Session, person: pydantic_schemas.PersonCreate):
    db_person = sql_models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

# UPDATE an existing person
def update_person(db: Session, person_id: int, person_update: pydantic_schemas.PersonUpdate):
    db_person = get_person(db, person_id=person_id)
    if not db_person:
        return None
    
    update_data = person_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_person, key, value)
        
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

# DELETE a person
def delete_person(db: Session, person_id: int):
    db_person = get_person(db, person_id=person_id)
    if not db_person:
        return None
    
    db.delete(db_person)
    db.commit()
    return db_person

# CREATE a loan for a specific person
def create_person_loan(db: Session, loan: pydantic_schemas.LoanCreate, person_id: int):
    db_loan = sql_models.Loan(**loan.dict(), person_id=person_id)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

# UPDATE a loan's status
def update_loan_status(db: Session, loan_id: int, status: str):
    db_loan = db.query(sql_models.Loan).filter(sql_models.Loan.loan_id == loan_id).first()
    if not db_loan:
        return None
    db_loan.loan_status = status
    db.commit()
    db.refresh(db_loan)
    return db_loan
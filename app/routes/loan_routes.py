from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import sql_crud
from app.models import pydantic_schemas
from app.db.database import SessionLocal

router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE endpoint
@router.post("/persons/", response_model=pydantic_schemas.Person)
def create_person(person: pydantic_schemas.PersonCreate, db: Session = Depends(get_db)):
    return sql_crud.create_person(db=db, person=person)

# READ endpoint for multiple persons
@router.get("/persons/", response_model=List[pydantic_schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = sql_crud.get_persons(db, skip=skip, limit=limit)
    return persons

# READ endpoint for a single person
@router.get("/persons/{person_id}", response_model=pydantic_schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = sql_crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

# UPDATE endpoint
@router.put("/persons/{person_id}", response_model=pydantic_schemas.Person)
def update_person(person_id: int, person_update: pydantic_schemas.PersonUpdate, db: Session = Depends(get_db)):
    db_person = sql_crud.update_person(db=db, person_id=person_id, person_update=person_update)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

# DELETE endpoint
@router.delete("/persons/{person_id}", response_model=pydantic_schemas.Person)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = sql_crud.delete_person(db=db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person
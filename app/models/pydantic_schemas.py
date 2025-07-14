from pydantic import BaseModel
from typing import List, Optional

# --- Loan Schemas ---
class LoanBase(BaseModel):
    loan_amount: float
    loan_interest_rate: float
    loan_status: str

# This schema can still be used internally if needed
class LoanCreate(LoanBase):
    pass

# Schema for reading a loan from the database
class Loan(LoanBase):
    loan_id: int
    person_id: int

    class Config:
        from_attributes = True

# Schema for updating a loan's status
class LoanUpdate(BaseModel):
    loan_status: str

# --- Person Schemas ---
# Schema for reading a person from the database
class Person(BaseModel):
    person_id: int
    age: int
    income: float
    home_ownership_id: int
    employment_experience: int
    credit_score: int
    credit_history_length: int
    loans: List[Loan] = [] 

    class Config:
        from_attributes = True

# Schema for updating a person (all fields are optional)
class PersonUpdate(BaseModel):
    age: Optional[int] = None
    income: Optional[float] = None
    home_ownership_id: Optional[int] = None
    employment_experience: Optional[int] = None
    credit_score: Optional[int] = None
    credit_history_length: Optional[int] = None

# --- NEW: Schema for a complete new application ---
# This is the request body for our main endpoint.
class ApplicationCreate(BaseModel):
    # Person details
    age: int
    income: float
    employment_experience: int
    credit_score: int
    credit_history_length: int
    home_ownership_id: int
    gender: str # e.g., "Male", "Female"
    education: str # e.g., "High School", "Bachelor's"

    # Loan details (status is excluded)
    loan_amount: float
    loan_interest_rate: float
    loan_intent: str # e.g., "EDUCATION", "MEDICAL"
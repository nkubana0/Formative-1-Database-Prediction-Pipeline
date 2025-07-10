from pydantic import BaseModel
from typing import List, Optional

# --- Loan Schemas ---
# Schema for creating a loan
class LoanBase(BaseModel):
    loan_amount: float
    loan_interest_rate: float
    loan_status: str

class LoanCreate(LoanBase):
    pass

# Schema for reading a loan
class Loan(LoanBase):
    loan_id: int
    person_id: int

    class Config:
        from_attributes = True

# --- Person Schemas ---
# Schema for creating a new person.
# We define the fields directly to ensure they appear correctly in the docs.
class PersonCreate(BaseModel):
    age: int
    income: float
    home_ownership_id: int
    employment_experience: int
    credit_score: int
    credit_history_length: int

# Schema for updating a person (all fields are optional)
class PersonUpdate(BaseModel):
    age: Optional[int] = None
    income: Optional[float] = None
    home_ownership_id: Optional[int] = None
    employment_experience: Optional[int] = None
    credit_score: Optional[int] = None
    credit_history_length: Optional[int] = None

# Schema for reading a person, including their loans
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

class LoanUpdate(BaseModel):
    loan_status: str
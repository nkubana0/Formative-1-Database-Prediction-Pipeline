from pydantic import BaseModel

# This is a Pydantic model (or "schema").
# It defines the data shape for reading a 'person' from the API.
# FastAPI uses this to validate types and serialize the response.
class Person(BaseModel):
    person_id: int
    age: int
    income: float
    home_ownership_id: int
    employment_experience: int
    credit_score: int
    credit_history_length: int

    # This Config class allows Pydantic to work with ORM models.
    class Config:
        orm_mode = True
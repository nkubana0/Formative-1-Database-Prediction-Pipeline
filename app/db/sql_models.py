from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# SQLAlchemy model for the 'person' table
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# SQLAlchemy model for the 'person' table
class Person(Base):
    __tablename__ = "person"

    person_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    income = Column(Float)
    home_ownership_id = Column(Integer)
    employment_experience = Column(Integer)
    credit_score = Column(Integer)
    credit_history_length = Column(Integer)
    gender_id = Column(Integer) # <-- ADD THIS LINE
    education_id = Column(Integer) # <-- AND ADD THIS LINE

    # Defines the one-to-many relationship with the 'Loan' model
    loans = relationship("Loan", back_populates="owner")

# SQLAlchemy model for the 'loan' table
# Update the Loan class to include all columns
class Loan(Base):
    __tablename__ = "loan"

    loan_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id"))
    loan_amount = Column(Float)
    loan_interest_rate = Column(Float)
    loan_status = Column(String)
    loan_percent_income = Column(Float) # <-- ADD THIS LINE
    previous_loan_defaults = Column(Integer) # <-- ADD THIS LINE
    loan_intent_id = Column(Integer) # <-- AND ADD THIS LINE

    # Defines the many-to-one relationship back to the 'Person' model
    owner = relationship("Person", back_populates="loans")
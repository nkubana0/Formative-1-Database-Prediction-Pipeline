from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# SQLAlchemy model for the 'person' table
class Person(Base):
    __tablename__ = "person"

    person_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    income = Column(Float)
    home_ownership_id = Column(Integer) # In a full app, this would be a FK
    employment_experience = Column(Integer)
    credit_score = Column(Integer)
    credit_history_length = Column(Integer)

    # Defines the one-to-many relationship with the 'Loan' model
    loans = relationship("Loan", back_populates="owner")

# SQLAlchemy model for the 'loan' table
class Loan(Base):
    __tablename__ = "loan"

    loan_id = Column(Integer, primary_key=True, index=True)
    loan_amount = Column(Float)
    loan_interest_rate = Column(Float)
    loan_status = Column(String)
    person_id = Column(Integer, ForeignKey("person.person_id"))

    # Defines the many-to-one relationship back to the 'Person' model
    owner = relationship("Person", back_populates="loans")
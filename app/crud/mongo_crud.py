from pymongo import MongoClient
from datetime import datetime
from app.models import pydantic_schemas

def create_application_document(mongo_client: MongoClient, application_data: pydantic_schemas.ApplicationCreate, predicted_status: str, sql_loan_id: int):
    """
    Formats the application data and inserts it as a new document into MongoDB.
    Now includes the SQL loan_id for future reference.
    """
    db = mongo_client['loan_prediction_db']
    collection = db['loanApplications']

    document = {
        "sql_loan_id": sql_loan_id, # Link to the SQL database record
        "personDetails": { "age": application_data.age, "gender": application_data.gender, "education": application_data.education, "income": application_data.income, "employmentExperienceYears": application_data.employment_experience, "homeOwnership": str(application_data.home_ownership_id) },
        "loanDetails": { "amount": application_data.loan_amount, "intent": application_data.loan_intent, "interestRate": application_data.loan_interest_rate, "percentIncome": application_data.loan_amount / application_data.income if application_data.income > 0 else 0 },
        "creditDetails": { "creditHistoryLengthYears": application_data.credit_history_length, "creditScore": application_data.credit_score, "previousLoanDefaults": "N" },
        "loanStatus": predicted_status,
        "ingestionTimestamp": datetime.now()
    }
    collection.insert_one(document)

def update_document_status(mongo_client: MongoClient, loan_id: int, status: str):
    """
    Finds a document by its SQL loan_id and updates its status.
    """
    db = mongo_client['loan_prediction_db']
    collection = db['loanApplications']
    collection.update_one({"sql_loan_id": loan_id}, {"$set": {"loanStatus": status}})
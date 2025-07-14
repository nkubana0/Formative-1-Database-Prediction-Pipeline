import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = 'loan_prediction_db'
COLLECTION_NAME = 'loanApplications'
CSV_FILE_PATH = 'data/Phase2.csv' 

# --- Main Script ---
def populate_mongodb_from_csv(csv_path, mongo_uri, db_name, collection_name):
    if not mongo_uri:
        print("Error: MONGO_URI not found. Make sure you have a .env file with the MONGO_URI variable.")
        return

    try:
        # 1. Load the CSV dataset
        df = pd.read_csv(csv_path)
        print(f"Successfully loaded '{csv_path}' with {len(df)} rows and {len(df.columns)} columns.")
        
        # 2. Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        
        # --- THE FIX: Clear the collection before inserting ---
        print(f"Clearing existing documents from '{collection_name}'...")
        collection.delete_many({})
        print("Collection cleared.")
        # ----------------------------------------------------

        # 3. Prepare documents for insertion
        documents = []
        for index, row in df.iterrows():
            doc = {
                "personDetails": {
                    "age": row['person_age'],
                    "gender": row['person_gender'],
                    "education": row['person_education'],
                    "income": row['person_income'],
                    "employmentExperienceYears": row['person_emp_exp'],
                    "homeOwnership": row['person_home_ownership']
                },
                "loanDetails": {
                    "amount": row['loan_amnt'],
                    "intent": row['loan_intent'],
                    "interestRate": row['loan_int_rate'],
                    "percentIncome": row['loan_percent_income']
                },
                "creditDetails": {
                    "creditHistoryLengthYears": row['cb_person_cred_hist_length'],
                    "creditScore": row['credit_score'],
                    "previousLoanDefaults": row['previous_loan_defaults_on_file']
                },
                "loanStatus": row['loan_status'],
                "ingestionTimestamp": datetime.now()
            }
            documents.append(doc)

        # 4. Insert documents into the collection
        if documents:
            result = collection.insert_many(documents)
            print(f"Successfully inserted {len(result.inserted_ids)} documents into '{collection_name}'.")
        else:
            print("No documents to insert.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_path}'. Please ensure the path is correct.")
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file '{csv_path}' is empty.")
    except KeyError as e:
        print(f"Error: Missing expected column in CSV: {e}. Please ensure column names in CSV match the script's expectations.")
        if 'df' in locals():
            print(f"Columns found in CSV: {df.columns.tolist()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == '__main__':
    print("Starting MongoDB population script...")
    populate_mongodb_from_csv(CSV_FILE_PATH, MONGO_URI, DB_NAME, COLLECTION_NAME)
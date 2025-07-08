import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import numpy as np 

# --- Configuration ---
MONGO_URI = 'mongodb://localhost:27017/' 
DB_NAME = 'loan_prediction_db'
COLLECTION_NAME = 'loanApplications'
CSV_FILE_PATH = 'Phase2.csv' 

# --- Main Script ---
def populate_mongodb_from_csv(csv_path, mongo_uri, db_name, collection_name):
    try:
        # 1. Load the CSV dataset
        # pandas will automatically use the first row as headers and detect delimiter.
        df = pd.read_csv(csv_path)

        print(f"Successfully loaded '{csv_path}' with {len(df)} rows and {len(df.columns)} columns.")
        print(f"Columns found: {df.columns.tolist()}")

        # 2. Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # 3. Prepare documents for insertion
        documents = []
        for index, row in df.iterrows():
            # Convert pandas NaN to None for MongoDB (MongoDB stores None as null).
            # Using .get() for robustness in case a column somehow gets missed,
            # though with read_csv and known headers, it should be fine.
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
                "ingestionTimestamp": datetime.now() # Add a timestamp for tracking when inserted
            }
            documents.append(doc)

        # 4. Insert documents into the collection
        if documents:
            result = collection.insert_many(documents)
            print(f"Successfully inserted {len(result.inserted_ids)} documents into '{collection_name}'.")
        else:
            print("No documents to insert.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_path}'. Please ensure '{csv_path}' is in the same directory as this script.")
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
import os
from pymongo import MongoClient
# from urllib.parse import quote_plus # No longer needed
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration (using your full MONGO_URI from .env) ---
# Direct loading of the full MONGO_URI from .env
MONGO_URI = os.getenv("MONGO_URI") # <-- This is the main change!

# You can keep CLUSTER_ID and APP_NAME as references, but they are not used for URI construction anymore
# CLUSTER_ID = "loanpredictor.jqhvfck.mongodb.net"
# APP_NAME = "LoanPredictor"

if not MONGO_URI:
    # It's good practice to provide a clear error if the essential URI is missing
    raise ValueError("MONGO_URI environment variable must be set in your .env file.")

# The MONGO_URI is now directly available from os.getenv()
# No need for encoded_username, encoded_password, or manual string formatting here

DB_NAME = 'loan_prediction_db'
COLLECTION_NAME = 'loanApplications'

# --- Connect to MongoDB ---
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping') # Test connection
    print("MongoDB connection successful!")
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    print(f"\n--- Querying the '{COLLECTION_NAME}' collection ---")

    # --- Query Examples ---

    # 1. Find All Documents (Limit to a few for display)
    print("\n1. Finding all documents (first 5):")
    # .find({}) means no filter, get all. .limit(5) restricts results.
    for doc in collection.find({}).limit(5):
        print(doc)
    print("...") # Indicate more documents exist

    # 2. Count All Documents
    print(f"\n2. Total number of documents: {collection.count_documents({})}")

    # 3. Find Documents with Specific Criteria (Equality)
    # Find all applications where loan_status is 1 (approved)
    print("\n3. Finding approved loan applications (loanStatus = 1, first 3):")
    for doc in collection.find({"loanStatus": 1}).limit(3):
        print(doc)

    # 4. Find Documents with Nested Field Criteria
    # Find applications for females (personDetails.gender = "female")
    print("\n4. Finding applications from females (first 3):")
    for doc in collection.find({"personDetails.gender": "female"}).limit(3):
        print(doc)

    # 5. Find Documents Using Comparison Operators ($gt, $lt, $gte, $lte)
    # Find applications with income > 100000 and age < 30
    print("\n5. Finding applications with income > 100000 and age < 30 (first 3):")
    for doc in collection.find({
        "personDetails.income": {"$gt": 100000},
        "personDetails.age": {"$lt": 30}
    }).limit(3):
        print(doc)

    # 6. Find Documents with "OR" Logic ($or operator)
    # Find applications with loan_intent = "education" OR "small_business"
    print("\n6. Finding applications for 'education' OR 'small_business' intent (first 3):")
    for doc in collection.find({
        "$or": [
            {"loanDetails.intent": "education"},
            {"loanDetails.intent": "small_business"}
        ]
    }).limit(3):
        print(doc)

    # 7. Projection (Selecting Specific Fields)
    # Get only loan_amount and loan_intent for approved loans
    print("\n7. Projecting 'loan_amount' and 'loan_intent' for approved loans (first 3):")
    for doc in collection.find(
        {"loanStatus": 1},
        {"loanDetails.amount": 1, "loanDetails.intent": 1, "_id": 0} # 1 to include, 0 to exclude
    ).limit(3):
        print(doc)

    # 8. Sorting Results (.sort())
    # Find applications sorted by person_age (ascending)
    print("\n8. Finding applications sorted by person_age (ascending, first 3):")
    for doc in collection.find({}).sort("personDetails.age", 1).limit(3): # 1 for ascending, -1 for descending
        print(doc)

    # 9. Combining Filters, Projections, and Sorting
    # Find applications from males with income > 50000, show only age, income, and loan_status, sorted by income descending
    print("\n9. Combined Query (Male, Income > 50000, specific fields, sorted by income DESC, first 3):")
    for doc in collection.find(
        {
            "personDetails.gender": "male",
            "personDetails.income": {"$gt": 50000}
        },
        {
            "personDetails.age": 1,
            "personDetails.income": 1,
            "loanStatus": 1,
            "_id": 0
        }
    ).sort("personDetails.income", -1).limit(3):
        print(doc)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'client' in locals() and client:
        client.close()
        print("\nMongoDB connection closed.")

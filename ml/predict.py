import requests
import pandas as pd
import joblib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
API_URL = "http://127.0.0.1:8000"
ASSETS_PATH = "ml/saved_model/pipeline_assets.joblib"
# Define the decision threshold to tune model behavior
# Raise this (e.g., 0.75) to reduce False Positives (be stricter)
# Lower this (e.g., 0.35) to reduce False Negatives (be more lenient)
DECISION_THRESHOLD = 0.75 

def api_call(method, url, json=None):
    """A helper function to handle API calls."""
    try:
        response = requests.request(method, url, json=json)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None

def main():
    """Main function to run the prediction and logging pipeline."""
    print("🚀 Starting Prediction Pipeline Script...")

    # 1. Fetch the latest person from the API
    all_persons = api_call("GET", f"{API_URL}/persons/")
    if not all_persons:
        print("Could not fetch persons. Please ensure the API is running and data exists.")
        return
    
    latest_person = all_persons[-1]
    person_id = latest_person['person_id']
    print(f"\n✅ Step 1: Fetched latest person (ID: {person_id})")

    # 2. Create a 'Pending' loan application
    loan_application = {"loan_amount": 25000.0, "loan_interest_rate": 7.5, "loan_status": "Pending"}
    created_loan = api_call("POST", f"{API_URL}/persons/{person_id}/loans/", json=loan_application)
    if not created_loan: return
    loan_id = created_loan['loan_id']
    print(f"✅ Step 2: Created a 'Pending' loan application (ID: {loan_id})")

    # 3. Prepare the data for the model
    try:
        # Load all pipeline assets: model, scaler, and training columns
        assets = joblib.load(ASSETS_PATH)
        model, scaler, training_columns = assets['model'], assets['scaler'], assets['columns']
        
        # Create a single-row DataFrame with the correct columns, initialized to 0
        input_df = pd.DataFrame(columns=training_columns, index=[0]).fillna(0)

        # Map the data from the API response to the correct columns
        input_df.loc[0, 'person_age'] = latest_person['age']
        input_df.loc[0, 'person_income'] = latest_person['income']
        input_df.loc[0, 'person_emp_exp'] = latest_person['employment_experience']
        input_df.loc[0, 'credit_score'] = latest_person['credit_score']
        input_df.loc[0, 'cb_person_cred_hist_length'] = latest_person['credit_history_length']
        
        print("\n✅ Step 3: Prepared input data for model.")
        
        # 4. Scale data and make a prediction using the new threshold
        input_scaled = scaler.transform(input_df)
        
        # Get the probability of the 'Approved' class (which is the second column)
        probability_approved = model.predict_proba(input_scaled)[0, 1]
        
        # Apply the threshold to make a decision
        result = "Approved" if probability_approved >= DECISION_THRESHOLD else "Rejected"
        
        print(f"🧠 Step 4: Model Prediction is '{result}' (Confidence: {probability_approved:.2f}, Threshold: {DECISION_THRESHOLD})")
        
        # 5. Log the prediction result back to the database via the API
        update_payload = {"loan_status": result}
        updated_loan = api_call("PUT", f"{API_URL}/loans/{loan_id}", json=update_payload)
        
        if updated_loan:
            print(f"🎉 Step 5: Success! Prediction result was logged to the database for loan ID {loan_id}.")
        else:
            print("❌ Step 5: Failed to log prediction result.")
    
    except FileNotFoundError:
        print(f"❌ Error: Pipeline assets not found at '{ASSETS_PATH}'. Please run the Jupyter Notebook to train and save the assets.")
    except Exception as e:
        print(f"❌ An error occurred during the pipeline: {e}")

if __name__ == "__main__":
    main()
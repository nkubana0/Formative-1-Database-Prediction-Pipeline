import requests
import joblib
import pandas as pd

# --- Configuration ---
API_URL = "http://127.0.0.1:8000"
MODEL_PATH = "ml/saved_model/loan_predictor.joblib"

def api_call(method, url, json=None):
    """Handles API calls and returns the JSON response."""
    try:
        response = requests.request(method, url, json=json)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None

def main():
    """Main function to run the full prediction and logging pipeline."""
    print("🚀 Starting prediction script...")
    
    # 1. Fetch the latest person
    persons_data = api_call("GET", f"{API_URL}/persons/")
    if not persons_data:
        print("Could not fetch persons. Exiting.")
        return
        
    latest_person = persons_data[-1]
    person_id = latest_person['person_id']
    print(f"✅ Fetched latest person (ID: {person_id})")

    # 2. Create a 'Pending' loan application for this person
    loan_application = {
        "loan_amount": 15000.0,
        "loan_interest_rate": 12.5,
        "loan_status": "Pending"
    }
    created_loan = api_call("POST", f"{API_URL}/persons/{person_id}/loans/", json=loan_application)
    if not created_loan:
        print("Could not create loan application. Exiting.")
        return
        
    loan_id = created_loan['loan_id']
    print(f"✅ Created a 'Pending' loan application (ID: {loan_id})")

    # 3. Prepare data for the model
    features = {
        'age': [latest_person['age']],
        'income': [latest_person['income']],
        'employment_experience': [latest_person['employment_experience']],
        'credit_score': [latest_person['credit_score']]
    }
    input_df = pd.DataFrame(features)
    
    # 4. Load model and make prediction
    try:
        model = joblib.load(MODEL_PATH)
        prediction = model.predict(input_df)[0]
        result = "Approved" if prediction == 1 else "Rejected"
        print(f"🧠 Model Prediction: {result}")
        
        # 5. Log the prediction result back to the database
        update_payload = {"loan_status": result}
        updated_loan = api_call("PUT", f"{API_URL}/loans/{loan_id}", json=update_payload)
        
        if updated_loan:
            print(f"🎉 Success! Prediction result '{result}' was logged back to the database for loan ID {loan_id}.")
        else:
            print("❌ Failed to log prediction result back to the database.")

    except FileNotFoundError:
        print(f"❌ Error: Model file not found at {MODEL_PATH}")
    except Exception as e:
        print(f"❌ An error occurred during prediction: {e}")

if __name__ == "__main__":
    main()
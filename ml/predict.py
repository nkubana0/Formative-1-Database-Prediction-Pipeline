import requests
import pandas as pd
import joblib

API_URL = "http://127.0.0.1:8000"
ASSETS_PATH = "ml/saved_model/pipeline_assets.joblib"

def get_person_and_loan(person_id, loan_id):
    """Fetches the full person object from the API and checks the loan status."""
    try:
        response = requests.get(f"{API_URL}/persons/{person_id}")
        response.raise_for_status()
        person_data = response.json()
        
        # Find the specific loan from the person's loan list
        for loan in person_data.get('loans', []):
            if loan['loan_id'] == loan_id:
                # --- THIS IS THE NEW VALIDATION STEP ---
                if loan['loan_status'] == 'Pending':
                    return person_data, loan
                else:
                    print(f"❌ Error: Loan {loan_id} has a status of '{loan['loan_status']}' and cannot be updated.")
                    return None, None
        
        print(f"❌ Error: Loan with ID {loan_id} not found for person {person_id}.")
        return None, None

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None, None

def main():
    print("🚀 Starting Loan Prediction Script...")
    try:
        person_id = int(input("Enter the Person ID to predict for: "))
        loan_id = int(input(f"Enter the Loan ID for person {person_id}: "))
    except ValueError:
        print("❌ Invalid ID. Please enter numbers.")
        return

    # 1. Fetch data for the specified person and loan (includes status check)
    person, loan = get_person_and_loan(person_id, loan_id)
    if not person: 
        return

    # 2. Prepare data for prediction
    try:
        assets = joblib.load(ASSETS_PATH)
        model, scaler, training_columns = assets['model'], assets['scaler'], assets['columns']
        input_df = pd.DataFrame(columns=training_columns, index=[0]).fillna(0)

        # Map person and loan data
        input_df.loc[0, 'person_age'] = person['age']
        input_df.loc[0, 'person_income'] = person['income']
        # ... (add all other feature mappings here, similar to the notebook) ...
        input_df.loc[0, 'loan_amnt'] = loan['loan_amount']
        input_df.loc[0, 'loan_int_rate'] = loan['loan_interest_rate']
        
        # 3. Make prediction
        input_scaled = scaler.transform(input_df[training_columns])
        prediction = model.predict(input_scaled)[0]
        result = "Approved" if prediction == 1 else "Rejected"
        print(f"🧠 Model Prediction: {result}")

        # 4. Update the loan status in both databases via the API
        response = requests.put(f"{API_URL}/loans/{loan_id}", json={"loan_status": result})
        if response.status_code == 200:
            print(f"\n🎉 Success! Loan {loan_id} status updated to '{result}' in both databases.")
        else:
            print(f"\n❌ Failed to update loan status. API response: {response.text}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
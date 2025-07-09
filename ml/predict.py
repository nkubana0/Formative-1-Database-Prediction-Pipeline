import requests
import joblib
import pandas as pd

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/persons/"
MODEL_PATH = "ml/saved_model/loan_predictor.joblib"

def fetch_latest_person(url: str):
    """Fetches the list of persons and returns the latest one."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        all_persons = response.json()
        if not all_persons:
            print("❌ No persons found in the database.")
            return None
        # Return the last person in the list (most recently added)
        return all_persons[-1]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from API: {e}")
        return None

def main():
    """Main function to run the prediction process."""
    print("🚀 Starting prediction script...")
    
    # 1. Fetch the latest entry from the API
    latest_person = fetch_latest_person(API_URL)
    
    if latest_person:
        print(f"✅ Successfully fetched latest person (ID: {latest_person['person_id']})")
        
        # 2. Prepare data for prediction
        # The model was trained on: age, income, employment_experience, credit_score
        # We need to create a DataFrame in the same order.
        features = {
            'age': [latest_person['age']],
            'income': [latest_person['income']],
            'employment_experience': [latest_person['employment_experience']],
            'credit_score': [latest_person['credit_score']]
        }
        input_df = pd.DataFrame(features)
        print("\nData prepared for model:")
        print(input_df)
        
        # 3. Load the pre-trained model
        try:
            model = joblib.load(MODEL_PATH)
            print(f"\n✅ Model loaded from {MODEL_PATH}")
            
            # 4. Make a prediction
            prediction = model.predict(input_df)
            prediction_proba = model.predict_proba(input_df)
            
            result = "Approved" if prediction[0] == 1 else "Rejected"
            confidence = prediction_proba[0][prediction[0]] * 100
            
            print(f"\n🎉 Prediction Result: The loan is **{result}** with {confidence:.2f}% confidence.")
            
        except FileNotFoundError:
            print(f"❌ Error: Model file not found at {MODEL_PATH}")
        except Exception as e:
            print(f"❌ An error occurred during prediction: {e}")

if __name__ == "__main__":
    main()
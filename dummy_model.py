import joblib
from sklearn.linear_model import LogisticRegression
import numpy as np

# Create simple placeholder data
# Features: age, income, employment_experience, credit_score
X_train = np.array([
    [25, 50000, 2, 650],
    [45, 120000, 20, 780],
    [22, 35000, 1, 600],
    [50, 95000, 15, 720]
])
# Target: 0 (Rejected), 1 (Approved)
y_train = np.array([0, 1, 0, 1])

# Create and "train" a simple logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the trained model to the correct folder
model_path = 'ml/saved_model/loan_predictor.joblib'
joblib.dump(model, model_path)

print(f"✅ Dummy model saved to {model_path}")
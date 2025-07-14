# Loan Prediction Pipeline

This project is a machine learning pipeline that integrates both relational and NoSQL databases, a FastAPI backend, and a trained machine learning model to predict loan approvals based on borrower profiles.

---


## 🚀 Features

- 🔗 Dual database support: SQLite (SQL) + MongoDB Atlas (NoSQL)
- 🧠 Logistic Regression model for loan approval prediction
- 📊 RESTful API built with FastAPI (CRUD operations for Person + Loan)
- 🔄 Realtime prediction via Python script or Jupyter notebook
- ✨ Automatic update of prediction results to both databases

---

## 🛠 Tech Stack

- **Backend**: FastAPI, SQLite, MongoDB (pymongo)
- **ML**: scikit-learn, joblib, pandas
- **Dev Tools**: Uvicorn, Jupyter Notebook

---

## 🧪 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Formative-1-Database-Prediction-Pipeline.git
cd Formative-1-Database-Prediction-Pipeline
```

## 2. Set Up a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate    # Windows
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt

```

## 4. Start the API Server

```bash
uvicorn app.main:app --reload
```

Open your browser and visit:
http://127.0.0.1:8000/docs

## 5. Run Predictions
### Option A: Script
```bash
python ml/predict.py
```
Enter the person_id and loan_id when prompted.

### Option B: Notebook
Open and run ml/predict.ipynb step-by-step:

- Enter person_id and loan_id

- Fetch data via API

- Predict with trained model

- Automatically update loan status



import pandas as pd
import numpy as np
import random
from sklearn.ensemble import IsolationForest, RandomForestClassifier
import xgboost as xgb
import joblib
import os

os.makedirs("app/models", exist_ok=True)

def generate_synthetic_data(n_samples=1000):
    print("Generating synthetic banking data...")
    data = []
    
    for _ in range(n_samples):
        is_risky = np.random.choice([0, 1], p=[0.8, 0.2])
        
        if is_risky == 0:
            income = np.random.normal(50000, 5000)
            spend = np.random.normal(30000, 2000)
            balance_min = np.random.normal(5000, 1000)
            overdrafts = 0
            gambling_txns = 0
        else:
            income = np.random.normal(40000, 10000)
            spend = np.random.normal(45000, 5000) # Living on edge
            balance_min = np.random.normal(-500, 2000)
            overdrafts = np.random.randint(1, 10)
            gambling_txns = np.random.randint(0, 5)

        data.append({
            "avg_monthly_income": income,
            "avg_monthly_spend": spend,
            "min_balance": balance_min,
            "overdraft_count": overdrafts,
            "gambling_flag_count": gambling_txns,
            "debt_to_income": spend / (income + 1), # +1 avoid div by 0
            "target_default": is_risky 
        })
        
    return pd.DataFrame(data)

def train_and_save_models():
    df = generate_synthetic_data()
    
    # --- 1. Train Risk Model (Supervised) ---
    X = df.drop(columns=["target_default"])
    y = df["target_default"]
    
    print("Training XGBoost Risk Model...")
    risk_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    risk_model.fit(X, y)
    joblib.dump(risk_model, "app/models/risk_model.pkl")
    
    # --- 2. Train Fraud/Anomaly Model (Unsupervised) ---
    print("Training Isolation Forest for Anomalies...")
    fraud_model = IsolationForest(contamination=0.1, random_state=42)
    fraud_model.fit(X)
    joblib.dump(fraud_model, "app/models/fraud_model.pkl")
    
    # --- 3. Train Transaction Classifier (Simple Text) ---
    # Dummy logic just to save a file, in real life use TF-IDF
    print("Saving dummy transaction classifier...")
    dummy_classifier = {"MCDONALDS": "Food", "UBER": "Transport", "SALARY": "Income", "EMI": "Loan"}
    joblib.dump(dummy_classifier, "app/models/txn_classifier.pkl")

    print("✅ All models trained and saved in app/models/")

if __name__ == "__main__":
    train_and_save_models()

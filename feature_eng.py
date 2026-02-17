import pandas as pd
import numpy as np

class FeatureEngineer:
    def extract_features(self, df):
        if df.empty:
            return None

        # Ensure correct types
        df['amount'] = pd.to_numeric(df['amount'])
        df['balance'] = pd.to_numeric(df['balance'])
        
        # 1. Income Metrics
        credits = df[df['type'] == 'credit']
        # FORCE PYTHON FLOAT
        avg_income = float(credits['amount'].mean()) if not credits.empty else 0.0
        
        # 2. Expense Metrics
        debits = df[df['type'] == 'debit']
        # FORCE PYTHON FLOAT
        avg_spend = float(debits['amount'].mean()) if not debits.empty else 0.0
        
        # 3. Risk Metrics
        # FORCE PYTHON FLOAT
        min_balance = float(df['balance'].min())
        # FORCE PYTHON INT
        overdraft_count = int(len(df[df['balance'] < 0]))
        
        # 4. Keyword Flags
        gambling_keywords = ["BET365", "DREAM11", "CASINO"]
        # .sum() returns numpy.int64, so we must cast to int()
        gambling_count = int(df['description'].apply(lambda x: 1 if any(k in x.upper() for k in gambling_keywords) else 0).sum())
        
        # 5. Debt Ratio
        debt_to_income = float(avg_spend / avg_income) if avg_income > 0 else 0.0

        # Feature Vector
        features = {
            "avg_monthly_income": avg_income,
            "avg_monthly_spend": avg_spend,
            "min_balance": min_balance,
            "overdraft_count": overdraft_count,
            "gambling_flag_count": gambling_count,
            "debt_to_income": debt_to_income
        }
        
        return features
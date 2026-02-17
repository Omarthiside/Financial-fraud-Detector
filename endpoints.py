from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.preprocessor import DocumentPreprocessor
from app.core.ocr_engine import OCREngine
from app.core.feature_eng import FeatureEngineer
import joblib
import pandas as pd
import os
import traceback

router = APIRouter()

preprocessor = DocumentPreprocessor()
ocr = OCREngine()
feat_eng = FeatureEngineer()

MODEL_PATH = "app/models/"
try:
    risk_model = joblib.load(os.path.join(MODEL_PATH, "risk_model.pkl"))
    fraud_model = joblib.load(os.path.join(MODEL_PATH, "fraud_model.pkl"))
except Exception as e:
    print(f"⚠️ Models not loaded: {e}")
    risk_model = None

@router.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        file_bytes = await file.read()

        processed_images = preprocessor.preprocess(file_bytes)
        if not processed_images:
            return {"error": "Preprocessing failed. Check Poppler installation or PDF validity."}

        raw_text = ocr.extract_text(processed_images)
        df = ocr.parse_to_dataframe(raw_text)
        
        if df.empty:
            return {"message": "OCR finished but found no transactions.", "raw_text_preview": raw_text[:500]}

        features = feat_eng.extract_features(df)
        
        if risk_model:
            input_vector = pd.DataFrame([features])
            risk_prob = float(risk_model.predict_proba(input_vector)[:, 1][0])
            anomaly_score = int(fraud_model.predict(input_vector)[0]) 
            recommendation = "APPROVE" if risk_prob < 0.4 else "REJECT"
        else:
            risk_prob = -1
            recommendation = "Models not loaded"

        return {
            "filename": file.filename,
            "transaction_count": len(df),
            "financial_profile": features,
            "risk_assessment": {
                "default_probability": round(risk_prob, 2),
                "recommendation": recommendation
            },
            "extracted_data": df.head(5).to_dict(orient="records")
        }

    except Exception as e:
        error_msg = traceback.format_exc()
        print(error_msg)
        return {
            "CRITICAL_ERROR": str(e),
            "Traceback": error_msg.split("\n")[-3:] 
        }
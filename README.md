# 🏦 Financial Document Intelligence API

> **Automated Underwriting & Fraud Detection System**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688.svg)](https://fastapi.tiangolo.com/)
[![ML](https://img.shields.io/badge/Model-XGBoost-orange.svg)](https://xgboost.readthedocs.io/)
[![OCR](https://img.shields.io/badge/OCR-Tesseract-green.svg)](https://github.com/tesseract-ocr/tesseract)

## 📖 Overview

This project is an AI-powered API designed to automate the analysis of bank statement PDFs. It streamlines the underwriting process by extracting transaction data, calculating financial health metrics, and predicting credit risk using Machine Learning.

The system performs the following pipeline:
1.  **Ingest:** Accepts raw PDF bank statements.
2.  **Preprocess:** Converts PDF to high-quality images (OpenCV).
3.  **OCR:** Extracts text using Tesseract 4.0+.
4.  **Parse:** Structured data extraction (Dates, Descriptions, Credits, Debits).
5.  **Feature Engineering:** Calculates income, spending patterns, gambling flags, and overdraft history.
6.  **Predict:** Returns a Risk Score (XGBoost) and Anomaly Detection (Isolation Forest).

---

## 🚀 Key Features

* **📄 PDF-to-Image Conversion:** High-resolution rendering using `pdf2image` and `Poppler`.
* **👁️ Optical Character Recognition:** Custom logic built on `pytesseract` to handle tabular bank data.
* **🧠 Machine Learning Models:**
    * **Risk Model:** Supervised XGBoost classifier to predict default probability.
    * **Fraud Model:** Unsupervised Isolation Forest to detect anomalous transaction patterns.
* **🚩 Red Flag Detection:** Automatically flags gambling keywords (e.g., "Dream11", "Bet365") and overdrafts.
* **⚡ FastAPI Backend:** High-performance, asynchronous REST API.
* **🧪 Synthetic Data Engine:** Includes a script to generate training data and retrain models from scratch.

---

## 📂 Project Structure

```bash
Financial-Document-Intelligence/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py       # API Routes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── feature_eng.py     # Logic for financial metrics
│   │   ├── ocr_engine.py      # Tesseract wrapper & parsing
│   │   └── preprocessor.py    # OpenCV image processing
│   ├── models/                # Saved .pkl models (Generated script)
│   └── main.py                # FastAPI entry point
├── create_pdf.py              # Utility to generate dummy PDFs
├── generate_data.py           # ML Training Script
├── requirements.txt           # Python dependencies
└── README.md

Gemini said
Here is a professional, clean, and comprehensive README.md for your GitHub repository. It covers installation, usage, architecture, and configuration details.

You can copy and paste the code block below directly into your README.md file.
```

🛠️ Installation & Setup
1. System Dependencies (Crucial)
This project requires Tesseract OCR and Poppler installed on your system.

MacOS (Homebrew):

```Bash
brew install tesseract
brew install poppler
Windows:

Download and install Tesseract-OCR. Add it to your System PATH.

Download Poppler and add bin/ to your PATH.

Linux (Ubuntu/Debian):

Bash
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
2. Python Setup
Clone the repository and install dependencies:

Bash
git clone [https://github.com/yourusername/financial-doc-intelligence.git](https://github.com/yourusername/financial-doc-intelligence.git)
cd financial-doc-intelligence

# Create virtual environment (Optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install libraries
pip install -r requirements.txt
⚙️ Configuration (Important)
If you are running this on Windows or Linux, you may need to update the binary paths in the code.

Open app/core/ocr_engine.py:

Python
# Change this line if Tesseract is not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # Example for Linux
Open app/core/preprocessor.py:

Python
# Update Poppler path if necessary
poppler_path = r"/usr/bin" 
🏃‍♂️ Usage
1. Train the Models
Before starting the API, generate synthetic data and train the ML models. This will create the .pkl files in app/models/.

Bash
python generate_data.py
Output: ✅ All models trained and saved in app/models/

2. Start the Server
Run the FastAPI server using Uvicorn:

Bash
python main.py
Server runs at: https://www.google.com/search?q=http://0.0.0.0:8000

3. Generate a Test PDF
Create a sample bank statement to test the OCR:

Bash
python create_pdf.py
4. Test the API
You can use Postman, cURL, or the built-in Swagger UI.

Option A: Swagger UI

Go to http://localhost:8000/docs.

Click on /api/v1/analyze.

Upload dummy_bank_statement1.pdf.

Execute.

Option B: cURL

Bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@dummy_bank_statement1.pdf;type=application/pdf'
📊 Sample Response
JSON
{
  "filename": "dummy_bank_statement1.pdf",
  "transaction_count": 10,
  "financial_profile": {
    "avg_monthly_income": 45000.0,
    "avg_monthly_spend": 14949.0,
    "min_balance": 48051.0,
    "overdraft_count": 0,
    "gambling_flag_count": 1,
    "debt_to_income": 0.33
  },
  "risk_assessment": {
    "default_probability": 0.12,
    "recommendation": "APPROVE"
  }
}
🤝 Contributing
Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes.

Push to the branch.

Open a Pull Request.
```
📄 License
This project is licensed under the MIT License.

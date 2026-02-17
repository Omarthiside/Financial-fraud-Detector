import pytesseract
import pandas as pd
import re
import shutil

# --- FORCE TESSERACT PATH FOR M1 MAC ---
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

class OCREngine:
    def extract_text(self, images):
        full_text = ""
        # PSM 6 assumes a single uniform block of text
        custom_config = r'--oem 3 --psm 6' 
        for img in images:
            try:
                text = pytesseract.image_to_string(img, config=custom_config)
                full_text += text + "\n"
            except Exception as e:
                print(f"⚠️ OCR Error: {e}")
        return full_text

    def parse_to_dataframe(self, raw_text):
        lines = raw_text.split('\n')
        data = []
        
        # Regex for Date (DD/MM/YYYY)
        date_pattern = r'\d{2}/\d{2}/\d{4}'
        # Regex for Money (e.g. 1,000.00 or 500.00)
        amount_pattern = r'(\d{1,3}(?:,\d{3})*|\d+)(\.\d{2})?'

        for line in lines:
            if not line.strip(): continue
            
            # 1. Find the Date
            match = re.search(date_pattern, line)
            if not match: continue
            date = match.group(0)
            
            # 2. CRITICAL FIX: Remove the date from the line so we don't count it as money
            line_no_date = line.replace(date, "")
            
            # 3. Find all money numbers in the remaining text
            amounts = [float(x[0].replace(',', '')) for x in re.findall(amount_pattern, line_no_date)]
            
            # Filter out tiny numbers that might be noise (optional)
            amounts = [a for a in amounts if a > 0]

            if not amounts: continue

            # Logic: 
            # If 2 numbers found -> First is Txn Amount, Second is Balance
            # If 1 number found -> It's probably the Balance (skip) or Amount
            
            if len(amounts) >= 2:
                balance = amounts[-1]
                amount = amounts[0]
            elif len(amounts) == 1:
                amount = amounts[0]
                balance = 0.0 # Unknown
            else:
                continue

            # Description is whatever is left after removing numbers
            description = re.sub(amount_pattern, "", line_no_date).strip()
            # Clean up extra symbols
            description = description.replace("|", "").replace("[", "").strip()

            # Determine Type
            txn_type = "credit" if any(x in line for x in ["Cr", "Deposit", "Credit", "TRF FROM", "SALARY"]) else "debit"

            data.append({
                "date": date,
                "description": description,
                "amount": amount,
                "type": txn_type,
                "balance": balance
            })

        return pd.DataFrame(data)
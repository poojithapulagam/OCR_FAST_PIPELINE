import ollama
import json

class LLMExtractor:

    def __init__(self, model="qwen2.5"):
        self.model = model

    def extract_name_address_pairs(self, text):

        prompt = f"""
You are an advanced OCR cleanup and information extraction model. 
Your ONLY task is to extract the HUMAN RECIPIENT’S NAME and FULL DELIVERY ADDRESS 
from noisy, unstructured shipping label text.

The input text may contain:
- Tracking numbers
- Company names (e.g., USPS, FedEx, UPS, Amazon, Notifii)
- Sender information
- Marketing text
- Barcode artifacts
- Weight, shipping class, timestamps
- Random broken OCR characters

RULES:
1. Extract ONLY the final delivery recipient's NAME.
2. Extract ONLY ONE complete postal ADDRESS, including:
   - Street number
   - Street name
   - Apartment/Suite (if present)
   - City
   - State
   - ZIP code (5 or 9 digits)
3. Ignore:
   - Company names
   - “Ship To”, “From”, “Sender”
   - Tracking numbers
   - Shipping class (priority, ground, express)
   - Barcode values
4. The name must be a person, NOT a company.
5. The address must be the FULL delivery address.
6. Output MUST be valid JSON only. No explanation, no extra text.

JSON OUTPUT FORMAT:
[
  {{
    "input_name": "<recipient name>",
    "input_address": "<cleaned full address>"
  }}
]

Now extract the information from this OCR text:

{text}
"""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt
            )
            return json.loads(response["response"])
        except Exception as e:
            print("LLM Extractor Error:", e)
            return []













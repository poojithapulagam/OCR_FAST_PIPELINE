import pandas as pd
from src.extractors.fast_extractor import FastExtractor
from src.utils.fuzzy_matcher import FuzzyMatcher

class OCRPipeline:

    def __init__(self, input_file="data/ocr_test_data.csv"):
        self.input_file = input_file
        self.extractor = FastExtractor()
        self.matcher = FuzzyMatcher()

    def run(self):
        df = pd.read_csv(self.input_file)

        results = []

        for i, row in df.iterrows():
            raw_text = row["ocr_text"]

            print("\n==============================")
            print(f"🔍 Processing Record {i+1}")
            print("==============================")

            try:
                # -------------------------
                # 1️⃣ Extract Name & Address
                # -------------------------
                extracted_name = self.extractor.extract_name(raw_text)
                extracted_address = self.extractor.extract_address(raw_text)

                print(f"Extracted Name: {extracted_name}")
                print(f"Extracted Address: {extracted_address}")

                # -------------------------
                # 2️⃣ Match with DB
                # -------------------------
                match = self.matcher.match(extracted_name, extracted_address)

                if match:
                    print("\n🎉 MATCH FOUND:")
                    print(f"Recipient ID: {match['recipient_id']}")
                    print(f"Full Name  : {match['preferred_full_name']}")
                    print(f"Address    : {match['address']}")
                else:
                    print("\n❌ No matching record found.")

                # -------------------------
                # 3️⃣ Store result
                # -------------------------
                results.append({
                    "raw_text": raw_text,
                    "name": extracted_name,
                    "address": extracted_address,
                    "match": match
                })

            except Exception as e:
                # -------------------------
                # 4️⃣ Error-safe: Continue pipeline
                # -------------------------
                print("\n⚠️ ERROR PROCESSING RECORD:", e)

                results.append({
                    "raw_text": raw_text,
                    "name": None,
                    "address": None,
                    "match": None,
                    "error": str(e)
                })

                continue  # continue processing remaining rows

        return results

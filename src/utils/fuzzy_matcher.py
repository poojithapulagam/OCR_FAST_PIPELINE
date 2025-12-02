import json
from rapidfuzz import fuzz

class FuzzyMatcher:

    def __init__(self, db_path="data/recipient_db.json"):
        with open(db_path, "r", encoding="utf-8") as f:
            self.db = json.load(f)["recipients"]

    def match(self, extracted_name, extracted_address):
        if not extracted_name and not extracted_address:
            return None

        best_record = None
        best_score = 0

        for r in self.db:
            full_name = f"{r['first_name']} {r['last_name']}"
            address = r["address"]

            name_score = fuzz.token_set_ratio(extracted_name.lower(), full_name.lower()) if extracted_name else 0
            addr_score = fuzz.token_set_ratio(extracted_address.lower(), address.lower()) if extracted_address else 0

            final_score = (name_score * 0.7) + (addr_score * 0.3)

            if final_score > best_score:
                best_score = final_score
                best_record = r

        if best_score < 60:  # threshold
            return None

        return best_record

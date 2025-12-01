from difflib import SequenceMatcher

class RecipientMatcher:

    def __init__(self, db_file):
        import json
        with open(db_file, "r") as f:
            self.db = json.load(f)["recipients"]

    def match_pair(self, name, address):
        best = None
        best_score = 0

        for r in self.db:
            db_name = f"{r['first_name']} {r['last_name']}"
            db_address = r['address']

            name_score = SequenceMatcher(None, name.lower(), db_name.lower()).ratio()
            addr_score = SequenceMatcher(None, address.lower(), db_address.lower()).ratio()

            score = (name_score * 0.7) + (addr_score * 0.3)

            if score > best_score:
                best_score = score
                best = r

        if best_score >= 0.50:
            return [best]
        return []

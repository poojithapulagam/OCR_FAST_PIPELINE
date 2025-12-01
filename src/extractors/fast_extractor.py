import re
import spacy
from difflib import SequenceMatcher

nlp = spacy.load("en_core_web_sm")

class FastExtractor:
    """Fast name+address extractor with LLM fallback."""

    def __init__(self, llm_extractor=None):
        self.llm = llm_extractor

    def extract_person(self, text):
        doc = nlp(text)

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text

        words = text.split()
        skip = {"street", "main", "roseville", "usa", "fat1"}

        candidates = []
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i+1]
            if w1.isalpha() and w2.isalpha():
                if w1.lower() not in skip and w2.lower() not in skip:
                    candidates.append(f"{w1} {w2}")

        if candidates:
            return candidates[-1]

        if self.llm:
            pairs = self.llm.extract_name_address_pairs(text)
            if pairs:
                return pairs[0]["input_name"]

        return None

    def extract_address(self, text):
        pattern = r"\d{2,5}\s+[A-Za-z0-9\s]+?(?:dr|st|road|ave|blvd|ln|way|street)\b.*?(?:\d{5}(?:-\d{4})?)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

        if self.llm:
            pairs = self.llm.extract_name_address_pairs(text)
            if pairs:
                return pairs[0]["input_address"]

        return None

    def similarity(self, a, b):
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

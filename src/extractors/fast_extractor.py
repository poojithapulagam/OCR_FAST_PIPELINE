import spacy
import re

# Load spaCy NER
nlp = spacy.load("en_core_web_sm")

class FastExtractor:

    def extract_name(self, text):
        """Extract person name using spaCy + fallback rules."""

        doc = nlp(text)

        # 1️⃣ spaCy PERSON entity
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()

        # 2️⃣ Fallback rule - find two consecutive words
        fallback = re.findall(r"[A-Za-z]+\s+[A-Za-z]+", text)

        return fallback[-1].strip() if fallback else None

    def extract_address(self, text):
        """Extract address using regex pattern."""

        pattern = (
            r"\d{2,5}\s+[A-Za-z0-9\s]+?"
            r"(?:dr|st|road|ave|blvd|suite|ste|street|pkwy|trail|drive|ln|lane)\b"
            r".*?(?:\d{5}(?:-\d{4})?)"
        )

        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(0).strip() if match else None

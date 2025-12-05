# src/extractors/fast_extractor.py

import spacy
import re

nlp = spacy.load("en_core_web_sm")

class FastExtractor:

    def __init__(self):
        self.skip_words = {
            "priority", "mail", "ground", "tracking", "ship", "shipment",
            "ups", "usps", "fedex", "notifi", "notifii", "llc", "corporation",
            "street", "st", "ave", "blvd", "suite", "ste", "road", "rd",
            "pkwy", "drive", "ln", "lane", "trail", "p", "signature",
            "world", "church", "victory", "financial", "fees", "postage",
            "roseville", "cleveland", "ca", "oh", "usa"
        }

    # ----------------------------------------------------------
    # NAME EXTRACTION
    # ----------------------------------------------------------
    def extract_name(self, text):
        lines = [l.strip() for l in re.split(r"[,\n]+", text) if l.strip()]
        human_names = []

        for line in lines:
            low = line.lower()

            if re.search(r"\d", low):
                continue
            if any(w in low for w in self.skip_words):
                continue
            if not re.search(r"[a-zA-Z]{2,}", low):
                continue
            if 1 <= len(low.split()) <= 3:
                human_names.append(line)

        # Return last candidate if 2+ appear
        if len(human_names) >= 2:
            return human_names[-1].strip()

        # Single early-line names are suspicious → discard
        if len(human_names) == 1 and lines.index(human_names[0]) < 3:
            return None

        # SpaCy fallback
        doc = nlp(text)
        persons = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
        if persons:
            return persons[-1]

        # Bigram fallback
        bigrams = re.findall(r"[A-Za-z]+ [A-Za-z]+", text)
        for bg in reversed(bigrams):
            low = bg.lower()
            if not re.search(r"\d", low) and not any(w in low for w in self.skip_words):
                return bg.strip()

        return None

    # ----------------------------------------------------------
    # ADDRESS EXTRACTION  (← FIXED INDENTATION)
    # ----------------------------------------------------------
    def extract_address(self, text):
        # Strict US address pattern
        pattern = (
            r"\d{2,5}\s+"                                # house number
            r"[A-Za-z0-9\s]+?(?:dr|st|road|ave|blvd|street|ln|lane|rd)\b"  # street
            r"(?:\s*,?\s*)"                              # comma / space
            r"[A-Za-z\s]+"                               # city
            r"\s*,?\s*"                                  # comma / space
            r"(?:ca|tx|fl|ny|wa|az|or|co|ga|oh|il|pa|nc|nd|nm|nv|ok|ks|al|ar|ia|id|sd|sc|ut|va|wv|wi|mi|mn)"  # state
            r"\s*[, ]\s*"                                # separator
            r"\d{5}(?:-\d{4})?"                          # ZIP
        )

        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()

        return None

    # ----------------------------------------------------------
    # CONFIDENCE SCORING (When to use Qwen)
    # ----------------------------------------------------------
    def is_low_confidence(self, name, address):
        """
        Decide whether LLM fallback (Qwen) is needed.
        """

        # NAME VALIDATION
        if not name:
            return True

        name_lower = name.lower()

        bad_name_words = {
            "sender", "colle", "srra", "priority", "mail",
            "fees", "postage", "notifi", "notifii", "usps", "ups"
        }

        if any(w in name_lower for w in bad_name_words):
            return True

        if len(name.split()) < 2 or len(name.split()) > 3:
            return True

        # ADDRESS VALIDATION
        if not address:
            return True

        addr_lower = address.lower()

        if name_lower in addr_lower:
            return True

        if "sender" in addr_lower:
            return True

        if len(address) > 120:
            return True

        if not re.search(r"\d{2,5}\s", addr_lower):
            return True

        if not re.search(r"\d{5}", addr_lower):
            return True

        return False  # Confidence is high

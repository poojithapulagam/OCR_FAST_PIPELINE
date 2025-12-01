import pandas as pd
from config import OCR_TEST_DATA_PATH, RECIPIENT_DB_PATH
from src.extractors.fast_extractor import FastExtractor
from src.extractors.llm_extractor import LLMExtractor
from src.utils.fuzzy_matcher import RecipientMatcher

class OCRPipeline:

    def __init__(self):
        self.llm = LLMExtractor()
        self.fast = FastExtractor(llm_extractor=self.llm)
        self.matcher = RecipientMatcher(RECIPIENT_DB_PATH)

    def process_single(self, text):
        name = self.fast.extract_person(text)
        address = self.fast.extract_address(text)

        matches = self.matcher.match_pair(name or "", address or "")

        return {
            "name": name,
            "address": address,
            "matches": matches
        }

    def run(self):
        df = pd.read_csv(OCR_TEST_DATA_PATH)
        results = []

        for text in df["ocr_text"]:
            results.append(self.process_single(text))

        return results

# src/pipeline.py

import pandas as pd
import re

from src.extractors.fast_extractor import FastExtractor
from src.extractors.llm_extractor import LLMExtractor
from src.utils.fuzzy_matcher import FuzzyMatcher


class OCRPipeline:

    def __init__(self, input_file="data/ocr_test_data.csv"):
        self.input_file = input_file
        self.extractor = FastExtractor()
        self.llm = LLMExtractor()
        self.matcher = FuzzyMatcher()

    # -----------------------------
    # LLM VALIDATIONS
    # -----------------------------
    def is_valid_name(self, name):
        if not name:
            return False
        if len(name.split()) > 4:
            return False
        if re.search(r"\d", name):
            return False
        return True

    def is_valid_address(self, addr):
        if not addr:
            return False
        if not re.search(r"\d{5}", addr):
            return False
        if not re.search(r"\d{2,5}\s", addr):
            return False
        return True

    # -----------------------------
    # MAIN PIPELINE
    # -----------------------------
    def run(self):
        df = pd.read_csv(self.input_file)
        results = []

        for i, row in df.iterrows():
            raw_text = row["ocr_text"]

            print("\n==============================")
            print(f"🔍 Processing Record {i+1}")
            print("==============================")

            try:
                # -----------------------------------
                # 1️⃣ FAST EXTRACTOR FIRST
                # -----------------------------------
                fast_name = self.extractor.extract_name(raw_text)
                fast_addr = self.extractor.extract_address(raw_text)

                print(f"FAST Name: {fast_name}")
                print(f"FAST Address: {fast_addr}")

                needs_llm = self.extractor.is_low_confidence(fast_name, fast_addr)

                # -----------------------------------
                # 2️⃣ CALL QWEN ONLY IF NEEDED
                # -----------------------------------
                if needs_llm:
                    print("⚠ Low confidence → calling Qwen AI...")
                    llm_output = self.llm.extract_name_address_pairs(raw_text)

                    if llm_output:
                        llm = llm_output[0]
                        llm_name = llm.get("input_name")
                        llm_addr = llm.get("input_address")

                        if self.is_valid_name(llm_name):
                            fast_name = llm_name

                        if self.is_valid_address(llm_addr):
                            fast_addr = llm_addr

                        print("✔ Qwen extraction used.")
                    else:
                        print("⚠ Qwen returned nothing → keeping FastExtractor values.")
                else:
                    print("✔ FastExtractor confident → skipping Qwen.")

                extracted_name = fast_name
                extracted_address = fast_addr

                print(f"FINAL NAME: {extracted_name}")
                print(f"FINAL ADDRESS: {extracted_address}")

                # -----------------------------------
                # 3️⃣ FUZZY MATCHING
                # -----------------------------------
                match = self.matcher.match(extracted_name, extracted_address)

                if match:
                    print("\n🎉 MATCH FOUND!")
                    print(f"Name   : {match['preferred_full_name']}")
                    print(f"Addr   : {match['address']}")
                else:
                    print("\n❌ No matching record found.")

                results.append({
                    "raw_text": raw_text,
                    "name": extracted_name,
                    "address": extracted_address,
                    "match": match
                })

            except Exception as e:
                print("⚠ ERROR:", e)
                results.append({
                    "raw_text": raw_text,
                    "name": None,
                    "address": None,
                    "match": None
                })

        return results

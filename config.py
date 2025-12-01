from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RECIPIENT_DB_PATH = BASE_DIR / "data" / "recipient_db.json"
OCR_TEST_DATA_PATH = BASE_DIR / "data" / "ocr_test_data.csv"

TEST_RESULTS_PATH = BASE_DIR / "data" / "results.json"
REVIEW_LOG_PATH = BASE_DIR / "data" / "review_log.json"

from src.pipeline import OCRPipeline

if __name__ == "__main__":
    pipeline = OCRPipeline()
    results = pipeline.run()

    for r in results:
        print("\n=== RESULT ===")
        print("Extracted Name:", r["name"])
        print("Extracted Address:", r["address"])
        print("Match:", r["matches"])
